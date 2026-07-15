# Plano de Qualidade

## Introdução

<p align = "justify"> &emsp;&emsp; A qualidade de software diz respeito à capacidade de um software satisfazer as necessidades e expectativas dos usuários, apresentando código confiável e de fácil manutenção. </p>

<p align = "justify"> &emsp;&emsp; Neste documento, são apresentadas as ferramentas utilizadas para garantir a qualidade do projeto durante o seu desenvolvimento, além da análise de métricas para estabelecer critérios de qualidade. </p>

## Ferramentas

### SonarCloud

<p align = "justify"> &emsp;&emsp; O SonarCloud é uma ferramenta amplamente empregada para coletar métricas e indicadores técnicos, permitindo o monitoramento da qualidade do código. Durante o desenvolvimento do projeto, métricas foram capturadas após cada Pull Request submetido. Essas métricas foram combinadas para calcular os aspectos relevantes de qualidade do código, com foco na confiabilidade e manutenibilidade. Esses dados são cruciais para orientar o planejamento de melhorias contínuas, visando garantir um código confiável e de fácil manutenção. </p>

### Testes Unitários

<p align = "justify"> &emsp;&emsp; Os testes unitários são testes automatizados cujo objetivo é verificar o desempenho de partes isoladas de código em um sistema maior. </p>

#### Jest

<p align = "justify"> &emsp;&emsp; A equipe utilizou o Jest no frontend, uma ferramenta de código aberto, para realizar esses testes de forma simples e conveniente em aplicações JavaScript e Typescript. </p>

### ESLint

<p align = "justify"> &emsp;&emsp; O ESLint é uma ferramenta muito utilizada para fazer a verificação e análise estática de código JavaScript. Ela ajuda os desenvolvedores a garantir a qualidade do código, ao encontrar e relatar possíveis problemas, erros ou práticas inadequadas de programação. O ESLint disponibiliza várias regras configuráveis, que podem ser personalizadas de acordo com as necessidades do projeto, permitindo a aplicação de padrões de codificação consistentes e melhorando a legibilidade, a manutenibilidade e a interoperabilidade do código-fonte. </p>

### Verificação e validação

<p align = "justify"> &emsp;&emsp; Para garantir a qualidade do projeto, a equipe adotou as seguintes técnicas de verificação e validação: </p>

<p align = "justify"> &emsp;&emsp; Validações com os donos do produto: É essencial envolver os donos ou usuários do projeto na validação. Foram realizadas reuniões semanais com os POs para validar o progresso e obter feedback. Essa interação contínua ajuda a garantir que o software esteja sendo desenvolvido de acordo com as expectativas e necessidades dos stakeholders. </p>

<p align = "justify"> &emsp;&emsp; Inspeção contínua do código: A equipe optou por utilizar o Sonar Cloud como ferramenta de análise estática de código. Essa técnica permite obter métricas mensuráveis e identificar potenciais problemas no código-fonte. O Sonar Cloud fornece informações relevantes para a gestão da qualidade do projeto, auxiliando na tomada de decisões e na identificação de pontos que precisam ser aprimorados pela equipe. </p>

<p align = "justify"> &emsp;&emsp; Revisão de PRs: Foi implementada uma prática de verificação de correção de PRs. Antes de mesclar um PR no repositório principal, algum membro da equipe de EPS revisa o código, analisando a lógica, a qualidade, a conformidade com as diretrizes do projeto e identificando possíveis melhorias ou problemas. Essa verificação adicional ajuda a garantir que o código entregue esteja correto e atenda aos padrões de qualidade estabelecidos. </p>

## Métricas de qualidade

As métricas de qualidade definidas para o software são:

| Métrica          | Descrição                                     |
| ---------------- | --------------------------------------------- |
| Bugs             | Número de problemas identificados no código   |
| Coverage         | Grau de cobertura dos testes no código        |
| Duplicação       | Quantidade de linhas de código duplicadas     |
| Linhas           | Total de linhas de código no projeto          |
| Security Rating  | Avaliação de segurança e vulnerabilidades     |

<p align = "justify"> &emsp;&emsp; Através do uso de métricas, é possível identificar as subcaracterísticas relacionadas e avaliar a qualidade do produto. Essa avaliação fornece insights sobre a produtividade do projeto e influencia as decisões tomadas durante o desenvolvimento. Os valores mínimos aceitáveis para cada métrica do projeto foram estabelecidos com base nas métricas especificadas no SonarCloud. </p>

| Métrica           | Critério                         |
| ----------------- | -------------------------------- |
| Coverage          | Pelo menos 80% de cobertura      |
| Bugs              | Classificado como "A"            |
| Security Hotspots | Classificado como "A"            |
| Duplication       | Até 3.0% de duplicação de código |

## Referências
- Qualidade de Software. Disponível em: https://www.devmedia.com.br/qualidade-de-software-engenharia-de-software-29/18209. Acesso em 20 out. 2023

- ISO/IEC 25010. ISO 25000. Software and data quality. 2011. Disponível em: https://iso25000.com/index.php/en/iso-25000-standards/iso-25010. Acesso em 20 out. 2023

- ENGSOFTMODERNA. Engenharia de Software Moderna. Disponível em: https://engsoftmoderna.info/. Acesso em: 20 out. 2023.

## Versionamento

|Data|Autor|Descrição|Versão|
|:--:|:--:|:---:|:---:|