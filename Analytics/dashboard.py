import io
import json
import os
import datetime
import urllib.request
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
# AgileEVM & Risk Matrix config
# ---------------------------------------------------------------------------

EVM_SHEET_ID = "1vEGKl1ZxSeijZwuVfzDAaH6eT9NllpKnPJGDVQK7TP0"
RISK_MONITORING_SHEET_ID = "1GwJcwHRQiUD4aSyL3WGowaQ-XBv20FOyaGkc1mXob94"

RISK_DEFINITIONS = [
    {"ID": "R01", "Descrição": "Dificuldade com as tecnologias definidas",                         "Categoria": "Técnico"},
    {"ID": "R02", "Descrição": "Saída de algum integrante do projeto",                             "Categoria": "Gerencial"},
    {"ID": "R03", "Descrição": "Falta de participação de algum integrante do projeto",             "Categoria": "Gerencial"},
    {"ID": "R04", "Descrição": "Falta de integração da equipe",                                    "Categoria": "Gerencial"},
    {"ID": "R05", "Descrição": "Atraso na disponibilização de documentação / funcionalidades",     "Categoria": "Gerencial"},
    {"ID": "R06", "Descrição": "Divergência nos horários disponíveis dos integrantes",             "Categoria": "Organizacional"},
    {"ID": "R07", "Descrição": "Indisponibilidade de plataforma de comunicação definida",          "Categoria": "Externo"},
    {"ID": "R08", "Descrição": "Definição problemática da arquitetura",                            "Categoria": "Técnico"},
    {"ID": "R09", "Descrição": "Alteração no escopo do projeto",                                   "Categoria": "Gerencial"},
    {"ID": "R10", "Descrição": "Integrante com problema de saúde",                                 "Categoria": "Externo"},
    {"ID": "R11", "Descrição": "Indisponibilidade do cliente",                                     "Categoria": "Externo"},
    {"ID": "R12", "Descrição": "Baixa qualidade do código fonte",                                  "Categoria": "Técnico"},
    {"ID": "R13", "Descrição": "Falta de disponibilização de releases para o cliente testar",      "Categoria": "Gerencial"},
    {"ID": "R14", "Descrição": "Falta de concentração durante as reuniões",                        "Categoria": "Gerencial"},
    {"ID": "R15", "Descrição": "Membro da equipe sobrecarregado",                                  "Categoria": "Gerencial"},
    {"ID": "R16", "Descrição": "Falha de equipamento",                                             "Categoria": "Externo"},
    {"ID": "R17", "Descrição": "Dependência entre atividades",                                     "Categoria": "Organizacional"},
]

# Column name aliases (lowercase) used for auto-detection in EVM sheets
_EVM_SPRINT_ALIASES = {"sprint", "sprint nº", "sprint nro", "sprint número", "semana", "week", "iteração"}
_EVM_SPI_ALIASES    = {"spi", "idr", "índice de desempenho de prazo", "schedule performance index"}
_EVM_CPI_ALIASES    = {"cpi", "idc", "índice de desempenho de custo", "cost performance index"}
_EVM_PV_ALIASES     = {"pv", "vp", "valor planejado", "planned value", "vp acumulado", "pv acumulado"}
_EVM_EV_ALIASES     = {"ev", "va", "valor agregado", "earned value", "va acumulado", "ev acumulado"}
_EVM_AC_ALIASES     = {"ac", "cr", "custo real", "actual cost", "ac acumulado", "cr acumulado"}
_EVM_BAC_ALIASES    = {"bac", "orçamento total", "budget at completion"}
_EVM_EAC_ALIASES    = {"eac", "estimativa no término", "estimate at completion"}

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
        base = os.path.basename(path)
        import re as _re
        _m = _re.search(r"MeasureSoftGram-(\w+)\.json$", base)
        repo_name = _m.group(1) if _m else ""

        for issue in raw:
            try:
                milestone = issue.get("milestone") or {}
                labels = issue.get("labels") or []
                rows.append({
                    "Issue Number": issue["number"],
                    "Title":        issue.get("title", ""),
                    "State":        issue.get("state", ""),
                    "Created at":   pd.to_datetime(issue["created_at"]),
                    "Closed at":    pd.to_datetime(issue["closed_at"]) if issue.get("closed_at") else None,
                    "Milestone":    milestone.get("title", ""),
                    "Labels":       ", ".join(lbl.get("name", "") for lbl in labels),
                    "Repository":   repo_name,
                })
            except Exception:
                continue
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# AgileEVM & Risk monitoring data loading
# ---------------------------------------------------------------------------

def _download_gsheet_xlsx(sheet_id: str) -> bytes | None:
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read()
    except Exception:
        return None


def _find_col(df: pd.DataFrame, aliases: set) -> str | None:
    for col in df.columns:
        if str(col).strip().lower() in aliases:
            return col
    return None


@st.cache_data(ttl=300)
def load_evm_sheets() -> dict:
    data = _download_gsheet_xlsx(EVM_SHEET_ID)
    if data is None:
        return {}
    try:
        xls = pd.ExcelFile(io.BytesIO(data), engine="openpyxl")
        return {name: xls.parse(name) for name in xls.sheet_names}
    except Exception:
        return {}


