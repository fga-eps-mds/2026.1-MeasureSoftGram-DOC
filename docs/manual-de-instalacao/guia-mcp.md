# Manual de Uso - MeasureSoftGram AI (MCP)

## Pré-requisitos

- Ter o [Docker](https://docs.docker.com/get-docker/) instalado na sua máquina.
- Ter um agente de IA compatível com o protocolo MCP que **suporte MCPs locais** (ex: Claude Desktop, Cursor, VS Code com extensão MCP) e uma **conta ativa** nesse agente.
- Ter uma conta e credenciais de acesso ao MeasureSoftGram Service.

---

## Uso

Para utilizar o MeasureSoftGram AI no seu agente, suba o servidor MCP via Docker e depois vincule-o à sua ferramenta de IA.

### 1. Subindo o servidor MCP

Escolha o comando de acordo com o seu sistema operacional:

#### macOS / Linux

```bash
docker run -d \
  -p 8000:8000 \
  -e SERVICE=https://msgram-api.synaptha.com/api/v1/ \
  -e MSGRAM_USER=admin \
  -e MSGRAM_PASSWORD=admin \
  measuresoftgram/ai:homolog
```

#### Windows (PowerShell)

```powershell
docker run -d `
  -p 8000:8000 `
  -e SERVICE=https://msgram-api.synaptha.com/api/v1/ `
  -e MSGRAM_USER=admin `
  -e MSGRAM_PASSWORD=admin `
  measuresoftgram/ai:homolog
```

#### Windows (Prompt de Comando / CMD)

```cmd
docker run -d ^
  -p 8000:8000 ^
  -e SERVICE=https://msgram-api.synaptha.com/api/v1/ ^
  -e MSGRAM_USER=admin ^
  -e MSGRAM_PASSWORD=admin ^
  measuresoftgram/ai:homolog
```

Após executar o comando, o servidor MCP estará disponível em `http://localhost:8000/mcp`.

---

### 2. Vinculando ao seu Agente de IA

Com o container rodando, adicione o MCP ao seu agente através da seguinte configuração:

```json
{
  "mcpServers": {
    "measuresoftgram": {
      "type": "streamable-http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

> Consulte a documentação do seu agente para saber onde inserir esta configuração (ex: `claude_desktop_config.json` no Claude Desktop, `settings.json` no Cursor, etc.).

---

## Variáveis de Ambiente

| Variável          | Obrigatório | Descrição                                  |
|-------------------|-------------|--------------------------------------------|
| `SERVICE`         | sim         | URL base da API do MeasureSoftGram Service |
| `MSGRAM_USER`     | sim         | Usuário de acesso ao MeasureSoftGram       |
| `MSGRAM_PASSWORD` | sim         | Senha de acesso ao MeasureSoftGram         |


---

## O que o MCP disponibiliza

Com o servidor conectado, seu agente de IA terá acesso às seguintes ferramentas e capacidades:

### Navegação e Estrutura

- **Organizações** — lista as organizações cadastradas no MeasureSoftGram
- **Repositórios** — acessa os repositórios vinculados a um produto
- **Releases** — consulta as releases criadas, seu status e configurações
- **Árvore de relacionamento de entidades** — navega pela hierarquia completa do modelo (características → subcaracterísticas → medidas → métricas)

### Consulta de Dados de Qualidade

- **Características e subcaracterísticas suportadas** — lista os requisitos de qualidade disponíveis no modelo
- **Métricas e medidas suportadas** — exibe todas as métricas e medidas que podem ser coletadas e analisadas
- **Objetivos do produto** — acessa as metas de qualidade definidas para o produto
- **Últimos valores do repositório** — obtém os valores mais recentes coletados para um repositório
- **Histórico de valores do repositório** — consulta a evolução dos indicadores de qualidade ao longo do tempo

### Análise e Interpretação

- **Matriz de equilíbrio (equalizador)** — exibe o comparativo entre os requisitos de qualidade planejados e realizados
- **TSQMI** — acessa o índice de qualidade consolidado do produto
- **Identificação de pontos de melhoria** — o agente interpreta os indicadores para orientar o time a priorizar esforços e aproximar ou superar as metas da release
- **Análise de diff e norm_diff** — interpreta as funções de diferença para explicar o gap entre o planejado e o realizado em cada requisito de qualidade
- **Análise temporal** — responde sobre o comportamento da qualidade do produto ao longo do tempo, considerando características e subcaracterísticas

> **Restrição:** o MCP opera estritamente dentro do contexto do MeasureSoftGram. O agente não realiza ações externas nem acessa dados de outros sistemas ou projetos que não estejam explicitamente selecionados na requisição.


---

## Versionamento

| Versão | Data       | Descrição            | Autor                                    | Revisor |
|--------|------------|----------------------|------------------------------------------|---------|
| 1.0    | 24/05/2026 | Criação do documento | [João Antonio](https://github.com/i-JSS) |         |