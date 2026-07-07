# MeasureSoftGram Parser

## Onboarding Local

Este guia descreve como configurar e rodar os testes do `msgram-parser` em ambiente de desenvolvimento local, a partir do que está na branch `develop` do repositório.

### Pré-requisitos

| Ferramenta | Descrição |
| :--- | :--- |
| Python >= 3.9 | Runtime do projeto (`pyproject.toml`) |
| pip | Gerenciador de pacotes usado no repositório — **não** há `uv`/`uv.lock` neste repositório hoje |

> **Nota:** assim como o Core, o Parser não tem `Dockerfile` nem `docker-compose.yml` — é uma biblioteca pura, sem infraestrutura própria para subir.

### Instalando as dependências

```bash
pip install -r requirements.txt
```

### Estrutura do projeto

```txt
genericparser/
├── genericparser.py                 # classe GenericParser, ponto de entrada público
├── accept_plugins.py                 # mapa type_input -> módulo do plugin
├── plugins/
│   ├── statics/sonarqube.py          # parser de export JSON do SonarQube
│   ├── dinamic/github.py             # parser da API do GitHub (workflow runs, ci feedback time)
│   └── domain/generic_class.py       # classe abstrata que cada plugin implementa
└── services/

settings.py                           # paths padrão (.msgram/msgram.json), entidades e formatos suportados
```

Cada plugin implementa sua própria lógica de extração e é resolvido dinamicamente por `importlib` a partir do valor de `type_input` passado para `GenericParser.parse()` — adicionar uma nova fonte de dados é registrar um novo plugin em `accept_plugins.py`, sem tocar na classe genérica.

### Rodando os testes

O projeto usa `tox` (não `pytest` diretamente) para padronizar o ambiente de teste:

```bash
pip install tox
tox
```

### Publicação no PyPI

O pacote (`msgram-parser`) segue o mesmo fluxo de publicação do Core: tags de release candidate (`vX.Y.ZrcN`) testadas antes da tag final (`vX.Y.Z`), publicadas via GitHub Actions com Trusted Publishing (OIDC), sem token no repositório. Detalhes em `PUBLISHING.md`, no repositório.

## Repositório

[`fga-eps-mds/2026.1-MeasureSoftGram-Parser`](https://github.com/fga-eps-mds/2026.1-MeasureSoftGram-Parser)
