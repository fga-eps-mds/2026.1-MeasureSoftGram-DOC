# MeasureSoftGram Core

## Onboarding Local

Este guia descreve como configurar e rodar os testes do `msgram_core` em ambiente de desenvolvimento local, a partir do que está na branch `develop` do repositório.

### Pré-requisitos

| Ferramenta | Descrição |
| :--- | :--- |
| Python >= 3.9 | Runtime do projeto (`pyproject.toml`) |
| pip | Gerenciador de pacotes usado no repositório — **não** há `uv`/`uv.lock` neste repositório hoje |

> **Nota:** diferente do Service e do Front, o Core não tem `Dockerfile` nem `docker-compose.yml` no repositório — é uma biblioteca pura, sem infraestrutura própria para subir.

### Instalando as dependências

```bash
pip install -r requirements.txt
```

### Estrutura do projeto

```txt
src/
├── core/
│   ├── aggregated_normalized_measures.py   # fórmulas de cada medida suportada
│   ├── measures_functions.py               # funções auxiliares de cálculo de medidas
│   ├── schemas.py                          # validação (marshmallow) dos payloads de entrada
│   └── transformations.py                  # interpolação/normalização usadas nas fórmulas
├── resources/
│   ├── analysis.py                         # API pública: calculate_measures/subcharacteristics/characteristics/tsqmi
│   └── constants.py                        # mapeamento medida -> fórmula/schema
├── staticfiles/                            # métricas suportadas e pré-configuração padrão
└── util/                                   # checagem de thresholds e exceções do domínio
```

### Rodando os testes

O projeto usa `tox` (não `pytest` diretamente) para padronizar o ambiente de teste:

```bash
pip install tox
tox
```

Para rodar um pacote ou arquivo específico:

```bash
tox tests/unit/test_measures_functions.py
```

Se a instalação do `tox` falhar por dependência de mock, instale antes:

```bash
pip install pytest-mock
```

### Publicação no PyPI

O pacote (`msgram_core`) é publicado automaticamente via GitHub Actions com **Trusted Publishing (OIDC)** — não há token/secret no repositório. O fluxo é sempre: tag de release candidate (`vX.Y.ZrcN`) primeiro, testada, e só depois a tag final (`vX.Y.Z`); a publicação da tag final é bloqueada se não existir uma rc da mesma versão já publicada. Detalhes completos em `PUBLISHING.md`, no repositório.

## Repositório

[`fga-eps-mds/2026.1-MeasureSoftGram-Core`](https://github.com/fga-eps-mds/2026.1-MeasureSoftGram-Core)
