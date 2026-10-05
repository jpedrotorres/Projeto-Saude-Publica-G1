# Projeto-Saude-Publica-G1
## Análise de Indicadores de Saúde Pública no Brasil

Projeto acadêmico desenvolvido para a disciplina de **Linguagens de Programação**, com foco em análise exploratória de dados, tratamento e preparação de dados, visualização de informações e construção de um dashboard interativo utilizando Python e Streamlit.

O projeto utiliza uma base de dados simulada contendo indicadores relacionados à saúde pública no Brasil, abrangendo o período de **2015 a 2024**.

---

## 1. Identificação

**Discente:** João Pedro de Farias Torres de Souza
**Disciplina:** Linguagens de Programação
**Docente:** Alexandre Neves Louzada

---

## 2. Tema

### Análise de Indicadores de Saúde Pública no Brasil

Indicadores de saúde pública são importantes para acompanhar diferentes aspectos relacionados às condições de saúde da população e à estrutura dos serviços de saúde.

Neste projeto são analisados indicadores relacionados à mortalidade, internações, vacinação, expectativa de vida, doenças crônicas e infraestrutura hospitalar, permitindo observar sua distribuição e evolução nos diferentes recortes presentes na base de dados.

---

## 3. Objetivo

O objetivo do projeto é desenvolver uma aplicação de análise e visualização de dados capaz de investigar os indicadores de saúde pública presentes na base.

A análise busca:

* observar a evolução dos indicadores ao longo do tempo;
* comparar diferentes regiões brasileiras;
* comparar os estados presentes na base;
* identificar estados e regiões com maior criticidade;
* analisar a infraestrutura hospitalar;
* observar a evolução da expectativa de vida;
* investigar a relação entre cobertura vacinal e taxa de mortalidade;
* disponibilizar os resultados por meio de um dashboard interativo.

Esses objetivos estão alinhados às análises previstas para o tema de saúde pública.

---

## 4. Base de dados

O projeto utiliza o arquivo:

```text
simulacao_saude_publica_brasil.csv
```

A base contém dados simulados relacionados a indicadores de saúde pública no Brasil.

Entre as variáveis utilizadas estão:

| Variável                 | Descrição                                        |
| ------------------------ | ------------------------------------------------ |
| `ano`                    | Ano da medição                                   |
| `mes`                    | Mês da medição                                   |
| `data`                   | Data de referência                               |
| `regiao`                 | Região do Brasil                                 |
| `uf`                     | Estado                                           |
| `municipio`              | Município                                        |
| `expectativa_vida`       | Expectativa de vida                              |
| `taxa_mortalidade`       | Taxa de mortalidade                              |
| `taxa_internacao`        | Taxa de internação                               |
| `cobertura_vacinal`      | Percentual de vacinação                          |
| `medicos_por_1000`       | Quantidade de médicos                            |
| `leitos_hospitalares`    | Quantidade de leitos                             |
| `casos_doencas_cronicas` | Quantidade estimada de casos de doenças crônicas |
| `nivel_criticidade`      | Classificação em Baixo, Médio, Alto ou Crítico   |

A estrutura acima corresponde às variáveis indicadas na especificação do dataset do projeto.

---

## 5. Análise realizada

O projeto contempla as principais etapas de um processo de análise de dados:

1. Leitura da base de dados;
2. Inspeção e compreensão das variáveis;
3. Limpeza e preparação dos dados;
4. Engenharia de atributos;
5. Análise exploratória;
6. Cálculo dos KPIs;
7. Construção das visualizações;
8. Análise de correlação;
9. Interpretação dos resultados;
10. Conclusão.

Essa organização segue a estrutura definida para o notebook de análise do projeto.

---

## 6. KPIs

Os principais indicadores utilizados no projeto são:

