## Índice Rápido

| # | Tipo | Título | Data |
| --- | --- | --- | --- |
| Nº1| Planning | Mudança de Escopo e problemas no Web | 01/06/2026 |

---

### Nº1 — Mudança de Escopo e problemas no Web

| Campo | Detalhe |
| --- | --- |
| **Data** | 01 de junho de 2026 |
| **Horário** | 11:50 – 13:30 |
| **Local** | Presencial (em sala) |
| **Sprint** | Sprint 01/06 - 08/06 |

**Participantes**

- **Danilo** — Service
- **Guilherme** — Actions
- **João Antonio** — Actions
- **Luciano** — Front
- **Murilo** — CLI
- **Raquel** — Front

**Pauta**

- Acúmulo de issues abertas e foco em documentação (com destaque para o quadro de riscos).
- Validação e ampliação do escopo da US de Autenticação via GitHub.
- Refatoração dos dashboards e uso de dados *mockados* na US do Grafana.
- Realocação de membros entre os clãs e encerramento do clã CLI.
- Negociação de redução de escopo do projeto junto ao PO.

**Resumo da Reunião**
A reunião de planejamento teve como foco organizar as demandas da nova Sprint e destravar issues que vêm sendo acumuladas por dependerem de outras tarefas. Foi enfatizada a necessidade de focar nas documentações pendentes, principalmente no quadro de riscos. Constatou-se que as User Stories do clã Web (Autenticação GitHub e Grafana) tiveram um aumento significativo de escopo devido à necessidade de refatorações críticas no service, banco de dados e rotas do frontend. Para viabilizar a entrega técnica, a equipe definiu estratégias de contorno (como uso de mocks), decidiu pela extinção do clã CLI no fim desta sprint para reforçar o clã Web, reorganizou os membros e decidiu propor uma redução de escopo ao PO no próximo encontro.

**O que foi discutido**

- **Issues Abertas e Documentação:** Foram apontadas várias issues de documentação que estão sendo deixadas em aberto. O DLD necessita da resolução prévia da US de Autenticação pelo GitHub para avançar. Houve consenso sobre a necessidade de dar foco urgente às documentações pendentes, principalmente em relação ao quadro de riscos.
- **Autenticação pelo GitHub:** Foi comunicado que há bugs nas rotas de autenticação do frontend. O planejamento desta US será validado com o professor. A resolução de um problema crítico na geração de gráficos (falha do service com o banco de dados) foi incorporada a esta US, o que aumentará seu escopo, englobando também a refatoração do código atual, mudanças no fluxo de releases e no login do usuário.
- **US do Grafana:** A demanda cresceu além do previsto, exigindo a refatoração de toda a área de dashboards. Devido aos problemas atuais do banco de dados/service, decidiu-se que o desenvolvimento inicial usará um *mock* de dados até que a US de Autenticação resolva a estabilidade do fluxo de dados.
- **Redução de Escopo:** Em virtude do aumento das atividades no clã Web, a equipe discutiu a necessidade de acertar com o PO (na reunião de quarta-feira) uma redução no escopo geral do projeto, permitindo foco nas USs críticas.
- **Realocação e Fim do Clã CLI:** O clã CLI vai encerrar suas atividades no final da sprint (07/06), e todos os seus membros serão realocados para auxiliar no clã Web. Durante esta sprint de transição, Giovanni passa para o clã CLI, enquanto Anacleto, Márcio e Nicollas (os dois últimos do clã Action) já integram o clã Web.

**Decisões Tomadas**

- Foco prioritário na resolução e atualização das issues de documentação, com atenção especial ao quadro de riscos.
- O clã CLI será encerrado no dia 07/06, e seus membros migrarão permanentemente para o clã Web.
- O planejamento da implementação da Autenticação via GitHub será validado diretamente com o professor.
- A correção dos problemas de banco de dados e service será feita conjuntamente na US de Autenticação, não de forma isolada.
- A US do Grafana será construída provisoriamente com *mock* de dados para não bloquear o desenvolvimento visual e de arquitetura.
- Uma proposta de redução de escopo será formalmente apresentada ao PO na quarta-feira.

**Ações e Reponsáveis**

| Ação | Responsável | Prazo | Status |
| --- | --- | --- | --- |
| Lidar com pull request de usuário, resolver questão do PyPi e bugs | Clã CLI | 07/06/2026 | A fazer |
| Atualizar quadro de riscos e resolver issues de documentação pendentes | Equipe | Durante a sprint | A fazer |
| Desenvolvimento do Plugin | Clã Action | 08/06/2026 | A fazer |
| Terminar planejamento, escrita das US de Autenticação GitHub e dividir tarefas | Clã Web | 03/06/2026 | A fazer |
| Criar protótipo do dashboard e planejar arquitetura/configuração da US do Grafana | Clã Web | 03/06/2026 | A fazer |
| Negociar redução de escopo com o PO | Equipe | 03/06/2026 | A fazer |
| Iniciar desenvolvimento das tarefas das US (Autenticação e Grafana) | Clã Web | 08/06/2026 | A fazer |

---