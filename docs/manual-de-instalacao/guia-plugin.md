# Manual de Uso - Plugin VS Code

O Plugin MeasureSoftGram traz o painel de qualidade (TSQMI e características), os dashboards do Grafana e a execução local da GitHub Action para dentro do VS Code.

## O que o plugin faz

- **Score unificado (TSQMI)** — um único número de 0 a 1 que resume a saúde do projeto.
- **Três dimensões de qualidade** — Confiabilidade, Manutenibilidade e Adequação Funcional, cada uma com valor atual e meta configurável.
- **Dashboards Grafana embutidos** — os painéis analíticos carregados diretamente dentro do VS Code, via `iframe`, sem abrir o navegador.
- **Execução local da Action** — roda o workflow da GitHub Action dentro do editor (usando Docker + `nektos/act`), com log detalhado no painel Output.

## Instalação

1. Instale a extensão **MeasureSoftGram** no VS Code Marketplace e crie sua conta em [msgram.lappis.rocks](https://msgram.lappis.rocks/).
2. Clique no ícone **MeasureSoftGram** na Activity Bar lateral, ou acesse via paleta de comandos (`Ctrl+Shift+P` → `MeasureSoftGram: Abrir Painel`).
3. Faça login com sua conta — o token retornado pelo `Service` é guardado no Secret Storage do VS Code, nunca em texto plano nas configurações do workspace.

## Configuração

O plugin lê duas configurações do workspace/usuário (`settings.json` do VS Code):

| Configuração | Descrição |
| :--- | :--- |
| `msgram.serviceUrl` | URL base da API do MeasureSoftGram Service ao qual o plugin se conecta |
| `msgram.productName` | Nome do produto cujos dados de qualidade serão exibidos no painel |

O token de autenticação **não** é uma configuração de workspace — ele é obtido no login e guardado de forma segura no Secret Storage do próprio VS Code.

## Dashboards Grafana integrados

A aba **Grafana** carrega os dashboards diretamente no VS Code, já filtrados pelo produto e repositório selecionados. O plugin nunca chama o Grafana diretamente: a URL do dashboard é sempre resolvida e autorizada pelo `Service` (app `grafana_proxy`) antes de ser carregada no `iframe`.


## Histórico de Versão


| Versao | Data       | Descricao            | Autor                                    | Revisor                                  |
|--------|------------|----------------------|------------------------------------------|------------------------------------------|
| 1.0    | 05/07/2026 | Criação do documento | [Anacleto](https://github.com/jpanacleto2) | [João Antonio](https://github.com/i-JSS)                                         |    
