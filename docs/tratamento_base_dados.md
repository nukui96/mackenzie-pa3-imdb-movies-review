# Registro de tratamento e preparação dos dados

Este documento registra cada regra aplicada ao catálogo, o motivo e o efeito nas contagens. As regras estão implementadas em `src/preparo.py` e executadas em `notebooks/02_exploracao-e-preparacao.ipynb` (execução de 2026-10-02).

O arquivo preparado é uma nova versão para análise; o CSV original permanece disponível. `film_id` é o número da linha usado para distinguir filmes com o mesmo título. Na tabela abaixo, “ausente” significa que o arquivo não informa um valor: não significa zero.

- **Fonte:** `data/raw/imdb_top_1000.csv` (IMDb Top 1000, Kaggle, Harshit Shankhdhar). O arquivo bruto é imutável e não é alterado por nenhum notebook.
- **Saída:** `data/processed/filmes_preparados.csv` (1000 linhas, 18 colunas).

## Perfil do bruto (observado)

| Item | Resultado |
|---|---|
| Linhas / colunas | 1000 / 16 |
| Títulos distintos | 999 (*Drishyam* 2013 e 2015 são filmes distintos: diretores e sinopses diferentes) |
| Linhas totalmente duplicadas | 0 |
| Sinopses repetidas | 0 |
| Ausentes | `Certificate` 101; `Meta_score` 157; `Gross` 169 |
| `Released_Year` não numérico | 1 (`PG`, linha de *Apollo 13*, `film_id` 966) |
| `Runtime` no formato "N min" | 1000 de 1000 |
| `Gross` com vírgulas de milhar | 831 preenchidos, todos no formato esperado |
| Gêneros por filme | 1 gênero: 105; 2: 249; 3: 646; 21 gêneros distintos; Drama em 724 filmes |
| Sinopse (palavras) | mín 8; mediana 24; média 25,0; máx 56 |

## Regras

| Regra | Cenário observado | Regra aplicada e justificativa | Contagem (antes / depois) | Impacto no recomendador |
|---|---|---|---|---|
| R0 | Dados brutos | Não modificar `data/raw/`; o processado é derivado. | n/a | Rastreabilidade. |
| R1 | Títulos não são únicos | Criar `film_id` = posição (0-based) da linha no bruto. | 1000 / 1000 | Consultas e métricas por id, não por título. |
| R2 | Textos com possível espaço sobrando | `strip` e colapso de espaços internos em título, sinopse, gênero, diretor e elenco. | 1000 / 1000 | Efeito mínimo: 1 sinopse tinha espaços duplicados; sem mudança de conteúdo. |
| R3 | `Released_Year` = "PG" em 1 linha | Converter para inteiro; o valor não numérico vira ausente, sem acrescentar um ano de outra fonte. | 1 valor inválido no bruto / 1 ausente no preparado | Ano só serve de desempate; ausente fica por último. |
| R4 | `Runtime` como "142 min" | Extrair inteiro em `Runtime_min`; coluna original substituída. | 1000 / 1000 | Nenhum (não usado no modelo). |
| R5 | `Gross` com vírgulas; 169 ausentes | Converter para inteiro `Gross_usd`; ausente continua ausente (**não é zero**); 0 zeros criados. | ausentes 169 / 169 | Nenhum (não usado no modelo). |
| R6 | `Certificate` (101) e `Meta_score` (157) ausentes | Manter ausentes, sem preenchimento. | 101 / 101 e 157 / 157 | Nenhum (não usados no modelo). |
| R7 | Sinopse | Acrescentar `Overview_chars` e `Overview_words` (descritivas). | colunas +2 | Nenhum. |
| R8 | Duplicatas | Nenhuma linha removida: sem duplicatas exatas, homônimos são filmes distintos, sinopses todas preenchidas. | 1000 / 1000 | Catálogo completo. |
| R9 | `Poster_Link` | Não levada ao processado (não é atributo do modelo); permanece no bruto. | colunas -1 | Nenhum. |

Contagem de colunas: 16 no bruto, menos 3 (`Poster_Link`, `Runtime`, `Gross`), mais 5 (`film_id`, `Runtime_min`, `Gross_usd`, `Overview_chars`, `Overview_words`) = 18 no processado.

## Reconciliação executada

O notebook relê o CSV bruto e o preparado do disco para conferir se a preparação preservou os dados que deveriam permanecer iguais. As duas versões têm 1.000 linhas e 999 títulos distintos. Permanecem 101 ausências em `Certificate`, 157 em `Meta_score` e 169 em `Gross`/`Gross_usd`. O valor inválido de `Released_Year` tornou-se uma ausência. A soma de `No_of_Votes` permanece em 273.692.911, e nenhum zero foi criado em `Gross_usd`. Os valores de bilheteria, duração, título e gênero também foram comparados linha a linha. Os detalhes estão em `reports/metrics/reconciliacao_preparo.csv` e `reports/metrics/perfil_base.json`.

## Decisões deliberadamente não tomadas

- A sinopse **não** foi lematizada, nem teve stop words removidas na preparação: o vetorizador (TF-IDF, notebook 03) faz minúsculas e remove stop words em inglês, mantendo o texto do catálogo legível.
- Não há tratamento de outliers: nenhuma variável numérica entra no modelo da etapa 2.
- O ano de *Apollo 13* não foi corrigido por conhecimento externo, porque não há fonte registrada neste projeto para isso.
