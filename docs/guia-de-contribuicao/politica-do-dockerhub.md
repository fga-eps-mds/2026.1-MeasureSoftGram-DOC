# Política de _Tags_ no Docker Hub

Esta política define os padrões de _tagging_ de imagens Docker no Docker Hub do projeto MeasureSoftGram, visando profissionalizar e sistematizar o processo de deploy, diferenciando ambientes de homologação e produção.

---

## Estrutura das _Tags_

Cada imagem publicada no Docker Hub deve seguir o padrão de tags abaixo, aplicado a **todos** os repositórios do projeto (ex: `measuresoftgram/AI`, `measuresoftgram/service`, etc.):

```
<repositório>:homolog   → versão em homologação/validação pelo P.O.
<repositório>:latest    → versão mais recente aprovada em produção
<repositório>:vX.Y.Z    → versão fixa e imutável para rastreabilidade
```

### Exemplo

```
measuresoftgram/ai:homolog   → aguardando validação do P.O.
measuresoftgram/ai:latest    → última versão estável em produção
measuresoftgram/ai:v1.2.3    → versão fixa para rastreabilidade
```

---

## Descrição das _Tags_

### `homolog`

- Representa a versão candidata a produção, aguardando **aceitação formal do P.O.**
- É a tag padrão para toda nova versão gerada pela pipeline de CD antes da validação.
- **Nenhuma imagem deve ir direto para `latest` sem antes passar pela tag `homolog`.**

### `latest`

- Representa a versão mais recente **aprovada e estável em produção**.
- Só deve ser atualizada **após aceitação explícita do P.O.**
- Deve ser rigorosamente testada antes de ser disponibilizada.

### `vX.Y.Z`

- Tag imutável que representa uma versão específica do software.
- Segue o padrão [Semantic Versioning](https://semver.org/): `vMAJOR.MINOR.PATCH`.
- Utilizada para rastreabilidade, rollback e referência em ambientes controlados.
- Nunca deve ser sobrescrita após publicada.

---

## Fluxo de Promoção de Versões

```
Build/CI → :homolog → (Validação P.O.) → :latest + :vX.Y.Z
```

1. A pipeline de CD gera a imagem e publica com a tag `:homolog`.
2. O P.O. valida a versão em homologação.
3. Após aprovação, o time publica manualmente a imagem com as tags `:latest` e `:vX.Y.Z` correspondente.
4. A tag `:homolog` passa a apontar para a próxima versão candidata.

---

## Responsabilidades

- **Time de desenvolvimento**: manter as pipelines de CD configuradas para publicar automaticamente em `:homolog` a cada nova versão.
- **P.O.**: validar e aprovar formalmente a promoção de `:homolog` para `:latest`.

---

## Pipelines de CD

As pipelines de CD devem ser configuradas para:

1. Publicar automaticamente em `:homolog` a cada merge na branch principal.
2. Publicar em `:latest` e criar a tag `:vX.Y.Z` somente mediante aprovação formal do P.O.

---

## Histórico de Versão

| Versão | Data       | Descrição                              | Autor                                    | Revisor |
|--------|------------|----------------------------------------|------------------------------------------|---------|
| 1.0    | 25/05/2026 | Criação da política de tags Docker Hub | [João Antonio](https://github.com/i-JSS) |         |