| KPI                          | Descrição                                          |
| ---------------------------- | -------------------------------------------------- |
| Expectativa média de vida    | Indicador social relacionado à expectativa de vida |
| Taxa média de mortalidade    | Indicador epidemiológico                           |
| Cobertura vacinal média      | Indicador preventivo                               |
| Estado mais vulnerável       | Ranking relacionado à criticidade                  |
| Média de leitos hospitalares | Indicador de infraestrutura                        |
| Taxa média de internação     | Indicador relacionado às internações               |

Os KPIs foram definidos a partir dos indicadores esperados para o tema proposto.

> **Observação:** a base utilizada apresenta `taxa_internacao`. Portanto, a aplicação trabalha com a taxa média de internação, e não com um total absoluto de internações.

---

## 7. Visualizações

O dashboard apresenta diferentes visualizações para facilitar a interpretação dos dados.

### Evolução temporal

Permite observar o comportamento dos indicadores ao longo dos anos analisados.

### Comparação entre estados

Apresenta a taxa média de mortalidade por estado, permitindo identificar diferenças entre as unidades federativas.

### Infraestrutura hospitalar

Apresenta a média de leitos hospitalares por estado.

### Heatmap epidemiológico

Permite visualizar a distribuição da taxa média de mortalidade entre regiões e anos.

### Correlação

Apresenta uma matriz de correlação entre os principais indicadores numéricos.

Também é apresentada uma análise específica da relação entre:

```text
Cobertura vacinal × Taxa de mortalidade
```

por meio de gráfico de dispersão e coeficiente de correlação.

### Tabela dinâmica

Permite explorar detalhadamente os registros após a aplicação dos filtros.

Essas visualizações correspondem às visualizações previstas na especificação do projeto.

---

## 8. Dashboard Streamlit

O dashboard foi desenvolvido utilizando **Streamlit** e permite realizar análises interativas da base de dados.

### Filtros disponíveis

O usuário pode filtrar os dados por:

* ano;
* mês;
* região;
* estado;
* município;
* nível de criticidade.

Esses são os filtros definidos como obrigatórios para o dashboard do projeto.

### Funcionalidades

O dashboard disponibiliza:

* KPIs dinâmicos;
* filtros interativos;
* análise temporal;
* comparação entre regiões e estados;
* análise da infraestrutura hospitalar;
* heatmap epidemiológico;
* matriz de correlação;
* gráfico de dispersão;
* tabela dos dados filtrados;
* interpretação textual;
* conclusão executiva.

---

## 9. Persistência dos dados

Como funcionalidade adicional, o projeto utiliza **SQLite** para persistência dos dados.

A aplicação cria e utiliza a tabela:

```text
indicadores_saude
```

O acesso ao banco é realizado utilizando **SQLAlchemy**.

Além da persistência, o dashboard disponibiliza uma área para execução de consultas `SELECT` diretamente sobre a tabela armazenada no banco.

Essa funcionalidade utiliza uma das tecnologias recomendadas para funcionalidades avançadas do projeto: **SQLAlchemy + SQLite**.

---

## 10. Tecnologias utilizadas

### Obrigatórias

* **Python** — linguagem utilizada no desenvolvimento;
* **Pandas** — manipulação e análise dos dados;
* **Matplotlib** — construção das visualizações;
* **Seaborn** — visualizações estatísticas e heatmaps;
* **Streamlit** — desenvolvimento do dashboard;
* **GitHub** — versionamento e publicação do projeto.

Essas tecnologias fazem parte da relação de tecnologias obrigatórias definida para a atividade.

### Adicionais

* **SQLAlchemy** — conexão e interação com o banco;
* **SQLite** — persistência dos dados.

---

## 11. Estrutura do projeto

```text
projeto-saude-publica/
│
├── app.py
├── requirements.txt
├── README.md
├── index.html
│
├── dados/
│   └── simulacao_saude_publica_brasil.csv
│
├── notebooks/
│   └── analise_saude_publica.ipynb
│
└── database/
    └── saude_publica.sqlite
```

Essa organização segue a estrutura indicada para o projeto de saúde pública.

