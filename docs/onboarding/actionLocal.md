# Action

## Onboarding Local

Este guia descreve como configurar e executar a Action em ambiente local.

### Pré-requisitos

Antes de começar, certifique-se de ter as seguintes ferramentas instaladas:

| Ferramenta | Descrição |
|------------|-----------|
| [Docker](https://docs.docker.com/get-docker/) | Responsável pela containerização do projeto |
| [Node.js](https://nodejs.org/) | Necessário para compilação da Action |

### Serviços containerizados

O Docker será utilizado para orquestrar os seguintes serviços:

- **PostgreSQL** — Banco de dados relacional, exposto em `localhost:5432`
- **MeasureSoftGram Service** — API principal, exposta em `localhost:8080`
- **MeasureSoftGram Action** — Contém a biblioteca [Act](https://github.com/nektos/act), que permite executar pipelines do GitHub localmente. Este container só é iniciado quando um comando da Act é invocado.

> Para facilitar a execução das pipelines, foi criado um `Makefile` com os principais comandos — especialmente útil para quem não está familiarizado com a Act.

---

## Variáveis de Ambiente

As variáveis de ambiente devem ser configuradas dentro da pasta `env-vars/`, seguindo a estrutura de exemplo disponível em `env-vars-example/`.

> As variáveis do banco de dados e do Service **não precisam ser alteradas** — o projeto funciona corretamente com os valores padrão definidos em `env-vars-example/`.
>
> As variáveis da **Action**, no entanto, precisam ser preenchidas manualmente conforme descrito abaixo.

---

## Configurando e Executando a Action

### Estrutura da Pipeline

A criação de uma pipeline deve seguir o padrão descrito na página da Action. As seguintes variáveis de ambiente são obrigatórias:

```dotenv
GITHUB_TOKEN=SEU_GITHUB_TOKEN
SONAR_TOKEN=SEU_PROJETO_SONAR_TOKEN
MSGRAM_TOKEN=SEU_MSGRAM_SERVICE_TOKEN
MSGRAM_SERVICE_HOST=http://localhost:8080
```

---

### Obtendo o GitHub Token

O `GITHUB_TOKEN` utilizado na pipeline é um **Personal Access Token (PAT)** gerado na sua conta do GitHub. Siga os passos abaixo:

1. Acesse **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**
   (ou diretamente em `https://github.com/settings/tokens`)

2. Clique em **Generate new token → Generate new token (classic)**

3. Preencha os campos:
   - **Note:** `MeasureSoftGram Local` (ou qualquer nome identificador)
   - **Expiration:** escolha o período desejado
   - **Scopes:** selecione ao menos:
     - `repo` — acesso completo a repositórios
     - `read:org` — leitura de dados da organização
     - `user` — leitura de dados do perfil

4. Clique em **Generate token** e **copie o token gerado imediatamente** — ele não será exibido novamente.

5. Cole o valor no arquivo `env-vars/.action.env`:

```dotenv
GITHUB_TOKEN=ghp_SEU_TOKEN_AQUI
```

> **Dica:** caso o token expire, basta gerar um novo seguindo os mesmos passos e atualizar o arquivo de variáveis de ambiente.

---

### Configurando o OAuth App do GitHub (autenticação web)

Para habilitar o login via GitHub na interface web do MeasureSoftGram, é necessário criar um **OAuth App** e configurar as credenciais nos serviços. O app pode ser criado de duas formas: via conta pessoal ou via organização. Para ambientes de desenvolvimento individual, a conta pessoal é suficiente. Para ambientes compartilhados ou corporativos, recomenda-se criar pelo nível da organização.

#### Opção A — OAuth App via conta pessoal

1. Acesse **GitHub → Settings → Developer settings → OAuth Apps → New OAuth App**
   (ou diretamente em `https://github.com/settings/applications/new`)

2. Preencha os campos:

   | Campo | Valor |
   |---|---|
   | Application name | `MeasureSoftGram Local` |
   | Homepage URL | `http://localhost:3000` |
   | Authorization callback URL | `http://127.0.0.1:3000` |

3. Clique em **Register application**

4. Na página do app criado:
   - Copie o **Client ID**
   - Clique em **Generate a new client secret** e copie o secret

> **Atenção:** o client secret é exibido apenas uma vez. Guarde-o em local seguro.

---

#### Opção B — OAuth App via organização (recomendado para times)

Criar o OAuth App pelo nível da organização garante que as credenciais pertençam ao time e não a um membro individual, evitando problemas caso alguém saia da organização.

> **Pré-requisito:** você precisa ter permissão de **Owner** ou **Admin** na organização do GitHub.

1. Acesse a página da organização no GitHub e vá em:
   **Organization Settings → Developer settings → OAuth Apps → New OAuth App**
   
   A URL segue o padrão:
   ```
   https://github.com/organizations/<nome-da-org>/settings/applications/new
   ```

2. Preencha os campos:

   | Campo | Valor |
   |---|---|
   | Application name | `MeasureSoftGram` |
   | Homepage URL | `http://localhost:3000` |
   | Authorization callback URL | `http://127.0.0.1:3000` |

3. Clique em **Register application**

4. Na página do app criado:
   - Copie o **Client ID**
   - Clique em **Generate a new client secret** e copie o secret

5. Para que membros da organização consigam autenticar via esse OAuth App, pode ser necessário solicitar aprovação da organização. Caso apareça a mensagem **"Organization access"** durante o login, o owner da org precisa aprovar em:
   **Organization Settings → OAuth Application Policy**

> **Atenção:** o client secret é exibido apenas uma vez. Guarde-o em local seguro ou utilize um gerenciador de segredos (ex: GitHub Secrets, Vault).

---

#### Configurar as credenciais no Service

Edite `Service/env-vars/.service.env`:

```dotenv
GITHUB_CLIENT_ID=<seu_client_id>
GITHUB_SECRET=<seu_client_secret>
```

#### Configurar o Client ID no Front

Adicione ao arquivo `Front/.env`:

```dotenv
GITHUB_CLIENT_ID=<seu_client_id>
```

> O `GITHUB_CLIENT_ID` no Front é uma variável de **build-time** — é embutida na imagem durante o build. Sempre que alterar esse valor, execute `docker compose up --build` no diretório `Front/`.

#### Reiniciar os serviços

**Backend:**
```bash
cd Service
docker compose down
docker compose up
```

**Frontend:**
```bash
cd Front
docker compose up --build
```

Acesse `http://localhost:3000` e clique em **LOGIN COM GITHUB** para validar o fluxo.

---

### Obtendo o Sonar Token

O `SONAR_TOKEN` corresponde ao **nome do projeto no SonarQube/SonarCloud**. Durante a execução da pipeline, as métricas serão buscadas diretamente a partir desse identificador.

---

### Obtendo o MeasureSoftGram Service Token

Após subir os containers com o Docker Compose, siga os passos abaixo para gerar um token de acesso:

1. Acesse o painel administrativo em [`http://localhost:8080/admin`](http://localhost:8080/admin)
2. Faça login com as credenciais padrão:
    - **Usuário:** `admin`
    - **Senha:** `admin`
3. No menu lateral, navegue até a seção **"Tokens"**
4. Crie um novo token conforme ilustrado nas imagens abaixo:

<center>
    <a>Imagem 1 - Criação do token de autenticação MSGram</a>
</center>

![Criação de token — passo 1](../assets/images/actionLocal/img_1.png)

<center>
    <a>Imagem 2 - Hub de Tokens de autenticação MSGram</a>
</center>

![Criação de token — passo 2](../assets/images/actionLocal/img.png)


---

### Criando o Projeto no MeasureSoftGram Service

#### Produto

O parâmetro **Product Name** deve ser cadastrado no Service conforme demonstrado abaixo:

<center>
    <a>Imagem 3 - Cadastrando Product</a>
</center>

![Cadastro do Product Name](../assets/images/actionLocal/img_3.png)

> No caso do próprio MeasureSoftGram, o produto já se encontra previamente cadastrado, bastando apenas vincular o repositório e a release.

#### Repositório e Release

Também é necessário adicionar o repositório ao Service e vinculá-lo a uma release:

<center>
    <a>Imagem 4 - Crianção do repositório</a>
</center>

![Adicionando repositório](../assets/images/actionLocal/img_2.png)

<center>
    <a>Imagem 5 - Criação de release</a>
</center>

![Vinculando à release](../assets/images/actionLocal/img_4.png)

> Observação - quando for cadastrar um **Goal** é importante utilizar o json no seguinte formato:

```json
{
   "changes": [
      {
         "characteristic_key": "string",
         "delta": 0
      }
   ],
   "allow_dynamic": false
}
```

---

## Executando as Pipelines

Com tudo configurado, utilize os comandos do `Makefile` para compilar e executar as pipelines:

```bash
# Compila a Action e sobe os containers via Docker Compose
make build

# Executa uma pipeline específica (substitua [nome-da-pipeline] pelo nome desejado)
make action-[nome-da-pipeline]
```

> **Exemplo:** `make action-msgram` executaria a pipeline chamada `msgram.yml`.

## Formulario de Entrega da Release

Preencha o formulario de validacao da release neste link:

https://docs.google.com/forms/d/e/1FAIpQLSczE17X6JWlXLzCLAfMmKi0jpMGQuWmUxXdaS6dez6lL1OydQ/viewform?usp=publish-editor


## Versionamento

| Versao | Data       | Descricao                       | Autor                                    | Revisor |
|--------|------------|---------------------------------|------------------------------------------|---------|
| 1.0    | 12/04/2026 | Criação do documento            | [João Antonio](https://github.com/i-JSS) |     [Nicollas Gabriel](https://github.com/Nicollaxs)    |
| 1.1     | 13/04/2026 | Adicona JSON no cadastro de goal | [João Antonio](https://github.com/i-JSS)                                         |      [Nicollas Gabriel](https://github.com/Nicollaxs)    |
| 1.2     | 13/04/2026 | Adiciona formulário de entrega da release | [Nicollas Gabriel](https://github.com/Nicollaxs) |  |
| 1.3     | 16/06/2026 | Expande guia de obtenção do GitHub Token e adiciona configuração do OAuth App | [Nicollas Gabriel](https://github.com/Nicollaxs) |  |



