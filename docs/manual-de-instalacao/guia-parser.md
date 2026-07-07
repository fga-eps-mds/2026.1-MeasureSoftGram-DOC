# Manual de Uso - Parser

O `msgram-parser` é a biblioteca Python responsável por interpretar dados de diferentes fontes (arquivos JSON do SonarQube, respostas da API do GitHub) e transformá-los em uma representação interna comum, usada pelo restante do MeasureSoftGram. É publicada no PyPI e consumida diretamente pela `CLI` — não é uma dependência do `Service`.

## Instalação

```bash
pip install msgram-parser
```

## Uso

O ponto de entrada é a classe `GenericParser`, que despacha a entrada para o plugin correto de acordo com `type_input`:

```python
from genericparser.genericparser import GenericParser

parser = GenericParser()
resultado = parser.parse(
    input_value=dados_de_entrada,
    type_input="sonarqube",  # ou "github"
    filters=None,
)
```

| `type_input` | Plugin | Fonte de dados |
| :--- | :--- | :--- |
| `sonarqube` | `genericparser.plugins.statics.sonarqube` | Export de métricas do SonarQube (JSON estático) |
| `github` | `genericparser.plugins.dinamic.github` | API do GitHub (execuções de workflow, usado para `ci_feedback_time`) |

Os plugins disponíveis ficam registrados em `genericparser/accept_plugins.py` — adicionar um novo formato de entrada significa implementar um plugin novo e registrá-lo nesse mapa.

## Repositório

Código-fonte em [`fga-eps-mds/2026.1-MeasureSoftGram-Parser`](https://github.com/fga-eps-mds/2026.1-MeasureSoftGram-Parser).
