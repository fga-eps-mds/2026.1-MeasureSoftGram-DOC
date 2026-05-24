import json
import os
import datetime
from glob import glob
from typing import List

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="MeasureSoftGram – Dashboard Gerencial",
    page_icon="📊",
    layout="wide",
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

REPOS_LANGUAGE = {
    "Action": "py",
    "Front": "ts",
    "Service": "py",
    "Core": "py",
    "CLI": "py",
    "AI": "py",
    "Parser": "py",
}

METRIC_LIST = [
    "files", "functions", "complexity", "comment_lines_density",
    "duplicated_lines_density", "coverage", "ncloc", "tests",
    "test_errors", "test_failures", "test_execution_time", "security_rating",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def unmarshall(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# SonarQube data loading
# ---------------------------------------------------------------------------

def metric_per_file(json_dict: dict) -> List[dict]:
    result = []
    for component in json_dict.get("components", []):
        ncloc_value = 0
        for measure in component.get("measures", []):
            if measure["metric"] == "ncloc":
                try:
                    ncloc_value = float(measure["value"])
                except (ValueError, KeyError):
                    pass
                break
        qualifier = component.get("qualifier", "")
        if (qualifier == "FIL" and ncloc_value > 0) or qualifier in ("DIR", "UTS"):
            result.append(component)
    return result


def generate_component_df(metrics_list, file_data, lang_ext):
    files_rows, dirs_rows, uts_rows = [], [], []

    for f in file_data:
        qualifier = f.get("qualifier", "")
        row = {m: None for m in metrics_list}
        row["qualifier"] = qualifier
        row["path"] = f.get("path", "")
        for measure in f.get("measures", []):
            if measure["metric"] in metrics_list:
                row[measure["metric"]] = measure.get("value")

        try:
            lang = f.get("language", "")
        except Exception:
            lang = ""

        if qualifier == "FIL" and lang == lang_ext:
            files_rows.append(row)
        elif qualifier == "DIR":
            dirs_rows.append(row)
        elif qualifier == "UTS":
            uts_rows.append(row)

    df = pd.DataFrame(files_rows + dirs_rows + uts_rows)
    return df


@st.cache_data
def load_sonar_data() -> pd.DataFrame:
    sonar_files = glob(os.path.join(DATA_DIR, "fga-eps-mds-*.json"))
    if not sonar_files:
        return pd.DataFrame()

    frames = []
    for path in sonar_files:
        base = os.path.basename(path)
        parts = base.replace(".json", "").split("-")
        # filename: fga-eps-mds-2026.1-MeasureSoftGram-<Repo>-<datetime>-<version>
        try:
            repo_short = parts[5]
            lang_ext = REPOS_LANGUAGE.get(repo_short, "py")
        except IndexError:
            lang_ext = "py"

        raw = unmarshall(path)
        file_data = metric_per_file(raw)
        df = generate_component_df(METRIC_LIST, file_data, lang_ext)
        if df.empty:
            continue

        df["filename"] = base
        aux = df["filename"].str.extract(
            r"fga-eps-mds-[\w\.]+-MeasureSoftGram-(\w+)-(\d{2}-\d{2}-\d{4}-\d{2}-\d{2}-\d{2})-(.*?)\.json"
        )
        df["repository"] = aux[0]
        df["datetime"] = aux[1]
        df["version"] = aux[2]
        frames.append(df)

    if not frames:
        return pd.DataFrame()

    result = pd.concat(frames, ignore_index=True)
    result = result.sort_values(by=["repository", "datetime"])
    return result


# ---------------------------------------------------------------------------
# SonarQube metric calculations
# ---------------------------------------------------------------------------

def get_files_df(df):
    fdf = df[df["qualifier"] == "FIL"].copy()
    fdf = fdf.dropna(subset=["functions", "complexity", "comment_lines_density",
                              "duplicated_lines_density", "coverage"])
    return fdf


def get_dir_df(df):
    dirs = df[df["qualifier"] == "DIR"].copy()
    dirs["tests"] = pd.to_numeric(dirs["tests"], errors="coerce")
    if dirs.empty or dirs["tests"].isna().all():
        return None
    return dirs.loc[dirs["tests"].idxmax()]


def get_uts_df(df):
    uts = df[df["qualifier"] == "UTS"].copy()
    uts = uts.fillna(0)
    uts = uts.dropna(subset=["test_execution_time"])
    return uts


def _ncloc(df):
    total = 0
    for val in df.get("ncloc", []):
        try:
            total += int(val)
        except (ValueError, TypeError):
            pass
    return total


def calc_complexity(df):
    fdf = get_files_df(df)
    if fdf.empty:
        return 0
    return len(fdf[(fdf["complexity"].astype(float) / fdf["functions"].astype(float)) < 10]) / len(fdf)


def calc_comments(df):
    fdf = get_files_df(df)
    if fdf.empty:
        return 0
    return len(fdf[(fdf["comment_lines_density"].astype(float) > 10) &
                   (fdf["comment_lines_density"].astype(float) < 30)]) / len(fdf)


def calc_duplication(df):
    fdf = get_files_df(df)
    if fdf.empty:
        return 0
    return len(fdf[fdf["duplicated_lines_density"].astype(float) < 5]) / len(fdf)


def calc_test_success(df):
    dir_row = get_dir_df(df)
    if dir_row is None:
        return 0
    try:
        tests = float(dir_row["tests"])
        errors = float(dir_row["test_errors"])
        failures = float(dir_row["test_failures"])
        if tests == 0:
            return 0
        return (tests - errors - failures) / tests
    except (TypeError, ValueError):
        return 0


def calc_fast_tests(df):
    uts = get_uts_df(df)
    if uts.empty:
        return 0
    return len(uts[uts["test_execution_time"].astype(float) < 300000]) / len(uts)


def calc_coverage(df):
    fdf = get_files_df(df)
    if fdf.empty:
        return 0
    return len(fdf[fdf["coverage"].astype(float) > 60]) / len(fdf)


@st.cache_data
def build_sonar_metrics(sonar_df: pd.DataFrame) -> dict:
    metrics = {}
    for repo in sonar_df["repository"].dropna().unique():
        repo_df = sonar_df[sonar_df["repository"] == repo]
        rows = []
        for dt in repo_df["datetime"].dropna().unique():
            vdf = repo_df[repo_df["datetime"] == dt]
            version = vdf["version"].iloc[0] if not vdf.empty else ""
            rows.append({
                "datetime": dt,
                "version": version,
                "complexity": calc_complexity(vdf),
                "comments": calc_comments(vdf),
                "duplication": calc_duplication(vdf),
                "test_success": calc_test_success(vdf),
                "fast_tests": calc_fast_tests(vdf),
                "coverage": calc_coverage(vdf),
                "ncloc": _ncloc(vdf),
            })

        df = pd.DataFrame(rows).sort_values("datetime").reset_index(drop=True)
        df["code_quality"] = (df["complexity"] * 0.33 + df["comments"] * 0.33 + df["duplication"] * 0.33)
        df["testing_status"] = (df["test_success"] * 0.25 + df["fast_tests"] * 0.25 + df["coverage"] * 0.5)
        df["Maintainability"] = df["code_quality"] * 0.5
        df["Reliability"] = df["testing_status"] * 0.5
        df["total"] = df["Maintainability"] + df["Reliability"]
        metrics[repo] = df

    return metrics


# ---------------------------------------------------------------------------
# GitHub data loading
# ---------------------------------------------------------------------------

@st.cache_data
def load_github_runs() -> pd.DataFrame:
    run_files = glob(os.path.join(DATA_DIR, "GitHub_API-Runs-fga-eps-mds-*.json"))
    rows = []
    for path in run_files:
        raw = unmarshall(path)
        for run in raw.get("workflow_runs", []):
            try:
                updated_at = datetime.datetime.strptime(run["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
                created_at = datetime.datetime.strptime(run["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                feedback_time = (updated_at - created_at).total_seconds()
                rows.append({
                    "Workflow ID": run["id"],
                    "Conclusion": run.get("conclusion"),
                    "Author": run["actor"]["login"],
                    "Created at": created_at,
                    "Updated at": updated_at,
                    "Feedback Time (s)": feedback_time,
                    "Workflow Name": run["path"].split("/")[-1][:-4],
                    "Repository": run["repository"]["name"].split("-")[-1],
                })
            except Exception:
                continue
    return pd.DataFrame(rows)


@st.cache_data
def load_github_issues() -> pd.DataFrame:
    issue_files = glob(os.path.join(DATA_DIR, "GitHub_API-Issues-fga-eps-mds-*.json"))
    rows = []
    for path in issue_files:
        raw = unmarshall(path)
        if not isinstance(raw, list):
            continue
        for issue in raw:
            try:
                rows.append({
                    "Issue Number": issue["number"],
                    "Title": issue.get("title", ""),
                    "Created at": pd.to_datetime(issue["created_at"]),
                    "Closed at": pd.to_datetime(issue["closed_at"]) if issue.get("closed_at") else None,
                })
            except Exception:
                continue
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

st.title("📊 MeasureSoftGram – Dashboard Gerencial")
st.caption("Qualidade interna e produtividade do time por repositório")

sonar_df = load_sonar_data()
sonar_metrics = build_sonar_metrics(sonar_df) if not sonar_df.empty else {}
runs_df = load_github_runs()
issues_df = load_github_issues()

all_repos_sonar = sorted(sonar_metrics.keys()) if sonar_metrics else []
all_repos_github = sorted(runs_df["Repository"].dropna().unique().tolist()) if not runs_df.empty else []

# Sidebar
with st.sidebar:
    st.header("Filtros")
    selected_sonar_repos = st.multiselect(
        "Repositórios (Qualidade)",
        options=all_repos_sonar,
        default=all_repos_sonar,
    )
    selected_github_repos = st.multiselect(
        "Repositórios (GitHub)",
        options=all_repos_github,
        default=all_repos_github,
    )
    st.markdown("---")
    if not runs_df.empty:
        min_date = runs_df["Created at"].min().date()
        max_date = runs_df["Created at"].max().date()
        date_range = st.date_input(
            "Período (workflow runs)",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )
    else:
        date_range = None

tab1, tab2, tab3 = st.tabs(["🚀 Produtividade (GitHub)", "🔬 Qualidade (SonarCloud)", "📈 Indicador Geral"])

# ---------------------------------------------------------------------------
# TAB 1 – Produtividade
# ---------------------------------------------------------------------------
with tab1:
    st.subheader("Produtividade do Time")

    if runs_df.empty:
        st.info("Nenhum dado de workflow runs encontrado em `data/`.")
    else:
        filtered_runs = runs_df[runs_df["Repository"].isin(selected_github_repos)].copy()

        if date_range and len(date_range) == 2:
            start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
            filtered_runs = filtered_runs[
                (filtered_runs["Created at"] >= start) & (filtered_runs["Created at"] <= end)
            ]

        col1, col2, col3 = st.columns(3)
        total_runs = len(filtered_runs)
        total_success = len(filtered_runs[filtered_runs["Conclusion"] == "success"])
        total_failure = len(filtered_runs[filtered_runs["Conclusion"] == "failure"])
        col1.metric("Total de Runs", total_runs)
        col2.metric("✅ Sucesso", total_success)
        col3.metric("❌ Falha", total_failure)

        st.markdown("---")

        # CI Feedback Time
        st.markdown("### CI Feedback Time por Repositório")
        build_runs = filtered_runs[filtered_runs["Workflow Name"] == "build"].copy()
        if not build_runs.empty:
            build_runs["Feedback Time (min)"] = build_runs["Feedback Time (s)"] / 60
            fig = px.line(
                build_runs.sort_values("Created at"),
                x="Created at", y="Feedback Time (min)",
                color="Repository", markers=True,
                labels={"Feedback Time (min)": "Tempo (min)", "Created at": "Data"},
            )
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem dados de workflow 'build' no período selecionado.")

        col_a, col_b = st.columns(2)

        # Success / Failure pie
        with col_a:
            st.markdown("### Taxa de Sucesso dos Workflows")
            counts = filtered_runs["Conclusion"].value_counts().reset_index()
            counts.columns = ["Conclusion", "Count"]
            fig2 = px.pie(
                counts, values="Count", names="Conclusion",
                color="Conclusion",
                color_discrete_map={"success": "#4CAF50", "failure": "#F44336", "cancelled": "#FFC107"},
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Success/failure by repo bar
        with col_b:
            st.markdown("### Sucesso vs Falha por Repositório")
            repo_conclusion = (
                filtered_runs.groupby(["Repository", "Conclusion"])
                .size().reset_index(name="Count")
            )
            fig3 = px.bar(
                repo_conclusion, x="Repository", y="Count",
                color="Conclusion", barmode="group",
                color_discrete_map={"success": "#4CAF50", "failure": "#F44336", "cancelled": "#FFC107"},
            )
            st.plotly_chart(fig3, use_container_width=True)

    # Team Throughput
    st.markdown("### Team Throughput (Issues)")
    if issues_df.empty:
        st.info("Nenhum dado de issues encontrado em `data/`.")
    else:
        closed = issues_df[issues_df["Closed at"].notna()]
        open_issues = issues_df[issues_df["Closed at"].isna()]

        col_c, col_d, col_e = st.columns(3)
        col_c.metric("Total de Issues", len(issues_df))
        col_d.metric("✅ Fechadas", len(closed))
        col_e.metric("🔓 Abertas", len(open_issues))

        throughput_data = pd.DataFrame({
            "Status": ["Fechadas", "Abertas"],
            "Quantidade": [len(closed), len(open_issues)],
        })
        fig4 = px.pie(
            throughput_data, values="Quantidade", names="Status",
            color="Status",
            color_discrete_map={"Fechadas": "#4CAF50", "Abertas": "#F44336"},
        )
        st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------------------------------
# TAB 2 – Qualidade SonarCloud
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("Qualidade Interna – SonarCloud")

    if not sonar_metrics:
        st.info("Nenhum dado do SonarCloud encontrado em `data/`.")
    else:
        METRIC_LABELS = {
            "complexity": "Complexidade",
            "comments": "Comentários",
            "duplication": "Duplicação",
            "test_success": "Testes Passando",
            "fast_tests": "Testes Rápidos",
            "coverage": "Cobertura",
        }

        selected_metric = st.selectbox(
            "Métrica individual",
            options=list(METRIC_LABELS.keys()),
            format_func=lambda x: METRIC_LABELS[x],
        )

        fig5 = go.Figure()
        for repo in selected_sonar_repos:
            df = sonar_metrics.get(repo)
            if df is None or df.empty:
                continue
            fig5.add_trace(go.Scatter(
                x=df["datetime"], y=df[selected_metric],
                mode="lines+markers", name=repo,
                hovertemplate="%{x}<br>%{y:.2%}",
            ))
        fig5.update_layout(
            title=f"{METRIC_LABELS[selected_metric]} por Versão/Data",
            yaxis_tickformat=".0%",
            hovermode="x unified",
        )
        st.plotly_chart(fig5, use_container_width=True)

        st.markdown("---")
        col_f, col_g = st.columns(2)

        with col_f:
            st.markdown("### Code Quality")
            fig6 = go.Figure()
            for repo in selected_sonar_repos:
                df = sonar_metrics.get(repo)
                if df is None or df.empty:
                    continue
                fig6.add_trace(go.Scatter(
                    x=df["datetime"], y=df["code_quality"],
                    mode="lines+markers", name=repo,
                    hovertemplate="%{x}<br>%{y:.2%}",
                ))
            fig6.update_layout(yaxis_tickformat=".0%", yaxis_range=[0, 1], hovermode="x unified")
            st.plotly_chart(fig6, use_container_width=True)

        with col_g:
            st.markdown("### Testing Status")
            fig7 = go.Figure()
            for repo in selected_sonar_repos:
                df = sonar_metrics.get(repo)
                if df is None or df.empty:
                    continue
                fig7.add_trace(go.Scatter(
                    x=df["datetime"], y=df["testing_status"],
                    mode="lines+markers", name=repo,
                    hovertemplate="%{x}<br>%{y:.2%}",
                ))
            fig7.update_layout(yaxis_tickformat=".0%", yaxis_range=[0, 1], hovermode="x unified")
            st.plotly_chart(fig7, use_container_width=True)

        st.markdown("### Snapshot Atual por Repositório")
        snapshot_rows = []
        for repo in selected_sonar_repos:
            df = sonar_metrics.get(repo)
            if df is None or df.empty:
                continue
            last = df.iloc[-1]
            snapshot_rows.append({
                "Repositório": repo,
                "Versão": last.get("version", ""),
                "Complexidade": f"{last['complexity']:.1%}",
                "Cobertura": f"{last['coverage']:.1%}",
                "Duplicação": f"{last['duplication']:.1%}",
                "Code Quality": f"{last['code_quality']:.1%}",
                "Testing Status": f"{last['testing_status']:.1%}",
                "Maintainability": f"{last['Maintainability']:.1%}",
                "Reliability": f"{last['Reliability']:.1%}",
                "Total": f"{last['total']:.1%}",
            })
        if snapshot_rows:
            st.dataframe(pd.DataFrame(snapshot_rows), use_container_width=True)

# ---------------------------------------------------------------------------
# TAB 3 – Indicador Geral
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("Indicador de Qualidade Geral")

    if not sonar_metrics:
        st.info("Nenhum dado do SonarCloud encontrado em `data/`.")
    else:
        fig8 = go.Figure()
        for repo in selected_sonar_repos:
            df = sonar_metrics.get(repo)
            if df is None or df.empty:
                continue
            fig8.add_trace(go.Scatter(
                x=df["datetime"], y=df["total"],
                mode="lines+markers", name=repo,
                hovertemplate="%{x}<br>Total: %{y:.2%}",
            ))
        fig8.update_layout(
            title="Indicador Total de Qualidade por Repositório",
            yaxis_tickformat=".0%",
            yaxis_range=[0, 1],
            hovermode="x unified",
        )
        st.plotly_chart(fig8, use_container_width=True)

        st.markdown("### Maintainability vs Reliability")
        fig9 = go.Figure()
        for repo in selected_sonar_repos:
            df = sonar_metrics.get(repo)
            if df is None or df.empty:
                continue
            last = df.iloc[-1]
            fig9.add_trace(go.Bar(
                x=["Maintainability", "Reliability"],
                y=[last["Maintainability"], last["Reliability"]],
                name=repo,
            ))
        fig9.update_layout(
            barmode="group",
            yaxis_tickformat=".0%",
            yaxis_range=[0, 1],
        )
        st.plotly_chart(fig9, use_container_width=True)

        st.markdown("### Boxplot — Distribuição de Qualidade")
        box_data = []
        for repo in selected_sonar_repos:
            df = sonar_metrics.get(repo)
            if df is None or df.empty:
                continue
            for _, row in df.iterrows():
                box_data.append({"Repositório": repo, "Maintainability": row["Maintainability"], "Reliability": row["Reliability"]})

        if box_data:
            box_df = pd.DataFrame(box_data)
            fig10 = px.box(
                box_df.melt(id_vars="Repositório", var_name="Aspecto", value_name="Valor"),
                x="Repositório", y="Valor", color="Aspecto",
            )
            fig10.update_layout(yaxis_tickformat=".0%")
            st.plotly_chart(fig10, use_container_width=True)
