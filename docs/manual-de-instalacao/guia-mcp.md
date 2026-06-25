# Manual de Uso - MeasureSoftGram AI (MCP)

## Pré-requisitos

- Ter o [Docker](https://docs.docker.com/get-docker/) instalado na sua máquina.
- Ter um agente de IA compatível com o protocolo MCP e uma **conta ativa** nesse agente.
- Ter uma conta e credenciais de acesso ao MeasureSoftGram Service.
- Ter o [Node.js](https://nodejs.org) instalado (o `npx` vem junto com ele).

---

## Como o MeasureSoftGram AI se conecta ao seu agente

O servidor MCP do MeasureSoftGram expõe dois transports HTTP:

| Transport         | Rota   | Descrição                                        |
|-------------------|--------|--------------------------------------------------|
| `streamable-http` | `/mcp` | Padrão atual do protocolo MCP. Recomendado.      |
| `sse`             | `/sse` | Server-Sent Events. Legado, mas ainda suportado. |

> **Importante:** Agentes como **Claude Desktop** **não aceitam conexões HTTP diretamente** no arquivo de configuração. Eles exigem o transport `stdio`, que é baseado em processo local. Para conectar esses agentes ao servidor, é necessário um **proxy** que faça a ponte entre `stdio` e o servidor HTTP, veja a seção [Vinculando ao seu Agente](#2-vinculando-ao-seu-agente-de-ia) abaixo.

---

## Uso

### 1. Subindo o servidor MCP

Escolha o comando de acordo com o seu sistema operacional:

#### macOS / Linux

```bash
docker run -d \
  -p 8000:8000 \
  -e SERVICE=https://msgram.lappis.rocks/api/v1/ \
  -e MSGRAM_USER=admin \
  -e MSGRAM_PASSWORD=admin \
  measuresoftgram/ai:homolog
```

#### Windows (PowerShell)

```powershell
docker run -d `
  -p 8000:8000 `
  -e SERVICE=https://msgram.lappis.rocks/api/v1/ `
  -e MSGRAM_USER=admin `
  -e MSGRAM_PASSWORD=admin `
  measuresoftgram/ai:homolog
```

#### Windows (Prompt de Comando / CMD)

```cmd
docker run -d ^
  -p 8000:8000 ^
  -e SERVICE=https://msgram.lappis.rocks/api/v1/ ^
  -e MSGRAM_USER=admin ^
  -e MSGRAM_PASSWORD=admin ^
  measuresoftgram/ai:homolog
```

Por padrão, o servidor sobe com o transport `streamable-http` e fica disponível em `http://localhost:8000/mcp`.

Caso queira usar o transport `sse`, adicione a variável de ambiente `MCP_TRANSPORT=sse`, o servidor estará disponível em `http://localhost:8000/sse`.

#### Escolhendo o transport (opcional)

| Transport                  | Variável                                  | Rota disponível             |
|----------------------------|-------------------------------------------|-----------------------------|
| `streamable-http` (padrão) | `MCP_TRANSPORT=streamable-http` ou omitir | `http://localhost:8000/mcp` |
| `sse`                      | `MCP_TRANSPORT=sse`                       | `http://localhost:8000/sse` |

Exemplo com `sse` no macOS / Linux:

```bash
docker run -d \
  -p 8000:8000 \
  -e SERVICE=https://msgram.lappis.rocks/api/v1/ \
  -e MSGRAM_USER=admin \
  -e MSGRAM_PASSWORD=admin \
  -e MCP_TRANSPORT=sse \
  measuresoftgram/ai:homolog
```
 
---

#### Alternativa: subindo com Docker Compose

Crie um arquivo `docker-compose.yml` com o conteúdo abaixo e execute `docker compose up -d`:

```yaml
services:
  measuresoftgram-ai:
    image: measuresoftgram/ai:homolog
    ports:
      - "8000:8000"
    environment:
      - SERVICE=https://msgram.lappis.rocks/api/v1/
      - MSGRAM_USER=admin
      - MSGRAM_PASSWORD=admin
      - MCP_TRANSPORT=streamable-http  # ou sse
```

```bash
docker compose up -d
```
---

### 2. Vinculando ao seu Agente de IA

A forma de configurar depende do agente que você usa. Consulte a subseção correspondente abaixo.

---

#### Agentes com suporte nativo a HTTP (Cursor, VS Code com extensão MCP, etc.)

Alguns agentes aceitam conexão HTTP diretamente no arquivo de configuração, sem necessidade de proxy.

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

> Consulte a documentação do seu agente para saber onde inserir esta configuração (ex: `settings.json` no Cursor, arquivo de configuração da extensão no VS Code).

---

#### Claude Desktop (requer proxy stdio)

O **Claude Desktop** aceita apenas o transport `stdio` no arquivo de configuração, ele não consegue se conectar a servidores HTTP diretamente.

Para contornar isso, utilize o `mcp-remote`, uma ferramenta que age como proxy: o agente se comunica via `stdio` com o `mcp-remote`, que por sua vez encaminha as mensagens ao servidor HTTP.

```
Agente (Claude Desktop)
    ↓ stdio
mcp-remote
    ↓ streamable-http
Servidor MeasureSoftGram AI (localhost:8000/mcp)
```

**Pré-requisito:** ter o [Node.js](https://nodejs.org) instalado (o `npx` vem junto com ele). Para verificar:

```bash
node --version
npx --version
```

**Configuração no `claude_desktop_config.json`** (Claude Desktop):

```json
{
  "mcpServers": {
    "measuresoftgram": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "http://localhost:8000/mcp"]
    }
  }
}
```

> Após editar o arquivo, **feche e reabra o Claude Desktop** para carregar o novo MCP.

---

## Variáveis de Ambiente

| Variável          | Obrigatório | Descrição                                                  |
|-------------------|-------------|------------------------------------------------------------|
| `SERVICE`         | sim         | URL base da API do MeasureSoftGram Service                 |
| `MSGRAM_USER`     | sim         | Usuário de acesso ao MeasureSoftGram                       |
| `MSGRAM_PASSWORD` | sim         | Senha de acesso ao MeasureSoftGram                         |
| `MCP_TRANSPORT`   | não         | Transport do servidor: `streamable-http` (padrão) ou `sse` |

---

## O que o MCP disponibiliza

Com o servidor conectado, seu agente de IA terá acesso às seguintes ferramentas e capacidades:

### Navegação e Estrutura

- **Organizações** - lista as organizações cadastradas no MeasureSoftGram
- **Repositórios** - acessa os repositórios vinculados a um produto
- **Releases** - consulta as releases criadas, seu status e configurações
- **Árvore de relacionamento de entidades** - navega pela hierarquia completa do modelo (características → subcaracterísticas → medidas → métricas)

### Consulta de Dados de Qualidade

- **Características e subcaracterísticas suportadas** - lista os requisitos de qualidade disponíveis no modelo
- **Métricas e medidas suportadas** - exibe todas as métricas e medidas que podem ser coletadas e analisadas
- **Objetivos do produto** - acessa as metas de qualidade definidas para o produto
- **Últimos valores do repositório** - obtém os valores mais recentes coletados para um repositório
- **Histórico de valores do repositório** - consulta a evolução dos indicadores de qualidade ao longo do tempo

### Análise e Interpretação

- **Matriz de equilíbrio (equalizador)** - exibe o comparativo entre os requisitos de qualidade planejados e realizados
- **TSQMI** - acessa o índice de qualidade consolidado do produto
- **Identificação de pontos de melhoria** - o agente interpreta os indicadores para orientar o time a priorizar esforços e aproximar ou superar as metas da release
- **Análise de diff e norm_diff** - interpreta as funções de diferença para explicar o gap entre o planejado e o realizado em cada requisito de qualidade
- **Análise temporal** - responde sobre o comportamento da qualidade do produto ao longo do tempo, considerando características e subcaracterísticas

> **Restrição:** o MCP opera estritamente dentro do contexto do MeasureSoftGram. O agente não realiza ações externas nem acessa dados de outros sistemas ou projetos que não estejam explicitamente selecionados na requisição.

---

## Versionamento

| Versão | Data       | Descrição                                              | Autor                                    | Revisor |
|--------|------------|--------------------------------------------------------|------------------------------------------|---------|
| 1.0    | 24/05/2026 | Criação do documento                                   | [João Antonio](https://github.com/i-JSS) |         |
| 1.1    | 07/06/2026 | Adição de instruções para Claude Desktop (proxy stdio) | [João Antonio](https://github.com/i-JSS) |         |