---

## 12. Como executar localmente

### 12.1 Clonar o repositório

```bash
git clone https://github.com/jpedrotorres/Projeto-Saude-Publica-G1
```

Entre na pasta do projeto:

```bash
cd projeto-saude-publica
```

### 12.2 Instalar as dependências

```bash
pip install -r requirements.txt
```

### 12.3 Executar o dashboard

```bash
streamlit run app.py
```

Após a execução, o Streamlit disponibilizará o endereço local para acesso ao dashboard.

### 12.4 Executar o notebook

O notebook pode ser aberto pelo Jupyter, VS Code ou Google Colab.
Obs.: Para uso no Colab, tomar cuidado na hora da importação do banco de dados utilizado, tendo em vista a diferença da estrutura de diretórios adotados no projeto e a utilizada pela ferramenta.

Arquivo:

```text
notebooks/analise_saude_publica.ipynb
```

---

## 13. Perguntas analisadas

A análise procura auxiliar na investigação das seguintes questões:

* Quais regiões apresentam maiores índices de mortalidade?
* Houve mudanças nos indicadores de saúde ao longo do período?
* Existem diferenças entre as regiões?
* Quais estados apresentam maiores taxas de internação?
* Qual é a relação observada entre cobertura vacinal e mortalidade?
* Como evoluiu a expectativa de vida?
* Quais indicadores apresentam maior criticidade?

Essas perguntas fazem parte das questões orientadoras definidas para o tema.

---

## 14. Interpretação

A análise dos indicadores permite observar diferenças entre os recortes territoriais e temporais presentes na base.

As visualizações possibilitam identificar comportamentos distintos entre regiões e estados, enquanto a análise temporal permite acompanhar a evolução dos indicadores durante o período estudado.

A matriz de correlação e o gráfico de dispersão permitem investigar relações lineares entre os indicadores. Entretanto, uma correlação observada entre duas variáveis não deve ser interpretada como evidência de causalidade.

As conclusões apresentadas no projeto são restritas aos dados disponibilizados para a análise.

---

## 15. Conclusão

O projeto transforma a base de dados simulada de indicadores de saúde pública em uma aplicação analítica interativa.

A utilização conjunta de Pandas, Matplotlib, Seaborn e Streamlit permite realizar o tratamento dos dados, produzir visualizações e disponibilizar os resultados de maneira interativa.

A inclusão de persistência em SQLite e consultas SQL amplia a aplicação para além da análise exploratória, permitindo demonstrar também a integração entre Python e banco de dados.

Por se tratar de uma base de dados simulada, os resultados obtidos representam exclusivamente o comportamento dos dados utilizados no projeto e não devem ser interpretados como estimativas oficiais da situação da saúde pública brasileira.

---

## 16. Publicação

O projeto deverá ser disponibilizado nas plataformas previstas para a atividade:

| Plataforma                | Finalidade                        |
| ------------------------- | --------------------------------- |
| GitHub                    | Código-fonte e documentação       |
| GitHub Pages              | Página de apresentação do projeto |
| Streamlit Community Cloud | Dashboard interativo              |

A atividade estabelece essas três plataformas como meios de publicação do projeto.

### Links

**Repositório GitHub:**
`https://github.com/jpedrotorres/Projeto-Saude-Publica-G1`

**GitHub Pages:**
`https://jpedrotorres.github.io/Projeto-Saude-Publica-G1/`

**Dashboard Streamlit:**
`https://projeto-saude-publica-g1.streamlit.app/`

---

## 17. Considerações finais

O projeto busca demonstrar não apenas a capacidade de gerar gráficos, mas principalmente a utilização de técnicas de análise de dados para compreender os indicadores disponíveis, comparar diferentes recortes e comunicar os resultados de maneira clara.

A estrutura foi desenvolvida considerando as etapas de preparação, análise, visualização, interpretação e disponibilização dos resultados em uma aplicação interativa.

