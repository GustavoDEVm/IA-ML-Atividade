# Random Forest aplicado às receitas federais dos Estados Unidos

Trabalho acadêmico de Inteligência Artificial e Machine Learning: prever receitas
por linha contábil e ano com RandomForestRegressor, comparando com persistência.
A entrega central é [notebooks/budget_random_forest.ipynb](notebooks/budget_random_forest.ipynb),
com fundamentação, análise exploratória, código, gráficos, métricas e conclusão.

## Identificação — preencher antes da entrega

| Campo | Identificação |
|---|---|
| Instituição | PUC-SP, conforme material; confirmar denominação |
| Disciplina | [PREENCHER — nome oficial] |
| Professor(a) | [PREENCHER] |
| Integrante 1 | [PREENCHER — nome e identificação acadêmica] |
| Integrante 2 | [PREENCHER — nome e identificação acadêmica] |
| Turma | [PREENCHER] |
| Data de entrega | [PREENCHER — dd/mm/aaaa] |

## Dataset e procedência

**Budget — U.S. federal receipts and estimates by account**, distribuído pelo
[Vega Datasets](https://vega.github.io/vega-datasets/datasets/budget/), release 3.2.1.
Arquivo local: [data/raw/budget.json](data/raw/budget.json), com 237 registros
e 72 campos. Os valores temporais chegam como texto com separadores de milhares.

Fonte primária: OMB, [Budget FY 2016 — Receipts, no GovInfo](https://www.govinfo.gov/app/details/BUDGET-2016-DB/BUDGET-2016-DB-3).
A documentação da edição está no [guia FY 2016](https://www.govinfo.gov/content/pkg/BUDGET-2016-DB/pdf/BUDGET-2016-DB-4.pdf).
A interpretação documental e os critérios do recorte estão na seção 17 do notebook.
A conversão retira vírgulas sem multiplicar ou dividir os montantes.

## Estrutura do projeto

~~~text
README.md
PUCSP_CS_AI_11_AI_ML_RandomForest.ipynb  # material original preservado
notebooks/
  budget_random_forest.ipynb           # trabalho completo, com saídas
  backups/                            # versões anteriores preservadas
data/
  raw/budget.json                      # dataset principal, sem edição
  metadata/vega_datapackage_3.2.1.json
  alternatives/                        # arquivos da comparação preliminar
reports/
  validacao_datasets.json              # registro da inspeção inicial
src/
  validar_datasets.py                  # inspeção inicial, sem modelagem
~~~

Os arquivos em reports e src documentam uma etapa anterior e podem mencionar
pendências então existentes. As decisões e os resultados finais estão no notebook.
O script auxiliar não é necessário para reproduzir o experimento.

## Ambiente e execução

Ambiente usado: Python 3.11.9, Pandas 2.3.3, NumPy 2.3.3, Matplotlib 3.11.2,
Seaborn 0.13.2, Scikit-learn 1.9.1 e ipykernel 7.3.0. A execução também utiliza
a biblioteca padrão do Python. Não depende de vega_datasets, missingno ou KaggleHub.

1. Obtenha o projeto mantendo a estrutura de diretórios, incluindo o JSON e
   o notebook original da disciplina, que é lido na verificação de integridade.
2. Abra a pasta raiz no VS Code com suporte a Jupyter, ou em um ambiente Jupyter.
3. Abra notebooks/budget_random_forest.ipynb e selecione o kernel Python com as
   bibliotecas indicadas.
4. Use **Restart Kernel and Run All** (reiniciar o kernel e executar todas as células).
5. Confira as tabelas de resultados e a auditoria na seção 29.

O carregamento aceita execução na raiz ou em notebooks. Não há caminhos absolutos
fixos, downloads nem instalações nas células. Se o JSON estiver ausente, uma mensagem
interrompe a execução. A tabela inicial registra versões para reprodução.
Não é necessário executar ou alterar o notebook original.

## Experimento

- Unidade: linha identificada por órgão + bureau + conta, em um ano fiscal.
- Alvo: receita realizada dessa linha, em milhares de US$.
- Histórico elegível: 1982–2014; TQ e estimativas de 2015–2020 excluídos.
- Atributos: receitas t−1, t−2 e t−3, ano-alvo e categorias, com identidade explícita.
- Treino: 1985–2009, 5.925 observações.
- Teste: 2010–2014, 1.185 observações das mesmas 237 séries.
- Horizonte: um ano à frente, com atualização de valores passados observados
  e modelo fixo, sem reajuste nos anos de teste.
- Baseline: receita do ano anterior.
- Floresta: 300 árvores, max_depth=12, min_samples_leaf=2,
  max_features=1.0, bootstrap=True, random_state=42 e n_jobs=1.
- Pré-processamento: OneHotEncoder ajustado apenas no treino; códigos não são magnitudes.
  Sem otimização de hiperparâmetros pelo teste.

## Resultados

MAE e RMSE em **milhares de US$**, por linha/ano; R² sem unidade.
Valores arredondados para apresentação. Não são percentuais nem erros de um total nacional.

| Modelo | MAE | RMSE | R² |
|---|---:|---:|---:|
| Random Forest | 1.684.677,20 | 16.167.814,67 | 0,964546 |
| Persistência | 1.100.199,16 | 9.419.991,44 | 0,987965 |

Nesta configuração, Random Forest apresentou MAE **53,12% maior** e RMSE
**71,63% maior** que persistência. Portanto, não houve ganho preditivo global
frente ao baseline. R² alto não altera essa comparação e não mede percentual
de acerto. A conclusão não estabelece inferioridade universal do algoritmo.

A revisão final executa as 27 células de código em kernel novo e confere
defasagens por chave/ano, escala monetária e métricas com fórmulas independentes.
O notebook conserva tabelas e gráficos da execução; não usa métricas fictícias.

## Limitações

A análise é retrospectiva: a edição reclassifica o histórico, e sua identidade
contábil pode não refletir informação disponível em cada data passada. Sobreposição
e continuidade econômica de contas não foram reconciliadas. Não se somam receitas.

Muitos zeros e grandes diferenças de escala tornam as métricas agregadas
sensíveis a extremos. Séries e anos são dependentes; 1.185 linhas de teste
representam apenas cinco anos. Não há avaliação para contas inéditas nem
previsão recursiva de cinco passos. As explicações sobre extrapolação e persistência
são hipóteses plausíveis, não causas isoladas demonstradas.

## Publicação no GitHub e entrega no MS Teams

1. Preencha os campos de identificação no notebook e neste README.
2. Revise a conclusão e confirme que o notebook abre com os gráficos e as tabelas.
3. Crie um repositório no GitHub com a visibilidade exigida pela disciplina.
4. Use **Add file → Upload files**, preservando as pastas. Inclua pelo menos
   README.md, notebooks/budget_random_forest.ipynb, data/raw/budget.json e
   PUCSP_CS_AI_11_AI_ML_RandomForest.ipynb. Mantenha backups locais; eles não são
   necessários para executar a versão entregue.
5. Confirme o envio em **Commit changes**. Abra o notebook no repositório e copie
   o endereço da página dele, no formato
   https://github.com/USUARIO/REPOSITORIO/blob/BRANCH/notebooks/budget_random_forest.ipynb.
6. Confirme que o professor tem acesso ao repositório; em um repositório público,
   verifique também o link em uma janela sem autenticação.
7. Abra a atividade correspondente no MS Teams, cole o link do notebook no campo
   de entrega indicado pelo professor e finalize em **Entregar**. Confira o status
   de envio apresentado pela atividade.

Referência para o envio de arquivos:
[GitHub Docs — adicionar arquivos a um repositório](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).
Os controles do Teams dependem de como a atividade foi configurada.
Esta revisão prepara os arquivos; não cria repositório nem envia a atividade.

## Referências técnicas

- [Scikit-learn — árvores de decisão](https://scikit-learn.org/stable/modules/tree.html).
- [Scikit-learn — florestas e ensembles](https://scikit-learn.org/stable/modules/ensemble.html#forest).
- [Scikit-learn — documentação](https://scikit-learn.org/stable/).

A bibliografia completa e a distinção entre fonte dos dados e documentação do
algoritmo estão na seção 30 do notebook.