@st.cache_data(ttl=300)
def load_risk_monitoring() -> dict:
    data = _download_gsheet_xlsx(RISK_MONITORING_SHEET_ID)
    if data is None:
        return {}
    try:
        xls = pd.ExcelFile(io.BytesIO(data), engine="openpyxl")
        return {name: xls.parse(name) for name in xls.sheet_names}
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# Planejamento/Custos sheet parser
# ---------------------------------------------------------------------------

def _to_float_br(val) -> float | None:
    """Convert a Brazilian currency string or plain number to float."""
    if val is None:
        return None
    s = str(val).strip().replace("R$", "").replace("\xa0", "").replace(" ", "")
    if s in ("", "None", "nan"):
        return None
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    try:
        f = float(s)
        return f if not (f != f) else None  # reject NaN
    except ValueError:
        return None


def _brl(value: float) -> str:
    """Format float as Brazilian Real string."""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def parse_planejamento_sheet(df: pd.DataFrame) -> dict:
    """
    Parse the multi-table Custos/Planejamento EVM sheet.
    Returns extracted data: sprint costs, member count, release costs,
    project totals, and calendar.
    """
    result: dict = {}
    nr, nc = df.shape

    def cell(r, c) -> str:
        return str(df.iloc[r, c]).strip() if 0 <= r < nr and 0 <= c < nc else ""

    def find_section(text: str) -> int | None:
        tl = text.lower()
        for r in range(nr):
            for c in range(nc):
                if tl in cell(r, c).lower():
                    return r
        return None

    def find_row_exact(label: str, start: int = 0, end: int | None = None) -> int | None:
        ll = label.lower()
        for r in range(start, end or nr):
            for c in range(nc):
                if cell(r, c).lower() == ll:
                    return r
        return None

    # ---- Locate the Semana 1…N column positions ----
    week_cols: list[tuple[int, str]] = []
    for r in range(nr):
        hits = [(c, cell(r, c)) for c in range(nc) if cell(r, c).startswith("Semana ")]
        if len(hits) >= 10:
            for col_idx, lbl in hits:
                try:
                    int(lbl.split()[1])
                    week_cols.append((col_idx, lbl))
                except (ValueError, IndexError):
                    pass
            week_cols.sort(key=lambda x: int(x[1].split()[1]))
            break

    if not week_cols:
        return result

    result["semanas"] = [w[1] for w in week_cols]

    def week_row_values(r: int) -> list[float]:
        return [_to_float_br(df.iloc[r, c]) or 0.0 for c, _ in week_cols]

    # ---- Quantidade de membros ----
    r_mem = find_row_exact("quantidade de membros")
    if r_mem is not None:
        result["membros_por_semana"] = week_row_values(r_mem)

    # ---- Generic sub-table extractor ----
    first_wc = week_cols[0][0] if week_cols else 1
    desc_c = first_wc - 1  # Description column is one before "Semana 1"

    def extract_table(section_label: str) -> pd.DataFrame:
        r_sec = find_section(section_label)
        if r_sec is None:
            return pd.DataFrame()
        rows: list[dict] = []
        found = False
        for r in range(r_sec + 1, min(r_sec + 80, nr)):
            d = cell(r, desc_c)
            if d.lower() in ("descrição", "descricao", "tr"):
                continue
            week_vals = [_to_float_br(df.iloc[r, wc]) for wc, _ in week_cols]
            has_num = any(v is not None for v in week_vals)
            has_lbl = d and d not in ("", "None")
            if not has_lbl and not has_num:
                if found:
                    break
                continue
            found = True
            row_dict: dict = {"Descrição": d if has_lbl else ""}
            for (_, wname), v in zip(week_cols, week_vals):
                row_dict[wname] = v if v is not None else 0.0
            rows.append(row_dict)
        return pd.DataFrame(rows) if rows else pd.DataFrame()

    result["tabela_membros"]            = extract_table("quantidade de membros")
    result["tabela_custo_operacional"]  = extract_table("custo operacional")
    result["tabela_planejamento"]       = extract_table("planejamento membros")
    result["tabela_custo_sprint"]       = extract_table("custo total por sprint")

    # ---- Custo total por Sprint → Total ----
    r_sprint = find_section("custo total por sprint")
    if r_sprint is not None:
        r_total = find_row_exact("total", r_sprint, r_sprint + 8)
        if r_total is not None:
            result["custo_por_sprint"] = week_row_values(r_total)

    # ---- Custo por Release (vertical: label | value pairs) ----
    r_rel = find_section("custo por release")
    if r_rel is not None:
        releases: dict[str, float] = {}
        for r in range(r_rel, min(r_rel + 12, nr)):
            for c in range(nc):
                lbl = cell(r, c).lower()
                for key, search in [("Release 1", "custo release 1"),
                                     ("Release 2", "custo release 2"),
                                     ("Release 3", "custo release 3")]:
                    if lbl == search:
                        for cc in range(c + 1, min(c + 4, nc)):
                            v = _to_float_br(df.iloc[r, cc])
                            if v and v > 0:
                                releases[key] = v
                                break
        if releases:
            result["custo_por_release"] = releases

    # ---- Custo total do Projeto (vertical table) ----
    r_proj = find_section("custo total do projeto")
    if r_proj is not None:
        projeto: dict[str, float] = {}
        mapping = [
            ("Pré Desenvolvimento", "custo pré desenvolvimento"),
            ("Release 1",           "custo release 1"),
            ("Release 2",           "custo release 2"),
            ("Release 3",           "custo release 3"),
            ("Pós Desenvolvimento", "custo pós desenvolvimento"),
            ("Total",               "custo total"),
        ]
        for r in range(r_proj, min(r_proj + 20, nr)):
            for c in range(nc):
                lbl = cell(r, c).lower()
                for key, search in mapping:
                    if lbl == search:
                        for cc in range(c + 1, min(c + 4, nc)):
                            v = _to_float_br(df.iloc[r, cc])
                            if v and v > 0:
                                projeto[key] = v
                                break
        if projeto:
            result["custo_total_projeto"] = projeto

    # ---- Calendário (Semana | Data) ----
    r_cal = find_section("calendário") or find_section("calendario")
    if r_cal is not None:
        for r in range(r_cal, min(r_cal + 5, nr)):
            for c in range(nc):
                if cell(r, c).lower() == "semana" and c + 1 < nc and cell(r, c + 1).lower() == "data":
                    cal: list[dict] = []
                    for dr in range(r + 1, min(r + 25, nr)):
                        sem = cell(dr, c)
                        dat = cell(dr, c + 1)
                        if sem and sem != "None" and dat and dat != "None":
                            cal.append({"label": sem, "data": dat})
                        elif len(cal) > 3:
                            break
                    if cal:
                        result["calendario"] = cal
                    break

    return result


