# Metodologia Spotify

## Descrição da Metodologia

A **Metodologia Spotify** é um modelo de organização ágil criado e adotado pela empresa Spotify para escalar o desenvolvimento de software mantendo agilidade, autonomia e alinhamento entre as equipes. Ela é amplamente utilizada em projetos que exigem colaboração entre múltiplos times com diferentes especialidades [[1]](#referências-bibliográficas).

Seus principais pilares são:

- **Squads**: Times pequenos, autônomos e multidisciplinares responsáveis por uma funcionalidade ou área específica do produto. Funcionam como mini-startups dentro do projeto.
- **Tribos (Tribes)**: Agrupamento de Squads que trabalham em áreas relacionadas. Compartilham contexto e objetivos estratégicos.
- **Chapters**: Grupos de pessoas com habilidades semelhantes distribuídas em diferentes Squads (ex: todos os desenvolvedores front-end). Garantem alinhamento técnico e boas práticas.
- **Guildas (Guilds)**: Comunidades de interesse transversais, voluntárias, que compartilham conhecimento entre pessoas de diferentes Squads e Tribes.

No contexto deste projeto, adaptamos a metodologia utilizando o conceito de **Clãs** no lugar de Tribes/Squads, organizando as equipes com base na **arquitetura do produto**, conforme descrito a seguir [[1]](#referências-bibliográficas).

---

## Divisão de Clãs

A divisão foi realizada em **3 clãs principais**, a escolha foi realizada principalmente com base na arquitetura do produto, visando uma melhor organização e especialização das equipes. Conforme a figura a seguir:

![Diagrama Arquitetural](../assets/images/diagrama_arquitetura.png)

Cada clã é responsável por uma camada da arquitetura e possui um **líder** responsável pela coordenação interna. Além disso, os integrantes são alocados em repositórios conforme sua função dentro do clã.

A tabela abaixo apresenta a distribuição dos membros por **função técnica** (Chapter) dentro de cada Clã:

| Clã        | Actions                           | CLI                 | Core / Parser          | Service                | Front                           |
|------------|-----------------------------------|---------------------|------------------------|------------------------|---------------------------------|
| **Action** | • Guilherme<br>• **João Antonio** | —                   | —                      | • Nicollas<br>• Márcio | —                               |
| **CLI**    | —                                 | • **Murilo<br>**| • João Pedro<br> | —                      | —                               |
| **Web**    | —                                 | —                   | • Giovanni             | • Danilo<br>• **Luis** | • Raquel<br>• Luciano<br>• Davi |

---

## Clã Action

O **Clã Action** é responsável pela camada de **ações e serviços de negócio** da aplicação.

**Líder:** [João Antonio Ginuino Carvalho](https://github.com/i-JSS)

### Membros

| Membro                               | Função          | GitHub                                       |
|--------------------------------------|-----------------|----------------------------------------------|
| João Antonio Ginuino Carvalho        | Líder / Actions | [@i-JSS](https://github.com/i-JSS)           |
| Guilherme Aguera de la Fuente Vilela | Actions         | [@guivilela7](https://github.com/guivilela7) |
| Márcio Henrique de Sousa Costa       | Service         | [@DeM4rcio](https://github.com/DeM4rcio)     |
| Nicollas Gabriel Oliveira Sousa      | Service         | [@nicollaxs](https://github.com/nicollaxs)   |

### Cerimônias da equipe

| Reunião                     | Frequência | Meio    | Dia           | Horário        |
|-----------------------------|------------|---------|---------------|----------------|
| Review e Planning da sprint | Semanal    | Discord | Segunda-Feira | 20:00 às 21:00 |

---

## Clã CLI

O **Clã CLI** é responsável pela interface de linha de comando do projeto, além do desenvolvimento dos módulos de **Core** e **Parser**.

**Líder:** [Murilo Perazzo Barbosa Souto ](https://github.com/murilopbs)

### Membros

| Membro                               | Função        | GitHub                                         |
|--------------------------------------|---------------|------------------------------------------------|
| Murilo Perazzo Barbosa Souto         | Líder / CLI            | [@murilopbs](https://github.com/murilopbs)     |
| João Pedro Anacleto Ferreira Machado | Core / Parser | [@jpanacleto2](https://github.com/jpanacleto2) |

### Cerimônias da equipe

| Reunião                     | Frequência | Meio    | Dia | Horário |
|-----------------------------|------------|---------|-----|---------|
| Review e Planning da sprint | Semanal    | Discord | -   | -       |

---

## Clã Web

O **Clã Web** é o maior clã e é responsável pela camada de **apresentação e serviços web** do produto. Cobre desde o desenvolvimento front-end até os serviços de back-end web e módulos de Core/Parser da camada web.

**Líder:** [Luis Henrique Luz Costa](https://github.com/luishenrrique)

### Membros

| Membro                              | Função          | GitHub                                                           |
|-------------------------------------|-----------------|------------------------------------------------------------------|
| Luis Henrique Luz Costa             | Líder / Service | [@luishenrrique](https://github.com/luishenrrique)               |
| Danilo Naves do Nascimento          | Service         | [@DaniloNavesS](https://github.com/DaniloNavesS)                 |
| Giovanni Alvissus Camargo Giampauli | Core / Parser   | [@giovanniacg](https://github.com/giovanniacg)                   |
| Davi Gonçalves Akegawa Pierre       | Front           | [@DaviPierre](https://github.com/DaviPierre)                     |
| Luciano de Freitas Melo             | Front           | [@luciano-freitas-melo](https://github.com/luciano-freitas-melo) |
| Raquel Ferreira Andrade             | Front           | [@raquel-andrade](https://github.com/raquel-andrade)             |

### Cerimônias da equipe

| Reunião                     | Frequência | Meio    | Dia            | Horário        |
|-----------------------------|------------|---------|----------------|----------------|
| Review e Planning da sprint | Semanal    | Discord | Quarta-Feira   | 10:00 às 11:00 |

---

## Heatmap

<div align="justify">&emsp;&emsp;
Um HeatMap, ou mapa de calor, é uma ferramenta visual poderosa utilizada em diversas áreas, incluindo gestão de projetos, para representar dados de forma intuitiva e compreensível. Quando aplicado ao contexto dos horários disponíveis de uma equipe, o HeatMap oferece uma visão abrangente e instantânea das horas mais propícias para a realização de atividades, reuniões ou distribuição de tarefas ao longo do dia.
</div>

<div align="justify">&emsp;&emsp;
A importância do HeatMap em um projeto reside na sua capacidade de otimizar o tempo e recursos da equipe, permitindo uma alocação mais eficiente de trabalho de acordo com a disponibilidade de cada membro. Ao identificar visualmente os períodos de pico de atividade e os momentos de menor ocupação, o HeatMap possibilita uma melhor coordenação entre os membros da equipe, minimizando conflitos de agenda e maximizando a produtividade.
</div>

<div align="justify">&emsp;&emsp;
O mapa de calor da equipe pode ser visualizada abaixo:
</div>

<iframe
src="https://www.when2meet.com/?35721943-XFxke"
width="100%"
height="600px">
</iframe>

---

## Referências Bibliográficas
> [1] Atlassian (2026) Conheça o modelo do Spotify, Atlassian.com. Atlassian. Disponível em: https://www.atlassian.com/br/agile/agile-at-scale/spotify (Acesso em: 16 de abril de 2026).

## Histórico de Versão

| Versão | Data       | Descrição                              | Autor                                            | Revisor |
|--------|------------|----------------------------------------|--------------------------------------------------|---------|
| 1.0    | 16/04/2026 | Criação do Documento                   | [João Antonio](https://github.com/i-JSS)         |         |
| 1.1    | 16/04/2026 | Detalhamento dos Clãs e membros        | [João Antonio](https://github.com/i-JSS)         |         |
| 1.2    | 26/04/2026 | Review e Planning da sprint do Clã WEB | [Luis Henrique](https://github.com/luishenrrique)|         |