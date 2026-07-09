# Planejado X Realizado

## 1. Introdução

Este documento apresenta a comparação entre o planejamento e a execução do projeto MeasureSoftGram ao longo do semestre 2026.1. São avaliados o Backlog e as User Stories (US) por release, além de aspectos de Custo, Tempo, Qualidade e Risco.

---

## 2. Backlog

### 2.1. Release Minor 1

**Período:** 16/03/2026 – 13/04/2026

#### Planejado

7 issues planejadas.

#### Realizado

7 issues concluídas — **100%** de conclusão.

#### Análise

A Release Minor 1 foi integralmente concluída dentro do prazo, demonstrando boa capacidade inicial do time no onboarding do projeto.

---

### 2.2. Release Major 1

**Período:** 23/03/2026 – 27/04/2026

#### Planejado

| # | User Story | Repositório |
|---|-----------|-------------|
| US003 | [Executar a action localmente e dockerizar o sistema](https://app.zenhub.com/workspaces/20261-measuresoftgram-69bc3364de61b70029078e7a/issues/zh/125) | Action / Front |
| US004 | [Atualizar a publicação da Action no GitHub Marketplace](https://app.zenhub.com/workspaces/20261-measuresoftgram-69bc3364de61b70029078e7a/issues/zh/173) | Action |
| US005 | [Criptografar senhas e tokens do sistema](https://app.zenhub.com/workspaces/20261-measuresoftgram-69bc3364de61b70029078e7a/issues/zh/182) | Service |
| US006 | [Gerenciar timeout de sessão](https://app.zenhub.com/workspaces/20261-measuresoftgram-69bc3364de61b70029078e7a/issues/zh/183) | Front |
| US007 | [Notificação visual ao expirar sessão](https://app.zenhub.com/workspaces/20261-measuresoftgram-69bc3364de61b70029078e7a/issues/zh/184) | Front |
| US008 | [Melhorar legibilidade dos textos na CLI](https://app.zenhub.com/workspaces/20261-measuresoftgram-69bc3364de61b70029078e7a/issues/zh/185) | CLI |

Total estimado: **59 issues** (incluindo tasks técnicas e de infraestrutura).

#### Realizado

50 issues concluídas — **84,7%** de conclusão.

| User Story | Status |
|-----------|--------|
| US003 – Dockerizar Action e Front | Concluído |
| US004 – Atualizar GitHub Marketplace | Concluído |
| US005 – Criptografar senhas | Concluído |
| US006 – Gerenciar timeout de sessão | Concluído |
| US007 – Notificação visual de sessão expirada | Não entregue |
| US008 – Melhorar legibilidade CLI | Concluído |

#### Histórias não entregues

- **US007** – Notificação visual ao expirar sessão: não concluída nesta release.

#### Análise

O time concluiu 84,7% do planejado. A principal pendência foi a US007, postergada em favor da priorização de itens técnicos de infraestrutura (Docker Hub, CI/CD e ambiente de desenvolvimento).

---

### 2.3. Release Minor 2

**Período:** 14/04/2026 – 04/05/2026

#### Planejado

6 issues planejadas.

#### Realizado

6 issues concluídas — **100%** de conclusão.

#### Análise

Release integralmente entregue dentro do prazo. Neste ciclo foram incorporados o servidor MCP, badge TSQMI e correções de bugs no Core e Parser.

---

### 2.4. Release Minor 3

**Período:** 05/05/2026 – 11/05/2026

#### Planejado

77 issues planejadas.

#### Realizado

34 issues concluídas — **44,2%** de conclusão.

#### Histórias não entregues

!!! warning "Dados parciais"
    Apenas o total agregado está disponível para esta release. Atualizar com a lista detalhada de US não entregues.

#### Análise

Queda significativa na taxa de conclusão. O backlog cresceu substancialmente (77 issues) enquanto a capacidade operacional do time permaneceu estável, reflexo do overcommitment identificado nos relatórios de velocity. Houve concentração de fechamento de issues próximo ao prazo da release.

---

### 2.5. Release Major 2

**Período:** 28/04/2026 – 25/05/2026  
**Data efetiva da release:** 25/05/2026

#### Planejado

49 issues planejadas.

Funcionalidades previstas:

- Criação do servidor MCP do MeasureSoftGram
- Alteração do endpoint gerador da badge TSQMI
- Nova badge TSQMI nas páginas de repositório

#### Realizado

16 issues concluídas — **32,7%** de conclusão.

| Feature | Status |
|---------|--------|
| Servidor MCP (AI) | Concluído |
| Badge TSQMI – novo endpoint (Service) | Concluído |
| Nova badge TSQMI na interface (Front) | Concluído |
| Autenticação via GitHub (Front) | Concluído |

#### Histórias não entregues

!!! warning "Dados parciais"
    Lista completa de US não entregues não disponível. Atualizar com as issues pendentes do ZenHub.

**Pendência conhecida:** US6 (correção do gráfico de semáforo) postergada para a próxima release devido à complexidade da refatoração da página de gráficos.

#### Análise

As principais funcionalidades previstas foram entregues, porém o percentual total de conclusão foi de apenas 32,7%. O escopo cresceu além da capacidade de execução, agravado pela saída de membros do time durante o ciclo.

---

### 2.6. Release Minor 4

!!! warning "Dados de backlog não fornecidos"
    Lista de issues/US planejadas e realizadas desta release não disponível. Atualizar com os dados do ZenHub. Os dados de qualidade (SonarCloud) estão disponíveis na seção 5.

---

### 2.7. Release Major 3

!!! warning "Dados de backlog não fornecidos"
    Lista de issues/US planejadas e realizadas desta release não disponível. Atualizar com os dados do ZenHub. Os dados de qualidade (SonarCloud) estão disponíveis na seção 5.

---

## 3. Custo

<iframe width="1080" height="800" src="https://docs.google.com/spreadsheets/d/1vEGKl1ZxSeijZwuVfzDAaH6eT9NllpKnPJGDVQK7TP0/edit?gid=398928793#gid=398928793"></iframe>

---

## 4. Tempo

### 4.1. Planejado

| Release | Início | Fim |
|---------|--------|-----|
| Release Minor 1 | 16/03/2026 | 13/04/2026 |
| Release Major 1 | 23/03/2026 | 27/04/2026 |
| Release Minor 2 | 14/04/2026 | 04/05/2026 |
| Release Minor 3 | 05/05/2026 | 11/05/2026 |
| Release Major 2 | 28/04/2026 | 25/05/2026 |
| Release MVP | 26/05/2026 | 22/06/2026 |

### 4.2. Executado

| Release | Início | Fim Planejado | Fim Real | Status |
|---------|--------|---------------|----------|--------|
| Release Minor 1 | 16/03/2026 | 13/04/2026 | 13/04/2026 | No prazo (100%) |
| Release Major 1 | 23/03/2026 | 27/04/2026 | 27/04/2026 | No prazo (84,7%) |
| Release Minor 2 | 14/04/2026 | 04/05/2026 | 04/05/2026 | No prazo (100%) |
| Release Minor 3 | 05/05/2026 | 11/05/2026 | 11/05/2026 | Parcial (44,2%) |
| Release Major 2 | 28/04/2026 | 25/05/2026 | 25/05/2026 | Parcial (32,7%) |
| Release MVP | 26/05/2026 | 22/06/2026 | Em andamento | Em andamento |

### 4.3. Análise

Durante o desenvolvimento do projeto, foi ajustado o escopo do MVP com a validação do cliente e a execução da primeira onda. As releases Minor 1 e 2 foram entregues integralmente no prazo. A partir da Release Minor 3, o crescimento acelerado do backlog em relação à capacidade do time resultou em percentuais de conclusão mais baixos.

---

## 5. Qualidade

### 5.1. Planejado

Foi planejado que, de acordo com as métricas do SonarCloud, todos os repositórios atingiriam as seguintes metas:

| Métrica | Critério |
|---------|----------|
| Coverage | Pelo menos 85% de cobertura |
| Reliability (Bugs) | Classificado como "A" |
| Security | Classificado como "A" |
| Hotspots Reviewed | Classificado como "A" |
| Duplication | Até 3,0% de duplicação de código |

### 5.2. Executado

!!! info "Disponibilidade dos dados"
    Os dados desta seção são provenientes de duas fontes combinadas: os **arquivos JSON persistidos** pela GitHub Action de analytics em `Analytics/data/`, e a **visualização direta do dashboard do SonarCloud**. A ausência de algumas métricas em determinadas releases se deve ao fato de que, ao longo do desenvolvimento e aprendizado do projeto, foram cometidos erros de configuração que exigiram a **recriação de alguns repositórios dentro do SonarCloud**, o que acarretou na perda parcial do histórico de análises. Por isso, a maior parte dos dados considerados são aqueles persistidos nos arquivos de analytics, complementados pontualmente pelas capturas do dashboard quando os arquivos estavam incompletos ou ausentes.

---

#### Release Minor 1 (13/04/2026)

!!! info "Métricas de qualidade não consideradas nesta release"
    As métricas de qualidade **não foram aferidas** para a Release Minor 1. O período correspondente (16/03 – 13/04/2026) foi dedicado à ambientação do time com o projeto, onboarding técnico e configuração inicial do ambiente. A GitHub Action de analytics passou a coletar dados do SonarCloud somente a partir de 24/04/2026, após a estabilização da infraestrutura.

---

#### Release Major 1 (27/04/2026)

Dados provenientes dos arquivos persistidos em `Analytics/data/` referentes a 28/04/2026, complementados pelo dashboard do SonarCloud onde necessário.

| Repositório | Linguagem | Linhas | Coverage | Reliability | Security | Duplication |
|-------------|-----------|--------|----------|-------------|----------|-------------|
| Action | TypeScript | 663 | 82,8% | A | A | 0,0% |
| CLI | Python | 1.974 | **11,0%** | — ¹ | A | 0,0% |
| Core | Python | 1.392 | 91,6% | — ¹ | A | 0,0% |
| Front | TypeScript | 17.031 | — ¹ | — ¹ | **E** | **9,8%** |
| Parser | Python | 252 | 89,6% | — ¹ | A | 0,0% |
| Service | Python | 6.809 | **0,0%** ² | A | **C** | 0,6% |

**Conformidade com as metas planejadas:**

| Repositório | Coverage ≥ 85% | Reliability A | Security A | Duplication ≤ 3% |
|-------------|:--------------:|:-------------:|:----------:|:-----------------:|
| Action | Não (82,8%) | Sim | Sim | Sim |
| CLI | **Não (11,0%)** | — | Sim | Sim |
| Core | Sim (91,6%) | — | Sim | Sim |
| Front | — | — | **Não (E)** | **Não (9,8%)** |
| Parser | Sim (89,6%) | — | Sim | Sim |
| Service | **Não (0,0%)** | Sim | **Não (C)** | Sim |

> ¹ Métrica não disponível — perda parcial de histórico decorrente da recriação de repositórios no SonarCloud durante o período de aprendizado e configuração do projeto.
> ² Service reportou 0,0% nos arquivos persistidos; o histórico completo de coverage foi parcialmente perdido pela mesma razão (ver seção 5.3).

---

#### Release Minor 2 (04/05/2026)

Dados provenientes dos arquivos persistidos em `Analytics/data/` referentes a 04/05 e 05/05. Core e Parser não possuem arquivos neste período — valores do último snapshot disponível reutilizados (marcados com `*`).

| Repositório | Linguagem | Linhas | Coverage | Reliability | Security | Duplication |
|-------------|-----------|--------|----------|-------------|----------|-------------|
| Action | TypeScript | 663 | 82,8% | A | A | 0,0% |
| CLI | Python | 1.790 | 90,8% | — ¹ | A | 0,0% |
| Core | Python | 1.392 | 91,6% * | — ¹ | A * | 0,0% * |
| Front | TypeScript | 17.066 | — ¹ | — ¹ | **E** | **9,8%** |
| Parser | Python | 252 | 89,6% * | — ¹ | A * | 0,0% * |
| Service | Python | 6.809 | **0,0%** ² | A | **C** | 0,6% |

**Conformidade com as metas planejadas:**

| Repositório | Coverage ≥ 85% | Reliability A | Security A | Duplication ≤ 3% |
|-------------|:--------------:|:-------------:|:----------:|:-----------------:|
| Action | Não (82,8%) | Sim | Sim | Sim |
| CLI | Sim (90,8%) | — | Sim | Sim |
| Core | Sim (91,6%) | — | Sim | Sim |
| Front | — | — | **Não (E)** | **Não (9,8%)** |
| Parser | Sim (89,6%) | — | Sim | Sim |
| Service | **Não (0,0%)** | Sim | **Não (C)** | Sim |

> * Último snapshot disponível nos arquivos persistidos — histórico parcialmente perdido pela recriação de repositórios no SonarCloud durante o desenvolvimento do projeto.
> ¹ Métrica não disponível — perda parcial de histórico decorrente da recriação de repositórios no SonarCloud durante o período de aprendizado e configuração do projeto.
> ² Service reportou 0,0% nos arquivos persistidos; histórico de coverage parcialmente perdido pela mesma razão (ver seção 5.3).

---

#### Release Minor 3 (11/05/2026)

Dados provenientes dos arquivos persistidos em `Analytics/data/` referentes a 11/05 e 12/05. Parser não possui arquivo neste período — valor do último snapshot disponível reutilizado (marcado com `*`).

| Repositório | Linguagem | Linhas | Coverage | Reliability | Security | Duplication |
|-------------|-----------|--------|----------|-------------|----------|-------------|
| Action | TypeScript | 663 | 82,8% | A | A | 0,0% |
| CLI | Python | 1.790 | 90,8% | — ¹ | A | 0,0% |
| Core | Python | 1.392 | 91,6% | — ¹ | A | 0,0% |
| Front | TypeScript | 11.045 ³ | 62,0% | — ¹ | A | 4,2% |
| Parser | Python | 252 | 89,6% * | — ¹ | A * | 0,0% * |
| Service | Python | 6.809 | **0,0%** ² | A | **C** | 0,6% |

**Conformidade com as metas planejadas:**

| Repositório | Coverage ≥ 85% | Reliability A | Security A | Duplication ≤ 3% |
|-------------|:--------------:|:-------------:|:----------:|:-----------------:|
| Action | Não (82,8%) | Sim | Sim | Sim |
| CLI | Sim (90,8%) | — | Sim | Sim |
| Core | Sim (91,6%) | — | Sim | Sim |
| Front | **Não (62,0%)** | — | Sim | **Não (4,2%)** |
| Parser | Sim (89,6%) | — | Sim | Sim |
| Service | **Não (0,0%)** | Sim | **Não (C)** | Sim |

> * Último snapshot disponível nos arquivos persistidos — histórico parcialmente perdido pela recriação de repositórios no SonarCloud durante o desenvolvimento do projeto.
> ¹ Métrica não disponível — perda parcial de histórico decorrente da recriação de repositórios no SonarCloud durante o período de aprendizado e configuração do projeto.
> ² Service reportou 0,0% nos arquivos persistidos; histórico de coverage parcialmente perdido pela mesma razão (ver seção 5.3).
> ³ Queda de 17.066 → 11.045 linhas no Front entre Minor 2 e Minor 3, provocada pela branch `fix-sonar-coverage` que excluiu arquivos de configuração e testes da análise estática do SonarCloud.

---

#### Release Major 2 (25/05/2026)

Dados provenientes dos arquivos persistidos em `Analytics/data/` referentes a 24/05, complementados pelo dashboard do SonarCloud para o Service (confirmado via captura de tela, análise de 25/05). Core e Parser não possuem arquivos neste período — valores do último snapshot disponível reutilizados (marcados com `*`).

| Repositório | Linguagem | Linhas | Coverage | Reliability | Security | Hotspots Reviewed | Duplication |
|-------------|-----------|--------|----------|-------------|----------|:-----------------:|-------------|
| Action | TypeScript | 663 | 82,8% | A | A | — | 0,0% |
| CLI | Python | 1.790 | 90,8% | A | A | — | 0,0% |
| Core | Python | 1.392 | 91,6% * | — ¹ | A * | — | 0,0% * |
| Front | TypeScript | 11.088 | 64,1% | **C** | A | — | 4,2% |
| Parser | Python | 252 | 89,6% * | A * | A * | A (100%) * | 0,0% * |
| Service | Python/Shell | 5.600 | 78,9% ² | A | A | **E (0,0%)** | 0,7% |

**Conformidade com as metas planejadas:**

| Repositório | Coverage ≥ 85% | Reliability A | Security A | Hotspots A | Duplication ≤ 3% |
|-------------|:--------------:|:-------------:|:----------:|:----------:|:-----------------:|
| Action | Não (82,8%) | Sim | Sim | — | Sim |
| CLI | Sim (90,8%) | Sim | Sim | — | Sim |
| Core | Sim (91,6%) | — | Sim | — | Sim |
| Front | **Não (64,1%)** | **Não (C)** | Sim | — | **Não (4,2%)** |
| Parser | Sim (89,6%) | Sim | Sim | Sim | Sim |
| Service | Não (78,9%) | Sim | Sim | **Não (E)** | Sim |

> * Último snapshot disponível nos arquivos persistidos — histórico parcialmente perdido pela recriação de repositórios no SonarCloud durante o desenvolvimento do projeto.
> ¹ Métrica não disponível — perda parcial de histórico decorrente da recriação de repositórios no SonarCloud durante o período de aprendizado e configuração do projeto.
> ² Dados do Service obtidos diretamente do dashboard do SonarCloud, que preservou o histórico desta análise mesmo após a recriação dos repositórios.

---

!!! info "Fonte dos dados desta revisão"
    Os valores de Coverage, Linhas, Duplication e as classificações Reliability/Security das seções Minor 4, Minor 5 e Major 3 abaixo foram recalculados **exclusivamente a partir dos arquivos JSON persistidos em `Analytics/data/`** deste repositório (nenhuma captura de dashboard foi usada nesta revisão). Esses arquivos não incluem contagens de bugs/vulnerabilidades nem os campos "Hotspots Reviewed" e "Quality Gate" — por isso essas duas colunas mantêm o último valor conhecido (fonte: dashboard, revisões anteriores) e não fazem parte desta correção.

#### Release Minor 4 (01/06/2026)

Dados extraídos dos arquivos JSON persistidos mais próximos de 01/06/2026. Action e Front têm snapshot exatamente nesta data. CLI, Core, Parser e Service não foram reprocessados pelo SonarCloud no período — mantêm o último valor real disponível (marcado com `*`).

| Repositório | Linguagem | Linhas | Coverage | Reliability | Security | Hotspots Reviewed | Duplication | Quality Gate |
|-------------|-----------|--------|----------|-------------|----------|-------------------|-------------|:------------:|
| Action | TypeScript | 663 | 82,7% | A | A | A (100%) | 0,0% | Passed |
| CLI | Python | 1.790 | 90,8% * | A * | A * | A (100%) * | 0,0% * | Passed * |
| Core | Python | 1.392 | 91,6% * | — * | A * | A (100%) * | 0,0% * | Passed * |
| Front | TypeScript | 11.085 | **65,0%** | **C** | A | A (100%) | 4,2% | Passed |
| Parser | Python | 252 | 89,6% * | A * | A * | A (100%) * | 0,0% * | — * |
| Service | Python/Shell | 5.541 | 78,1% * | A * | A * | **E (0,0%)** * | 0,8% * | — * |

> * Último snapshot real disponível nos arquivos de `Analytics/data/`: CLI e Service em 26/05/2026, Parser em 25/05/2026, Core em 12/05/2026 (última análise com medições — o snapshot de 25/05/2026 do Core retornou sem métricas, indício de recriação do componente no SonarCloud).

**Conformidade com as metas planejadas:**

| Repositório | Coverage ≥ 85% | Reliability A | Security A | Hotspots A | Duplication ≤ 3% |
|-------------|:--------------:|:-------------:|:----------:|:----------:|:-----------------:|
| Action | Não (82,7%) | Sim | Sim | Sim | Sim |
| CLI | Sim (90,8%) | Sim | Sim | Sim | Sim |
| Core | Sim (91,6%) | — | Sim | Sim | Sim |
| Front | **Não (65,0%)** | **Não (C)** | Sim | Sim | **Não (4,2%)** |
| Parser | Sim (89,6%) | Sim | Sim | Sim | Sim |
| Service | Não (78,1%) | Sim | Sim | **Não (E)** | Sim |

---

#### Release Minor 5 (15/06/2026)

Dados extraídos dos arquivos JSON persistidos mais próximos de 15/06/2026. Front e Parser têm snapshot exatamente nesta data; CLI tem snapshot em 16/06/2026 (1 dia após, mais próximo disponível). Action, Core e Service não possuem análise nova neste período e mantêm os mesmos valores da Minor 4 (marcados com `*`).

| Repositório | Linguagem | Linhas | Coverage | Reliability | Security | Hotspots Reviewed | Duplication | Quality Gate |
|-------------|-----------|--------|----------|-------------|----------|-------------------|-------------|:------------:|
| Action | TypeScript | 663 | 82,7% * | A * | A * | A (100%) * | 0,0% * | Passed * |
| CLI | Python | 1.790 | 90,8% ** | A ** | A ** | A (100%) ** | 0,0% ** | Passed ** |
| Core | Python | 1.392 | 91,6% * | — * | A * | A (100%) * | 0,0% * | Passed * |
| Front | TypeScript | 10.233 | **79,6%** | **C** | A | A (100%) | 1,6% | Passed |
| Parser | Python | 252 | 89,6% | A | A | A (100%) | 0,0% | — |
| Service | Python/Shell | 5.541 | 78,1% * | A * | A * | **E (0,0%)** * | 0,8% * | — * |

> * Sem análise nova desde 01/06/2026 (Action) ou 26/05/2026 (Core, Service) — valores repetidos da Minor 4.
> ** Snapshot de 16/06/2026 (1 dia após a data da release), snapshot mais próximo disponível para a CLI.

**Conformidade com as metas planejadas:**

| Repositório | Coverage ≥ 85% | Reliability A | Security A | Hotspots A | Duplication ≤ 3% |
|-------------|:--------------:|:-------------:|:----------:|:----------:|:-----------------:|
| Action | Não (82,7%) | Sim | Sim | Sim | Sim |
| CLI | Sim (90,8%) | Sim | Sim | Sim | Sim |
| Core | Sim (91,6%) | — | Sim | Sim | Sim |
| Front | Não (79,6%) | **Não (C)** | Sim | Sim | Sim |
| Parser | Sim (89,6%) | Sim | Sim | Sim | Sim |
| Service | Não (78,1%) | Sim | Sim | **Não (E)** | Sim |

---

#### Release Major 3 (29/06/2026)

Dados extraídos diretamente dos arquivos JSON persistidos em 29/06/2026 (ou no snapshot real disponível mais próximo). Front e Parser têm snapshot exatamente nesta data. Action (última análise real 01/06/2026), CLI (16/06/2026), Core (12/05/2026) e Service (26/05/2026) não possuem análises novas desde então — valores refletem o último snapshot real disponível em `Analytics/data/` (marcados com `*`). Esta release inclui pela primeira vez o repositório **Plugin**, que ainda não está integrado ao pipeline de coleta de `Analytics/data/` — seus valores seguem os últimos registrados nesta revisão, sem fonte própria nos arquivos deste repositório.

| Repositório | Linguagem | Linhas | Coverage | Reliability | Security | Hotspots Reviewed | Duplication | Quality Gate |
|-------------|-----------|--------|----------|-------------|----------|:-----------------:|-------------|:------------:|
| Action | TypeScript | 663 | 82,7% * | A * | A * | A (100%) * | 0,0% * | Passed * |
| CLI | Python | 1.790 | 90,8% * | A * | A * | A (100%) * | 0,0% * | Passed * |
| Core | Python | 1.392 | 91,6% * | — * | A * | A (100%) * | 0,0% * | Passed * |
| Front | TypeScript | 10.777 | 82,8% | **C** | A | A (100%) | 1,5% | Passed |
| Parser | Python | 252 | 89,6% | A | A | A (100%) | 0,0% | — |
| Plugin | TypeScript, CSS | 2.900 | 90,2% | **C** | **E** | **E (0,0%)** | 1,6% | **Failed** |
| Service | Python/Shell | 5.541 | 78,1% * | A * | A * | **E (0,0%)** * | 0,8% * | — * |

**Conformidade com as metas planejadas:**

| Repositório | Coverage ≥ 85% | Reliability A | Security A | Hotspots A | Duplication ≤ 3% |
|-------------|:--------------:|:-------------:|:----------:|:----------:|:-----------------:|
| Action | Não (82,7%) | Sim | Sim | Sim | Sim |
| CLI | Sim (90,8%) | Sim | Sim | Sim | Sim |
| Core | Sim (91,6%) | — | Sim | Sim | Sim |
| Front | Não (82,8%) | **Não (C)** | Sim | Sim | Sim |
| Parser | Sim (89,6%) | Sim | Sim | Sim | Sim |
| Plugin | Sim (90,2%) | **Não (C)** | **Não (E)** | **Não (E)** | Sim |
| Service | Não (78,1%) | Sim | Sim | **Não (E)** | Sim |

> * Último snapshot real disponível em `Analytics/data/` — repositório não reprocessado pelo SonarCloud entre a data indicada e a Major 3. Parser e Front têm snapshot no próprio dia 29/06/2026, por isso não levam marcador.

---

#### Release Minor 6 (06/07/2026)

Dados extraídos dos arquivos JSON persistidos mais próximos de 06/07/2026, data desta release. Apenas o **Front** foi reprocessado pelo SonarCloud nesse dia (snapshot exato). Action, CLI, Core, Parser e Service não têm análise nova desde a Major 3 e mantêm os mesmos valores (marcados com `*`); o **Service** segue retornando erro de componente não encontrado no SonarCloud em todos os runs de julho até o momento. O **Plugin** segue sem integração ao pipeline de `Analytics/data/`.

| Repositório | Linguagem | Linhas | Coverage | Reliability | Security | Hotspots Reviewed | Duplication | Quality Gate |
|-------------|-----------|--------|----------|-------------|----------|:-----------------:|-------------|:------------:|
| Action | TypeScript | 663 | 82,7% * | A * | A * | A (100%) * | 0,0% * | Passed * |
| CLI | Python | 1.790 | 90,8% * | A * | A * | A (100%) * | 0,0% * | Passed * |
| Core | Python | 1.392 | 91,6% * | — * | A * | A (100%) * | 0,0% * | Passed * |
| Front | TypeScript | 10.809 | 82,7% | **C** | A | A (100%) | 1,5% | Passed |
| Parser | Python | 252 | 89,6% * | A * | A * | A (100%) * | 0,0% * | — * |
| Plugin | TypeScript, CSS | 2.900 | 90,2% * | **C** * | **E** * | **E (0,0%)** * | 1,6% * | **Failed** * |
| Service | Python/Shell | 5.541 | 78,1% * | A * | A * | **E (0,0%)** * | 0,8% * | — * |

**Conformidade com as metas planejadas:**

| Repositório | Coverage ≥ 85% | Reliability A | Security A | Hotspots A | Duplication ≤ 3% |
|-------------|:--------------:|:-------------:|:----------:|:----------:|:-----------------:|
| Action | Não (82,7%) | Sim | Sim | Sim | Sim |
| CLI | Sim (90,8%) | Sim | Sim | Sim | Sim |
| Core | Sim (91,6%) | — | Sim | Sim | Sim |
| Front | Não (82,7%) | **Não (C)** | Sim | Sim | Sim |
| Parser | Sim (89,6%) | Sim | Sim | Sim | Sim |
| Plugin | Sim (90,2%) | **Não (C)** | **Não (E)** | **Não (E)** | Sim |
| Service | Não (78,1%) | Sim | Sim | **Não (E)** | Sim |

> * Sem snapshot novo em `Analytics/data/` nesta data — valor carregado da Major 3 (29/06/2026) ou, para o Service, do último snapshot real em 26/05/2026.

## 6. Risco

### 6.1. Tabela de Resumo

<iframe width="1080" height="800" src="https://docs.google.com/spreadsheets/d/1GwJcwHRQiUD4aSyL3WGowaQ-XBv20FOyaGkc1mXob94/edit?usp=sharing"></iframe>

### 6.2. Análise

Durante o andamento das sprints, foi observada redução na probabilidade de certos riscos, como R01 (Dificuldade com as tecnologias definidas), R06 (Divergência nos horários disponíveis dos integrantes), R13 (Falta de disponibilização de releases para o cliente testar) e R17 (Dependência entre atividades). Os ajustes de impacto foram realizados sem que nenhum risco inviabilizasse o andamento do projeto.

---

## Versionamento

| Data | Autor | Descrição | Versão |
|------|-------|-----------|--------|
| 13/09/2024 | Brenno Oliveira | Criação do documento | 0.1 |
| 27/04/2026 | [Luis Henrique](https://github.com/luishenrrique) | Planejado e realizado 2026.1 | 1.0 |
| 09/06/2026 | Anacleto | Expansão com dados por release e SonarCloud RM4 | 2.0 |
| 10/06/2026 | Anacleto | Preenche seção 5.2 com métricas do SonarCloud extraídas dos snapshots de Analytics/data para Major 1, Minor 2, Minor 3 e Major 2. Adiciona análise transversal de tendências na seção 5.3. Corrige dados da Major 2 para o Service (78,9% coverage confirmado via screenshot do SonarCloud; JSON de 25/05 estava vazio). | 2.1 |
| 29/06/2026 | Anacleto | Adiciona seção de qualidade da Release Major 3 (dados do SonarCloud de 29/06/2026) com inclusão do repositório Plugin; adiciona seção 2.7 e análise da Major 3 na seção 5.3. | 2.2 |
| 06/07/2026 | Anacleto | Recalcula as seções de qualidade da Minor 4 (01/06/2026), adiciona a Release Minor 5 (15/06/2026, antes ausente do documento) e corrige a Major 3, usando exclusivamente os arquivos JSON persistidos em `Analytics/data/` como fonte. Corrige um erro de rotulagem: os dados de Front antes atribuídos à "Minor 4" eram na verdade do snapshot de 15/06 (Minor 5) — o Front da Minor 4 real (01/06) tinha coverage de 65,0%, não 79,6%. Corrige também as datas de "última análise" de CLI (16/06, não 04/05), Core (12/05, não 26/04) e Parser (29/06 exato, não 26/04) na Major 3, e ajusta o coverage do Service para 78,1% (valor do JSON de 26/05, antes usava 78,9% de uma captura de dashboard). | 2.3 |
| 06/07/2026 | Anacleto | Remove contagens de bugs/vulnerabilidades das tabelas de qualidade (Major 2, Major 3), mantendo apenas a classificação por letra — dado não coberto pelos arquivos de `Analytics/data/`. Adiciona a Release Minor 6 (06/07/2026, data desta revisão), com dado real do Front extraído do snapshot do próprio dia e os demais repositórios carregados da Major 3. | 2.4 |
