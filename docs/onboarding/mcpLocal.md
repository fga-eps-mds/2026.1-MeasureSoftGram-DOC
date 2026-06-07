# MeasureSoftGram AI — MCP

## Onboarding Local

Este guia descreve como configurar e executar o servidor MCP do MeasureSoftGram em ambiente local.

### Pré-requisitos

Antes de começar, certifique-se de ter as seguintes ferramentas instaladas:

| Ferramenta | Descrição |
|------------|-----------|
| [Docker](https://docs.docker.com/get-docker/) | Responsável pela containerização do projeto |
| [Docker Compose](https://docs.docker.com/compose/install/) | Utilizado para orquestrar os serviços |

### Serviços containerizados

O Docker Compose irá subir os seguintes serviços:

| Serviço | URL |
|---------|-----|
| **msgram-service** — API principal do MeasureSoftGram | `http://localhost:8080` |
| **mcp-server** — Servidor MCP que expõe as ferramentas para LLMs | `http://localhost:8000` |
| **mcp-inspector** — Interface de inspeção e debug do MCP | `http://localhost:6274` |

---

## Variáveis de Ambiente

As variáveis de ambiente devem ser configuradas dentro da pasta `env-vars/`, seguindo a estrutura de exemplo disponível em `env-vars-example/`.

Copie os arquivos de exemplo com os comandos abaixo:

```bash
cp env-vars-example/.service.env env-vars/.service.env
cp env-vars-example/.mcp.env env-vars/.mcp.env
```

> As variáveis do **service** não precisam ser alteradas — o projeto funciona corretamente com os valores padrão.
>
> As variáveis do **MCP**, no entanto, precisam ser preenchidas conforme descrito abaixo.

---

## Configurando o MCP

### Variáveis obrigatórias

Edite o arquivo `env-vars/.mcp.env` com as seguintes credenciais:

```env
SERVICE=http://service:8080/api/v1/
MSGRAM_USER=admin
MSGRAM_PASSWORD=admin
```

> Os valores acima correspondem às credenciais padrão do `msgram-service`. Caso você tenha alterado as credenciais do serviço, atualize-as aqui também.

### Escolhendo o transport (opcional)

O servidor MCP suporta dois transports. O padrão é `streamable-http`, mas pode ser alterado via variável de ambiente:

| Transport                  | Variável                                  | Rota disponível             |
|----------------------------|-------------------------------------------|-----------------------------|
| `streamable-http` (padrão) | `MCP_TRANSPORT=streamable-http` ou omitir | `http://localhost:8000/mcp` |
| `sse`                      | `MCP_TRANSPORT=sse`                       | `http://localhost:8000/sse` |

Para alterar, adicione ao arquivo `env-vars/.mcp.env`:

```env
MCP_TRANSPORT=sse  # ou streamable-http
```

---

## Subindo o Projeto

Com as variáveis de ambiente configuradas, suba todos os serviços com o Docker Compose:

```bash
docker compose -f compose.dev.yaml up --build
```

Aguarde os containers inicializarem. Após isso, os serviços estarão disponíveis nos endereços listados na seção de [Serviços containerizados](#serviços-containerizados).

---

## Vinculando ao seu Agente de IA

Com o projeto rodando localmente, a forma de configurar depende do agente que você usa.

### Agentes com suporte nativo a HTTP (Cursor, VS Code com extensão MCP, etc.)

Alguns agentes aceitam conexão HTTP diretamente no arquivo de configuração, sem necessidade de proxy:

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

> Consulte a documentação do seu agente para saber onde inserir esta configuração.

### Claude Desktop  (requer proxy stdio)

O **Claude Desktop** e  aceitam apenas o transport `stdio` no arquivo de configuração — eles não conseguem se conectar a servidores HTTP diretamente.

Para contornar isso, utilize o `mcp-remote`, uma ferramenta que age como proxy: o agente se comunica via `stdio` com o `mcp-remote`, que por sua vez encaminha as mensagens ao servidor HTTP.

```
Agente (Claude Desktop / Claude Code)
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

**Onde fica o arquivo de configuração do Claude Desktop:**

| Sistema Operacional | Caminho |
|---|---|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

> Após editar o arquivo, **feche e reabra o Claude Desktop** para carregar o novo MCP.

---

Com o MCP conectado, o LLM será capaz de:

- Listar organizações, produtos e releases cadastrados
- Consultar características, subcaracterísticas, métricas e medidas suportadas
- Verificar configurações e status de releases
- Acessar dados de análise e comparativos entre planejado e realizado
- Navegar pela árvore de relacionamentos entre entidades do MeasureSoftGram

---

## Rodando os Testes

Para executar a suíte de testes dentro do container do servidor MCP:

```bash
docker compose -f compose.dev.yaml exec mcp-server pytest -v
```

---

## Estrutura do Projeto

```txt
src/msgram_mcp/
├── __init__.py
├── server.py               # ponto de entrada — sobe o FastMCP e registra as tools
├── client.py               # cliente HTTP compartilhado entre as tools
├── auth/
│   └── msgram_auth.py      # autenticação com o msgram-service
└── tools/
    ├── __init__.py
    ├── organizations.py
    ├── releases.py
    ├── supported_characteristics.py
    ├── supported_measures.py
    ├── supported_metrics.py
    └── ...
tests/msgram_mcp/
├── test_client.py
├── test_server.py
└── auth/
    └── test_msgram_auth.py
└── tools/
    ├── test_organizations.py
    ├── test_releases.py
    ├── test_supported_characteristics.py
    ├── test_supported_measures.py
    ├── test_supported_metrics.py
    └── ....
```

---

## Versionamento

| Versão | Data       | Descrição                                                         | Autor                                    | Revisor |
|--------|------------|-------------------------------------------------------------------|------------------------------------------|---------|
| 1.0    | 24/05/2026 | Criação do documento                                              | [João Antonio](https://github.com/i-JSS) |         |
| 1.1    | 07/06/2026 | Adição de instruções para Claude Desktop e transport configurável | [João Antonio](https://github.com/i-JSS) |         |
