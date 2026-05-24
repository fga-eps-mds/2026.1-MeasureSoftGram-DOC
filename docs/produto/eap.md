# Estrutura Analítica do Projeto (EAP)

## 1. Objetivo do Documento

A Estrutura Analítica do Projeto (EAP), também conhecida como Work Breakdown Structure (WBS), é a decomposição hierárquica do escopo total do trabalho a ser executado pela equipe para atingir os objetivos e gerar as entregas requeridas, conforme definido pelo PMBOK.

No contexto do MeasureSoftGram 2026.1, a EAP organiza as entregas em **ondas** — conjuntos de funcionalidades agrupadas por tema e priorizadas sequencialmente, com base nos resultados da Lean Inception da equipe. O detalhamento operacional (sprints, status, responsáveis, issues e PRs) é mantido no ZenHub/GitHub.

---

## 2. Artefato Visual da EAP

<iframe
  src="https://www.figma.com/embed?embed_host=share&url=https://www.figma.com/board/pf94qkjnSNLTh3akEM2BeB/Untitled?t=Sb7ZPs0FeDwSLwLP-1"
  width="100%"
  height="600px"
  style="border: 1px solid #e0e0e0; border-radius: 8px;"
  allowfullscreen>
</iframe>

---

## 3. Estrutura Analítica do Projeto

### 1. MeasureSoftGram 2026.1

---

### 1.1 Gerenciamento do Projeto

**Objetivo:** Planejar, monitorar e formalizar a execução do projeto ao longo do semestre, garantindo governança, comunicação e rastreabilidade das atividades.

| Código | Pacote de Trabalho | Descrição |
|:------:|:-------------------|:----------|
| 1.1.1 | Implementar método de clãs ( spotify) | Definição do escopo, cronograma, papéis e cerimônias ágeis do projeto. |
| 1.1.2 | Criação do planejamento de Custo  | Acompanhamento de sprints, gestão de riscos e controle de progresso na visão orçamentária. |
| 1.1.3 | Criação do agile EVM | Consolidação no Earned Value Management  |
| 1.1.4 | Criação do plano de risco| Criação do plano de risco do ponto de vista do projeto. |

---

### 1.2 Documentação

**Objetivo:** Definir a base técnica, a experiência do usuário e manter a documentação estrutural do projeto atualizada e acessível.

| Código | Pacote de Trabalho | Descrição |
|:------:|:-------------------|:----------|
| 1.2.1 | Atualizar Docs por Repositório | Atualização e organização da documentação técnica de cada repositório do MeasureSoftGram de forma independente. |
| 1.2.6 | Atualizar Arquitetura planejada 2026.1 | Criação e atualização da documentação técnica de arquitetura de todos os repositórios. |
| 1.2.7 | Atualizar Time 2026.1 | Documentação dos prompts e fluxos de IA utilizados no MeasureSoftGram. |

---

### 1.4 MVP

**Objetivo:** Entregar as funcionalidades planejadas no MVP Canvas, organizadas em ondas priorizadas sequencialmente.

---

### 1.4.1 Release 1 — Fundação e Acesso Inicial

| Código | Pacote de Trabalho | Descrição |
| :---: | :--- | :--- |
| 1.4.1.1 | OnBoarding | Criação do fluxo de boas-vindas, tutorial inicial e guia de primeiros passos para novos usuários na plataforma. |
| 1.4.1.2 | Segurança e usabilidade do sistema | Implementação de autenticação, controle de acesso e refinamentos na interface para garantir uma navegação segura. |

---

### 1.4.2 Release 2 — Integrações e Métricas Core (MVP)

| Código | Pacote de Trabalho | Descrição |
| :---: | :--- | :--- |
| 1.4.2.1 | Integração com Repositório GitHub | Desenvolvimento da conexão e extração de dados e métricas diretamente de repositórios do GitHub. |
| 1.4.2.2 | Comunicação MCP com Claude | Implementação do protocolo MCP para comunicação e análise de dados auxiliada pela IA Claude. |
| 1.4.2.3 | Qualidade e Confiabilidade das Métricas | Estruturação da coleta, validação e garantia de precisão dos dados extraídos para o cálculo das métricas. |
| 1.4.2.4 | Relatórios e Badges | Geração de relatórios de análise e criação de badges dinâmicas para uso em READMEs de repositórios. |
| 1.4.2.5 | APIs e Integrações Externas | Construção de APIs para permitir a comunicação do MeasureSoftGram com serviços externos. |
| 1.4.2.6 | Dashboards e Visualização de Dados | Desenvolvimento dos painéis iniciais para apresentação gráfica clara das métricas coletadas. |

---

### 1.4.3 Release 3 — Agentes, Automação e UX Avançada

| Código | Pacote de Trabalho | Descrição |
| :---: | :--- | :--- |
| 1.4.3.1 | Dashboards e Visualização de Dados | Evolução dos dashboards, incluindo novas visões, filtros avançados e consolidação da interface gráfica. |
| 1.4.3.2 | Integração com Agente de IA | Inserção de um agente de IA dedicado para fornecer insights e auxiliar na interpretação de métricas de código. |
| 1.4.3.3 | Modelos e Cálculo de Qualidade | Implementação de algoritmos avançados para gerar o índice consolidado de qualidade do software. |
| 1.4.3.4 | Visualização e UX de Qualidade | Refinamento da experiência do usuário com foco em facilitar o entendimento dos índices de qualidade. |
| 1.4.3.5 | Automação da Execução e Integração com IDEs | Criação de soluções para automatizar a análise e exibir dados de qualidade diretamente no ambiente de desenvolvimento. |
| 1.4.3.6 | Gestão de Qualidade e Configuração | Módulos de administração e configuração de parâmetros de qualidade e repositórios. |

---

## 4. Observação de Rastreabilidade

O detalhamento operacional das entregas — incluindo sprints, status de execução, responsáveis, issues e pull requests — é mantido no **ZenHub** e no **GitHub**. Este documento registra apenas a estrutura hierárquica de escopo, não sendo duplicado com informações de acompanhamento já gerenciadas nas ferramentas de gestão.

## 5. Política de Atualização

Este documento deve ser atualizado apenas em caso de **mudanças estruturais no escopo do projeto** (inclusão, exclusão ou reorganização de pacotes de trabalho). Alterações operacionais como redistribuição de tarefas entre sprints, atualização de status ou fechamento de issues **não devem ser refletidas aqui**.

## 6. Histórico de Versão

| Versão | Data | Descrição | Autor | Revisor |
|--------|------|-----------|-------|---------|
| 1.0 | 25/04/2026 | Criação do documento de EAP 2026.1 | [DeM4rcio](https://github.com/DeM4rcio) | — |
| 1.1 | 03/05/2026 | Reestruturação no padrão WBS hierárquico com embed Figma | [DeM4rcio](https://github.com/DeM4rcio) | — |