def parse_custos_horizontal(df: pd.DataFrame) -> list[tuple[str, pd.DataFrame]]:
    """
    Parse a sheet where tables are arranged side-by-side horizontally (like the 'Custos' tab).
    Finds column groups separated by empty columns, then splits each group by header rows.
    Returns list of (title, DataFrame) pairs.
    """
    import re as _re
    nr, nc = df.shape
    if nr == 0 or nc == 0:
        return []

    def _s(r, c):
        v = str(df.iloc[r, c]).strip() if 0 <= r < nr and 0 <= c < nc else ""
        return "" if v.lower() in ("none", "nan") else v

    def _is_placeholder(v: str) -> bool:
        return bool(_re.match(r'^coluna\s+\d+$', v.lower()))

    def _is_numeric(s):
        try:
            float(s.replace(",", ".").replace("R$", "").replace("\xa0", "").replace(" ", ""))
            return True
        except ValueError:
            return False

    # Columns that contain ONLY empty/placeholder values are treated as separators
    def _col_is_real(c):
        return any(_s(r, c) and not _is_placeholder(_s(r, c)) for r in range(nr))

    # Find column groups: blocks of consecutive real-data columns
    col_groups: list[list[int]] = []
    in_grp, gstart = False, 0
    for c in range(nc):
        real = _col_is_real(c)
        if real and not in_grp:
            gstart, in_grp = c, True
        elif not real and in_grp:
            col_groups.append(list(range(gstart, c)))
            in_grp = False
    if in_grp:
        col_groups.append(list(range(gstart, nc)))

    tables: list[tuple[str, pd.DataFrame]] = []
    for group in col_groups:
        if not group:
            continue

        # Find header rows: rows where ≥50% of group cols are non-empty text (not pure numbers)
        header_rows: list[int] = []
        for r in range(nr):
            cells = [_s(r, c) for c in group]
            non_empty = [v for v in cells if v]
            if not non_empty or len(non_empty) / len(group) < 0.4:
                continue
            text_count = sum(1 for v in non_empty if not _is_numeric(v))
            if text_count / len(non_empty) >= 0.6:
                header_rows.append(r)

        if not header_rows:
            continue

        # Keep only header rows that have at least one data row after the previous header
        deduped: list[int] = [header_rows[0]]
        for hr in header_rows[1:]:
            prev = deduped[-1]
            if any(_s(r, group[0]) for r in range(prev + 1, hr)):
                deduped.append(hr)
        header_rows = deduped

        for i, hr in enumerate(header_rows):
            end_r = header_rows[i + 1] if i + 1 < len(header_rows) else nr

            col_names = {
                c: _s(hr, c) for c in group
                if _s(hr, c) and not _is_placeholder(_s(hr, c))
            }
            if not col_names:
                continue

            rows = []
            for r in range(hr + 1, end_r):
                row_data: dict = {}
                has_data = False
                for c, name in col_names.items():
                    v = _s(r, c)
                    if v:
                        has_data = True
                    num = _to_float_br(v)
                    row_data[name] = num if num is not None else (v or None)
                if has_data:
                    rows.append(row_data)

            if not rows:
                continue

            tbl = pd.DataFrame(rows).dropna(how="all", axis=1)
            if tbl.empty:
                continue

            col_str  = " ".join(col_names.values()).lower()
            data_str = " ".join(str(v) for row in rows for v in row.values() if v is not None).lower()

            if "deploy" in col_str and "domínio" in col_str:
                title = "💰 Custo de Infraestrutura"
            elif "serviços" in col_str or "hospedagem" in col_str:
                title = "🚀 Custos Deploy"
            elif "atividade" in col_str or ("horas" in col_str and "semana" in col_str):
                title = "📅 Planejamento do Projeto"
            elif "kwh" in data_str or "cons." in data_str:
                title = "⚡ Energia Individual"
            elif "valor médio" in data_str:
                title = "🌐 Internet Individual"
            elif ("unidf" in data_str or "- uf" in data_str or "crédito" in data_str
                  or "eps" in data_str):
                title = "🎓 Estudante"
            elif "computador" in data_str and ("vida util" in data_str or "depreciação" in data_str):
                title = "💻 Depreciação Computador"
            elif "release" in data_str and "custo" in data_str:
                title = "💰 Custos Totais"
            else:
                cols_preview = ", ".join(list(col_names.values())[:2])
                title = f"📋 {cols_preview}"

            tables.append((title, tbl))

    return tables


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

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🚀 Produtividade (GitHub)",
    "🔬 Qualidade (SonarCloud)",
    "📈 Indicador Geral",
    "💰 Agile EVM",
    "⚠️ Gestão de Riscos",
])

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

