# Manual de Uso - Core

O `msgram_core` é a biblioteca Python que implementa o modelo matemático de qualidade do MeasureSoftGram (métricas → medidas → subcaracterísticas → características → TSQMI). Ela é publicada no PyPI e consumida como dependência direta pelo `Service` — não é executada como um serviço de rede próprio.

## Instalação

```bash
pip install msgram-core
```

## Uso

O ponto de entrada público da biblioteca é o módulo `resources.analysis`, que expõe uma função por nível do modelo de qualidade:

```python
from resources.analysis import (
    calculate_measures,
    calculate_subcharacteristics,
    calculate_characteristics,
    calculate_tsqmi,
)

resultado = calculate_measures(extracted_measures, config=pre_config)
```

| Função | Entrada | Saída |
| :--- | :--- | :--- |
| `calculate_measures` | métricas extraídas + pré-configuração | valores das medidas |
| `calculate_subcharacteristics` | medidas calculadas | valores das subcaracterísticas |
| `calculate_characteristics` | subcaracterísticas calculadas | valores das características |
| `calculate_tsqmi` | características calculadas | nota final (TSQMI) |

É exatamente essa cadeia de chamadas que o `Service` executa dentro do próprio processo Django (ver "Visão de Processo" no [Documento de Arquitetura](../planejamento/arquitetura.md)) — sem chamada de rede entre `Service` e `Core`.

## Repositório

Código-fonte em [`fga-eps-mds/2026.1-MeasureSoftGram-Core`](https://github.com/fga-eps-mds/2026.1-MeasureSoftGram-Core).
