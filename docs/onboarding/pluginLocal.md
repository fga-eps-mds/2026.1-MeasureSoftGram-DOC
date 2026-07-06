# MeasureSoftGram Plugin (VS Code)

## Onboarding Local

Este guia descreve como configurar e rodar o Plugin VS Code do MeasureSoftGram em ambiente de desenvolvimento.

### Pré-requisitos

| Ferramenta | Descrição |
| :--- | :--- |
| [Node.js 20](https://nodejs.org) | Runtime usado pelo host da extensão (`src/`) e pela `webview-ui/` |
| [VS Code](https://code.visualstudio.com/) | Editor usado para rodar e depurar a extensão (`Run Extension`, `F5`) |
| [Docker](https://docs.docker.com/get-docker/) | Necessário apenas para a execução local da GitHub Action (via `nektos/act`) |
| Repositório do Service clonado localmente | Necessário para autenticar e obter dados de qualidade reais durante o desenvolvimento |

### Estrutura do projeto

O repositório é dividido em dois projetos independentes:

```txt
src/                          # Extension Host (Node/TypeScript)
├── extension.ts              # entrypoint
├── activator.ts              # wiring dos comandos e views
├── statusbar/
├── panels/
│   ├── measureSoftGramBase.ts
│   ├── measureSoftGramPanel.ts
│   └── measureSoftGramSidebar.ts
├── services/msgramApi.ts     # cliente HTTP para o Service
└── utilities/

webview-ui/                   # React + Vite, projeto separado
└── src/
    └── components/
        ├── DashboardView.tsx
        ├── GrafanaView.tsx
        ├── SettingsView.tsx
        └── action/ActionView.tsx
```

Os dois só se comunicam por `postMessage`/`acquireVsCodeApi` — a `webview-ui` nunca chama a API do Service diretamente, sempre por meio do Extension Host.

### Instalando as dependências

```bash
npm run install:all
```

Esse comando instala as dependências do host da extensão e, em seguida, as da `webview-ui/`.

### Rodando em modo de desenvolvimento

1. Abra o repositório no VS Code.
2. Pressione `F5` (ou rode a configuração de debug **Run Extension**) — isso compila a extensão (`build:all`) e abre uma nova janela do VS Code com o plugin carregado.
3. Para desenvolver a interface da webview isoladamente no navegador (sem precisar recarregar a extensão a cada mudança):

```bash
npm run start:webview
```

### Validando contra um Service local

O plugin precisa de um `Service` rodando para autenticar e exibir dados reais. Resumo dos passos (detalhado em `GUIA_VALIDACAO_API.md`, no repositório do Plugin):

```bash
cd ../2026.1-MeasureSoftGram-Service
docker compose up -d
```

Login padrão do ambiente de desenvolvimento: usuário `admin`, senha `admin`. Configure `msgram.serviceUrl` apontando para `http://localhost:8080` e faça login pelo painel do plugin — o token é salvo automaticamente no Secret Storage do VS Code.

### Executando a Action localmente (Docker + act)

A aba **Action** do plugin roda o workflow de CI do usuário localmente, dentro de um container com o [`nektos/act`](https://github.com/nektos/act) (imagem construída a partir de `resources/docker/Dockerfile`). Isso permite testar a integração com o MeasureSoftGram sem depender de um push real para o GitHub.

### Testes

```bash
npm run test:unit           # testes do Extension Host (mocha)
npm run test:webview-run    # testes da webview-ui (vitest)
npm run test:all            # os dois conjuntos de teste
npm run test:coverage       # cobertura do Extension Host
```

## Repositório

[`fga-eps-mds/2026.1-MeasureSoftGram-Plugin`](https://github.com/fga-eps-mds/2026.1-MeasureSoftGram-Plugin)