# ---------------------------------------------------------------------------
# TAB 4 – Agile EVM
# ---------------------------------------------------------------------------
with tab4:
    st.subheader("Agile EVM – Earned Value Management")
    st.caption(
        f"Dados carregados da [planilha de AgileEVM](https://docs.google.com/spreadsheets/d/{EVM_SHEET_ID}/edit) "
        f"(requer acesso público de leitura)."
    )

    with st.spinner("Carregando planilha de EVM..."):
        evm_sheets = load_evm_sheets()

    if not evm_sheets:
        st.warning(
            "Não foi possível carregar a planilha de EVM. "
            "Verifique se ela está compartilhada como **'Qualquer pessoa com o link pode visualizar'**."
        )
    else:
        sheet_names = list(evm_sheets.keys())
        selected_evm_sheet = st.selectbox("Aba da planilha", options=sheet_names, index=0)
        evm_df = evm_sheets[selected_evm_sheet]

        # ---- Try to parse as Custos/Planejamento sheet ----
        parsed = parse_planejamento_sheet(evm_df)

        if parsed.get("custo_por_sprint"):
            semanas       = parsed["semanas"]
            custo_sprint  = parsed["custo_por_sprint"]
            membros       = parsed.get("membros_por_semana", [])
            custo_release = parsed.get("custo_por_release", {})
            custo_projeto = parsed.get("custo_total_projeto", {})
            calendario    = parsed.get("calendario", [])

            # Detect release weeks from calendar labels
            release_sem: dict[str, str] = {}  # {"Release 1": "Semana 7", ...}
            for entry in calendario:
                lbl = entry.get("label", "")
                for rn in [1, 2, 3]:
                    if f"release {rn}" in lbl.lower():
                        try:
                            wk = int(lbl.split()[0])
                            if 1 <= wk <= len(semanas):
                                release_sem[f"Release {rn}"] = semanas[wk - 1]
                        except (ValueError, IndexError):
                            pass

            # -- KPI cards --
            total_proj = custo_projeto.get("Total") or sum(custo_sprint)
            kpi_cols = st.columns(4)
            kpi_cols[0].metric("💰 Custo Total do Projeto", _brl(total_proj))
            for idx, rname in enumerate(["Release 1", "Release 2", "Release 3"]):
                val = custo_release.get(rname) or custo_projeto.get(rname)
                kpi_cols[idx + 1].metric(f"🏁 {rname}", _brl(val) if val else "—")

            st.markdown("---")

            # -- Custo por Sprint bar chart --
            st.markdown("### Custo por Sprint (Semana)")
            sprint_df = pd.DataFrame({"Semana": semanas, "Custo (R$)": custo_sprint})
            fig_sprint = px.bar(
                sprint_df, x="Semana", y="Custo (R$)",
                color_discrete_sequence=["#2196F3"],
                text=sprint_df["Custo (R$)"].apply(lambda v: _brl(v)),
            )
            fig_sprint.update_traces(textposition="outside", textfont_size=10)
            for rname, sem_label in release_sem.items():
                fig_sprint.add_vline(
                    x=sem_label, line_dash="dash", line_color="#F44336", line_width=2,
                    annotation_text=rname, annotation_position="top",
                    annotation_font_color="#F44336",
                )
            fig_sprint.update_layout(
                yaxis_tickformat=",.0f",
                hovermode="x unified",
                uniformtext_minsize=8,
                uniformtext_mode="hide",
            )
            st.plotly_chart(fig_sprint, use_container_width=True)

            col_e1, col_e2 = st.columns(2)

            # -- Composição do custo do projeto --
            with col_e1:
                st.markdown("### Composição do Custo do Projeto")
                breakdown = {k: v for k, v in custo_projeto.items() if k != "Total" and v}
                if breakdown:
                    bd_df = pd.DataFrame(list(breakdown.items()), columns=["Fase", "Custo"])
                    fig_bd = px.bar(
                        bd_df, x="Custo", y="Fase", orientation="h",
                        color="Fase",
                        color_discrete_sequence=px.colors.qualitative.Set2,
                        text=bd_df["Custo"].apply(_brl),
                    )
                    fig_bd.update_traces(textposition="outside")
                    fig_bd.update_layout(
                        showlegend=False,
                        xaxis_tickformat=",.0f",
                        xaxis_title="Custo (R$)",
                        yaxis_title="",
                    )
                    st.plotly_chart(fig_bd, use_container_width=True)

            # -- Membros ativos por semana --
            with col_e2:
                st.markdown("### Membros Ativos por Semana")
                if membros:
                    mem_df = pd.DataFrame({"Semana": semanas, "Membros": membros})
                    fig_mem = px.area(
                        mem_df, x="Semana", y="Membros",
                        color_discrete_sequence=["#4CAF50"],
                        markers=True,
                    )
                    for rname, sem_label in release_sem.items():
                        fig_mem.add_vline(
                            x=sem_label, line_dash="dash", line_color="#F44336",
                            annotation_text=rname, annotation_position="top",
                            annotation_font_color="#F44336",
                        )
                    fig_mem.update_layout(
                        yaxis_range=[0, max(membros) + 3],
                        yaxis_title="Nº de Membros",
                        hovermode="x unified",
                    )
                    st.plotly_chart(fig_mem, use_container_width=True)

            # -- Tabelas separadas da planilha --
            st.markdown("---")
            st.markdown("### Detalhamento da Planilha")

            def _split_raw_tables(df: pd.DataFrame) -> list[pd.DataFrame]:
                """Split the flat evm_df into separate tables using 'Descrição' header rows."""
                nr, nc = df.shape

                # Find the description column: one column before "Semana 1"
                desc_c = None
                for r in range(min(10, nr)):
                    for c in range(nc):
                        v = str(df.iloc[r, c]).strip()
                        if v == "Semana 1":
                            desc_c = max(0, c - 1)
                            break
                    if desc_c is not None:
                        break
                if desc_c is None:
                    return []

                def cell(r, c):
                    if 0 <= r < nr and 0 <= c < nc:
                        v = str(df.iloc[r, c]).strip()
                        return "" if v.lower() in ("none", "nan") else v
                    return ""

                # Find all header rows (rows where desc_c == "Descrição")
                header_rows = [
                    r for r in range(nr)
                    if cell(r, desc_c).lower() in ("descrição", "descricao")
                ]

                tables = []
                for i, hr in enumerate(header_rows):
                    end_r = header_rows[i + 1] if i + 1 < len(header_rows) else nr

                    # Build column map {col_idx: col_name} from the header row
                    col_map = {}
                    for c in range(nc):
                        v = cell(hr, c)
                        if v:
                            col_map[c] = v

                    if not col_map:
                        continue

                    # Collect data rows
                    rows = []
                    for r in range(hr + 1, end_r):
                        row_data = {}
                        has_data = False
                        for c, name in col_map.items():
                            v = cell(r, c)
                            if v:
                                has_data = True
                            num = _to_float_br(v)
                            row_data[name] = num if num is not None else (v or None)
                        if has_data:
                            rows.append(row_data)

                    if rows:
                        tbl = pd.DataFrame(rows)
                        tbl = tbl.dropna(how="all", axis=1)
                        if not tbl.empty:
                            tables.append(tbl)

                return tables

            _TABLE_TITLES = [
                (lambda v, _: "quantidade" in v or ("membros" in v and "danilo" not in v),
                 "📊 Quantidade de Membros por Semana"),
                (lambda v, _: "infraestrutura" in v or "equipamento" in v,
                 "💻 Custos de Infraestrutura e Equipamentos"),
                (lambda v, _: any(n in v for n in ("danilo", "davi", "giovanni", "guilherme",
                    "ian", "ingrid", "joão", "luciano", "luis", "márcio",
                    "maria", "murilo", "nicollas", "raphael", "raquel", "felipe")),
                 "👥 Planejamento de Membros"),
                (lambda v, cols: "total" in v and any("semana" in c.lower() for c in cols) and len(v.split()) <= 10,
                 "🧾 Custo Total por Sprint"),
                (lambda v, cols: ("release" in v or "custo" in v) and any(
                    c.lower() in ("valor", "value") for c in cols),
                 "📈 Custos por Release e Etapas"),
            ]

            raw_tables = _split_raw_tables(evm_df)
            for idx, tbl_df in enumerate(raw_tables):
                first_col_text = " ".join(
                    str(v).lower() for v in tbl_df.iloc[:, 0] if v is not None
                )
                col_names = list(tbl_df.columns)
                title = f"📋 Tabela {idx + 1}"
                for matcher, label in _TABLE_TITLES:
                    if matcher(first_col_text, col_names):
                        title = label
                        break

                display_df = tbl_df.copy()
                desc_col = display_df.columns[0]

                # Detect member-count table by scanning all string values in the table
                all_str_vals = " ".join(
                    str(v).lower()
                    for col in display_df.columns
                    for v in display_df[col]
                    if v is not None and isinstance(v, str) and str(v).strip()
                )
                is_member_count = any(
                    k in all_str_vals for k in ("quantidade de membro", "qtd de membro")
                )

                _INT_COL_NAMES_PLAN = {
                    "#", "nº", "nro", "numero", "número",
                    "horas", "hora", "h", "sprint", "pp", "pontos", "us",
                }
                _INT_DESC_KW_PLAN = (
                    "vida util", "quantidade de", "qtd de", "nº de", "número de",
                    "sprint", "pontos planejados", "pontos real", "pontos concluí",
                    "user stor", "pp",
                )

                # Ensure description column is string before per-row detection
                display_df[desc_col] = display_df[desc_col].fillna("").astype(str)

                for col in display_df.columns:
                    col_is_int = str(col).lower().strip() in _INT_COL_NAMES_PLAN
                    formatted = []
                    for i, v in enumerate(display_df[col]):
                        if col == desc_col:
                            formatted.append(str(v) if v else "")
                            continue
                        if pd.isna(v) or v is None:
                            formatted.append("" if is_member_count else "R$ 0,00")
                            continue
                        try:
                            f = float(v)
                            if is_member_count:
                                formatted.append(str(int(f)))
                            else:
                                desc_v = display_df[desc_col].iloc[i].lower()
                                row_is_int = col_is_int or any(k in desc_v for k in _INT_DESC_KW_PLAN)
                                if row_is_int and f == int(f):
                                    formatted.append(str(int(f)))
                                else:
                                    formatted.append(_brl(f))
                        except (ValueError, TypeError):
                            formatted.append(str(v))
                    display_df[col] = formatted

                st.markdown(f"**{title}**")
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                st.divider()

            # -- Calendário --
            if calendario:
                st.markdown("**📅 Calendário de Sprints**")
                cal_df = pd.DataFrame(calendario).rename(columns={"label": "Sprint / Semana", "data": "Data"})
                st.dataframe(cal_df, use_container_width=True, hide_index=True)

            st.markdown("---")

            # -- Planejamento por Release (custo + US's) --
            st.markdown("### Planejamento por Release")

            # Build a fuzzy mapping: GitHub milestone title → EVM release key
            def _match_release_key(milestone_title: str) -> str | None:
                mt = milestone_title.lower()
                for rn in [1, 2, 3]:
                    if f"release {rn}" in mt or f"r{rn}" == mt or mt == f"v0.{rn}.0":
                        return f"Release {rn}"
                return None

            release_order = ["Release 1", "Release 2", "Release 3"]
            has_milestone_data = (
                not issues_df.empty
                and "Milestone" in issues_df.columns
                and issues_df["Milestone"].notna().any()
                and (issues_df["Milestone"] != "").any()
            )

            # Group issues by mapped release key
            rel_issues_map: dict[str, pd.DataFrame] = {}
            if has_milestone_data:
                for _, row_issue in issues_df.iterrows():
                    key = _match_release_key(str(row_issue.get("Milestone", "")))
                    if key:
                        rel_issues_map.setdefault(key, []).append(row_issue)
                rel_issues_map = {k: pd.DataFrame(v) for k, v in rel_issues_map.items()}

            rel_cols = st.columns(3)
            for idx, rname in enumerate(release_order):
                cost = custo_release.get(rname) or custo_projeto.get(rname)
                rel_df = rel_issues_map.get(rname, pd.DataFrame())
                pct = (cost / total_proj * 100) if cost and total_proj else 0

                with rel_cols[idx]:
                    st.markdown(f"#### 🏁 {rname}")
                    if cost:
                        st.metric("Custo Planejado", _brl(cost), delta=f"{pct:.1f}% do total")
                    n_issues = len(rel_df)
                    n_open   = len(rel_df[rel_df.get("State", pd.Series()) == "open"]) if not rel_df.empty and "State" in rel_df.columns else 0
                    n_closed = len(rel_df[rel_df.get("State", pd.Series()) == "closed"]) if not rel_df.empty and "State" in rel_df.columns else 0
                    st.metric("Total de US's", n_issues, delta=f"{n_closed} fechadas / {n_open} abertas" if n_issues else None)

                    if not rel_df.empty:
                        cols_to_show = [c for c in ["Issue Number", "Title", "State", "Labels", "Repository"] if c in rel_df.columns]
                        display = rel_df[cols_to_show].copy()
                        display.columns = [{"Issue Number": "#", "Title": "Título", "State": "Status",
                                            "Labels": "Labels", "Repository": "Repo"}.get(c, c) for c in cols_to_show]
                        if "Status" in display.columns:
                            display["Status"] = display["Status"].map({"open": "🔓 Aberta", "closed": "✅ Fechada"}).fillna(display["Status"])
                        st.dataframe(display, use_container_width=True, hide_index=True)
                    elif has_milestone_data:
                        st.info("Nenhuma issue vinculada a este release.")
                    else:
                        st.caption("Configure **milestones** no GitHub para ver as US's por release.")

        else:
            # ---- Try horizontal layout (e.g. 'Custos' tab) ----
            horiz_tables = parse_custos_horizontal(evm_df)
            if horiz_tables:
                st.markdown("### Detalhamento da Planilha")
                # Column names that indicate integer (count/duration) values
                _INT_COL_NAMES = {"#", "nº", "nro", "numero", "número", "horas", "hora", "h"}
                # Row description substrings that indicate integer values
                _INT_DESC_KW   = ("vida util", "quantidade de", "qtd de", "nº de", "número de")

                for htitle, htbl in horiz_tables:
                    display_htbl = htbl.copy()
                    desc_col_h = display_htbl.columns[0]

                    # Convert description column to strings first
                    display_htbl[desc_col_h] = display_htbl[desc_col_h].fillna("").astype(str)

                    for col in display_htbl.columns:
                        if col == desc_col_h:
                            continue
                        col_is_int = str(col).lower().strip() in _INT_COL_NAMES
                        formatted = []
                        for i in range(len(display_htbl)):
                            v = display_htbl[col].iloc[i]
                            if pd.isna(v) or v is None:
                                formatted.append("")
                                continue
                            desc_v = display_htbl[desc_col_h].iloc[i].lower()
                            row_is_int = col_is_int or any(k in desc_v for k in _INT_DESC_KW)
                            try:
                                f = float(v)
                                if row_is_int and f == int(f):
                                    formatted.append(str(int(f)))
                                else:
                                    formatted.append(_brl(f))
                            except (ValueError, TypeError):
                                formatted.append(str(v) if v else "")
                        display_htbl[col] = formatted

                    st.markdown(f"**{htitle}**")
                    st.dataframe(display_htbl, use_container_width=True, hide_index=True)
                    st.divider()
            else:
                # ---- Fallback: auto-detect SPI/CPI columns (for other EVM sheets) ----
                st.info(
                    f"A aba **'{selected_evm_sheet}'** não foi reconhecida como planilha de custo semanal. "
                    "Selecione a aba **'Planejamento'** para ver os gráficos de custo por sprint, "
                    "composição do projeto e membros ativos. "
                    "Se esta aba contiver SPI/CPI, os gráficos abaixo serão gerados automaticamente."
                )
            col_map = {str(c).strip().lower(): c for c in evm_df.columns}
            sprint_col = next((col_map[a] for a in _EVM_SPRINT_ALIASES if a in col_map), None)
            spi_col    = next((col_map[a] for a in _EVM_SPI_ALIASES    if a in col_map), None)
            cpi_col    = next((col_map[a] for a in _EVM_CPI_ALIASES    if a in col_map), None)
            pv_col     = next((col_map[a] for a in _EVM_PV_ALIASES     if a in col_map), None)
            ev_col     = next((col_map[a] for a in _EVM_EV_ALIASES     if a in col_map), None)
            ac_col     = next((col_map[a] for a in _EVM_AC_ALIASES     if a in col_map), None)
            bac_col    = next((col_map[a] for a in _EVM_BAC_ALIASES    if a in col_map), None)
            eac_col    = next((col_map[a] for a in _EVM_EAC_ALIASES    if a in col_map), None)

            if sprint_col:
                last_row = evm_df.dropna(subset=[sprint_col])
                if not last_row.empty:
                    last = last_row.iloc[-1]
                    m_cols = st.columns(4)
                    for idx, (label, col_name) in enumerate([
                        ("SPI", spi_col), ("CPI", cpi_col), ("BAC", bac_col), ("EAC", eac_col)
                    ]):
                        if col_name:
                            val = pd.to_numeric(last.get(col_name), errors="coerce")
                            if pd.notna(val):
                                delta = f"{val - 1:.2f}" if label in ("SPI", "CPI") else None
                                m_cols[idx].metric(label, f"{val:,.2f}", delta=delta)

            st.markdown("---")

            if sprint_col and (spi_col or cpi_col):
                st.markdown("### Índices SPI e CPI por Sprint")
                fig_idx = go.Figure()
                if spi_col:
                    fig_idx.add_trace(go.Scatter(
                        x=evm_df[sprint_col], y=pd.to_numeric(evm_df[spi_col], errors="coerce"),
                        name="SPI", mode="lines+markers", line=dict(color="#2196F3"),
                    ))
                if cpi_col:
                    fig_idx.add_trace(go.Scatter(
                        x=evm_df[sprint_col], y=pd.to_numeric(evm_df[cpi_col], errors="coerce"),
                        name="CPI", mode="lines+markers", line=dict(color="#FF9800"),
                    ))
                fig_idx.add_hline(y=1.0, line_dash="dash", line_color="green",
                                  annotation_text="Meta = 1.0", annotation_position="bottom right")
                fig_idx.update_layout(yaxis_title="Índice", xaxis_title="Sprint", hovermode="x unified")
                st.plotly_chart(fig_idx, use_container_width=True)

            if sprint_col and any([pv_col, ev_col, ac_col]):
                st.markdown("### PV × EV × AC")
                fig_ev = go.Figure()
                for col_name, label, color in [
                    (pv_col, "PV – Valor Planejado", "#607D8B"),
                    (ev_col, "EV – Valor Agregado",  "#4CAF50"),
                    (ac_col, "AC – Custo Real",       "#F44336"),
                ]:
                    if col_name:
                        fig_ev.add_trace(go.Scatter(
                            x=evm_df[sprint_col],
                            y=pd.to_numeric(evm_df[col_name], errors="coerce"),
                            name=label, mode="lines+markers", line=dict(color=color),
                        ))
                fig_ev.update_layout(xaxis_title="Sprint", yaxis_title="Valor (R$)", hovermode="x unified")
                st.plotly_chart(fig_ev, use_container_width=True)

        with st.expander("Dados Completos da Aba"):
            # Drop columns and rows that are entirely None to reduce noise from merged cells
            clean_df = evm_df.dropna(how="all", axis=1).dropna(how="all", axis=0)
            none_ratio = clean_df.isnull().mean(axis=1)
            clean_df = clean_df[none_ratio < 0.8].reset_index(drop=True)
            st.caption(f"{len(clean_df)} linhas com dados (linhas vazias de células mescladas foram ocultadas)")
            st.dataframe(clean_df, use_container_width=True)

# ---------------------------------------------------------------------------
# TAB 5 – Gestão de Riscos
# ---------------------------------------------------------------------------
with tab5:
    st.subheader("Gestão de Riscos")

    # -- Matriz 5×5 (estática conforme o documento)
    st.markdown("### Matriz Probabilidade × Impacto")
    prob_labels   = ["Muito Baixa (1)", "Baixa (2)", "Média (3)", "Alta (4)", "Muito Alta (5)"]
    impact_labels = ["Muito Baixo (1)", "Baixo (2)", "Médio (3)", "Alto (4)", "Muito Alto (5)"]
    matrix_z = [[p * i for i in range(1, 6)] for p in range(1, 6)]

    fig_heat = go.Figure(data=go.Heatmap(
        z=matrix_z,
        x=impact_labels,
        y=prob_labels,
        colorscale=[
            [0.00, "#4CAF50"],
            [0.20, "#CDDC39"],
            [0.48, "#FFC107"],
            [0.60, "#FF5722"],
            [1.00, "#B71C1C"],
        ],
        text=matrix_z,
        texttemplate="%{text}",
        showscale=True,
        colorbar=dict(
            title="Score",
            tickvals=[3, 9, 20],
            ticktext=["Baixo (1-5)", "Médio (6-12)", "Elevado (15-25)"],
        ),
    ))
    fig_heat.update_layout(
        xaxis_title="Impacto",
        yaxis_title="Probabilidade",
        height=380,
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("---")

    col_r1, col_r2 = st.columns([2, 1])

    # -- Tabela de riscos (estática do documento)
    with col_r1:
        st.markdown("### Tabela de Riscos")
        cat_icon = {"Técnico": "🔵", "Gerencial": "🟡", "Organizacional": "🟢", "Externo": "🔴"}
        risk_display = [
            {
                "ID": r["ID"],
                "Descrição": r["Descrição"],
                "Categoria": cat_icon.get(r["Categoria"], "⚪") + " " + r["Categoria"],
            }
            for r in RISK_DEFINITIONS
        ]
        st.dataframe(pd.DataFrame(risk_display), use_container_width=True, hide_index=True)

    # -- Distribuição por categoria
    with col_r2:
        st.markdown("### Distribuição por Categoria")
        cat_df = pd.DataFrame(RISK_DEFINITIONS)["Categoria"].value_counts().reset_index()
        cat_df.columns = ["Categoria", "Quantidade"]
        fig_cat = px.pie(
            cat_df, values="Quantidade", names="Categoria",
            color="Categoria",
            color_discrete_map={
                "Gerencial": "#FFC107",
                "Técnico":   "#2196F3",
                "Externo":   "#F44336",
                "Organizacional": "#4CAF50",
            },
        )
        fig_cat.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_cat, use_container_width=True)

    # -- Monitoramento de riscos (planilha dinâmica)
    st.markdown("---")
    st.markdown("### Monitoramento por Sprint")
    st.caption(
        f"Dados carregados da [planilha de monitoramento](https://docs.google.com/spreadsheets/d/{RISK_MONITORING_SHEET_ID}/edit) "
        f"(requer acesso público de leitura)."
    )

    with st.spinner("Carregando planilha de monitoramento de riscos..."):
        risk_sheets = load_risk_monitoring()

    if not risk_sheets:
        st.warning(
            "Não foi possível carregar a planilha de monitoramento. "
            "Verifique se ela está compartilhada como **'Qualquer pessoa com o link pode visualizar'**."
        )
    else:
        risk_sheet_names = list(risk_sheets.keys())
        selected_risk_sheet = st.selectbox("Aba da planilha de riscos", options=risk_sheet_names, index=0)
        risk_mon_df = risk_sheets[selected_risk_sheet]
        st.dataframe(risk_mon_df, use_container_width=True)

        # Se a primeira coluna parecer risco (R01…) e as demais colunas forem sprints/datas, plota evolução
        first_col = risk_mon_df.columns[0] if len(risk_mon_df.columns) > 0 else None
        if first_col and risk_mon_df[first_col].astype(str).str.match(r"R\d{2}").any():
            numeric_cols = [c for c in risk_mon_df.columns[1:] if pd.to_numeric(risk_mon_df[c], errors="coerce").notna().any()]
            if numeric_cols:
                st.markdown("#### Evolução do Score de Risco por Sprint")
                fig_risk_evo = go.Figure()
                for _, row in risk_mon_df.iterrows():
                    risk_id = str(row[first_col])
                    y_vals = pd.to_numeric(pd.Series([row[c] for c in numeric_cols]), errors="coerce")
                    fig_risk_evo.add_trace(go.Scatter(
                        x=numeric_cols, y=y_vals,
                        name=risk_id, mode="lines+markers",
                        hovertemplate=f"{risk_id}: %{{y}}<extra></extra>",
                    ))
                fig_risk_evo.add_hrect(y0=0, y1=5,   fillcolor="#4CAF50", opacity=0.08, line_width=0, annotation_text="Baixo")
                fig_risk_evo.add_hrect(y0=6, y1=12,  fillcolor="#FFC107", opacity=0.08, line_width=0, annotation_text="Médio")
                fig_risk_evo.add_hrect(y0=13, y1=25, fillcolor="#F44336", opacity=0.08, line_width=0, annotation_text="Elevado")
                fig_risk_evo.update_layout(
                    xaxis_title="Sprint",
                    yaxis_title="Score (P × I)",
                    yaxis_range=[0, 25],
                    hovermode="x unified",
                )
                st.plotly_chart(fig_risk_evo, use_container_width=True)
