🏥 Projeto de Análise e Proteção de Dados de Saúde
📌 Sobre o projeto

Este projeto apresenta um sistema desenvolvido em Python para demonstrar técnicas de geração, proteção e análise de dados relacionados à área da saúde.

O sistema utiliza dados 100% sintéticos e fictícios, não correspondendo a pacientes reais.

O objetivo é demonstrar um fluxo completo de tratamento de dados:

Geração dos dados
       ↓
Proteção dos dados
       ↓
Anonimização / Generalização
       ↓
Análise estatística
       ↓
Identificação de padrões
       ↓
Pseudoanálise
       ↓
Relatório e gráficos

🎯 Objetivos

O projeto possui os seguintes objetivos:

Demonstrar a utilização de Python para análise de dados.
Trabalhar com dados sensíveis de forma segura em ambiente acadêmico.
Demonstrar técnicas de desidentificação e generalização.
Calcular estatísticas descritivas.
Identificar padrões e possíveis relações entre variáveis.
Demonstrar o uso de ruído Laplace em estatísticas agregadas.
Gerar uma pseudoanálise baseada nos padrões encontrados.
Produzir relatórios e gráficos automaticamente.
🔐 Privacidade e proteção dos dados

Os dados deste projeto são sintéticos.

Nenhuma informação de paciente real é utilizada.

O sistema demonstra algumas técnicas de proteção:

Remoção de identificadores

O identificador individual dos registros não é utilizado na base protegida.

Exemplo:

ID: P0001


é removido antes da disponibilização da base protegida.

Generalização da idade

Em vez de utilizar:

67 anos


o sistema pode utilizar:

60-69


Isso reduz a precisão da informação individual.

Generalização de valores

Algumas variáveis numéricas também são arredondadas.

Exemplo:

IMC: 31.4


pode ser transformado em:

31


e:

Glicemia: 118


pode ser transformada em:

120

Ruído estatístico

O sistema também demonstra a aplicação de ruído Laplace sobre algumas estatísticas agregadas.

O projeto utiliza, para fins didáticos:

EPSILON = 1.0


Esse parâmetro é utilizado para demonstrar o conceito de privacidade diferencial.

⚠️ O valor de epsilon utilizado neste projeto é didático e não deve ser considerado uma configuração adequada para um sistema de produção.

📊 Dados utilizados

O sistema gera automaticamente 1.000 registros sintéticos.

As variáveis utilizadas incluem:

Variável	Descrição
ID	Identificador sintético
Idade	Idade fictícia
Sexo	Sexo do registro
Diagnóstico	Diagnóstico fictício
Pressão sistólica	Pressão arterial sistólica
Pressão diastólica	Pressão arterial diastólica
Glicemia	Valor sintético de glicemia
IMC	Índice de massa corporal
Internações	Quantidade sintética de internações
Risco	Classificação sintética de risco

Os diagnósticos utilizados são:

Nenhum
Hipertensão
Diabetes tipo 2
Asma
Hipotireoidismo
📈 Análise estatística

O sistema realiza diversas análises.

Entre elas:

média;
mediana;
variância;
desvio padrão;
mínimo;
máximo;
frequência;
percentual;
correlação;
análise por diagnóstico;
análise de risco.

Também são calculadas estatísticas específicas para diferentes grupos.

Exemplo:

Diagnóstico: Diabetes tipo 2

Quantidade: 200
Glicemia média: 170
IMC médio: 29
Pressão sistólica média: 130

🤖 Pseudoanálise

Além da análise estatística, o projeto possui um módulo de pseudoanálise.

A pseudoanálise procura padrões aparentes nos dados e transforma esses padrões em hipóteses.

Exemplo:

OBSERVAÇÃO:

O grupo com diabetes apresentou glicemia média
maior que os demais grupos.

HIPÓTESE:

Pode existir uma associação entre diabetes e
valores elevados de glicemia.

CONFIANÇA:

Média.


A pseudoanálise não deve ser interpretada como diagnóstico médico ou prova de causalidade.

Ela serve para demonstrar como um sistema pode transformar resultados estatísticos em possíveis interpretações que posteriormente precisam ser investigadas.

📊 Gráficos

O sistema gera automaticamente gráficos dos dados.

São gerados:

diagnosticos.png
risco.png
glicemia.png
imc.png


Os gráficos ficam dentro da pasta:

resultados/

📁 Estrutura do projeto
projeto/
│
├── ambiente_saude/
│
├── dados/
│   └── pacientes_sinteticos.csv
│
├── resultados/
│   ├── dados_protegidos.csv
│   ├── relatorio.txt
│   ├── diagnosticos.png
│   ├── risco.png
│   ├── glicemia.png
│   └── imc.png
│
├── main.py
├── requirements.txt
└── README.md

🛠️ Tecnologias utilizadas

O projeto foi desenvolvido utilizando:

Python 3.10
NumPy
Pandas
Matplotlib
💻 Instalação
1. Criar o ambiente virtual

No PowerShell:

C:\Python310\python.exe -m venv ambiente_saude

2. Instalar as dependências

Execute:

.\ambiente_saude\Scripts\python.exe -m pip install numpy pandas matplotlib

▶️ Executando o projeto

Entre na pasta do projeto:

cd "C:\Users\FATEC ZONA LESTE\Downloads\projeto"


Execute:

.\ambiente_saude\Scripts\python.exe main.py


Não é necessário ativar o ambiente virtual.

📄 Resultados

Após a execução, o sistema criará automaticamente:

dados/pacientes_sinteticos.csv


Esse arquivo contém os dados sintéticos originais.

Também será criado:

resultados/dados_protegidos.csv


Esse arquivo contém a versão tratada/generalizada.

O relatório completo será salvo em:

resultados/relatorio.txt


E os gráficos em:

resultados/

🔎 Fluxo do sistema

O funcionamento geral pode ser representado por:

                 ┌─────────────────────┐
                 │ Dados sintéticos    │
                 │     de saúde        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Proteção dos dados  │
                 │                     │
                 │ • Remoção de ID     │
                 │ • Generalização     │
                 │ • Arredondamento    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Análise estatística │
                 │                     │
                 │ • Média             │
                 │ • Mediana           │
                 │ • Variância         │
                 │ • Correlação        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Pseudoanálise    │
                 │                     │
                 │ • Padrões           │
                 │ • Hipóteses         │
                 │ • Interpretações    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      Relatório      │
                 │                     │
                 │ • TXT               │
                 │ • CSV               │
                 │ • Gráficos          │
                 └─────────────────────┘

⚠️ Limitações

Este projeto possui finalidade educacional e demonstrativa.

Os resultados não devem ser utilizados para:

diagnóstico médico;
tratamento de pacientes;
decisões clínicas;
identificação de indivíduos;
pesquisas clínicas reais;
tomada de decisão em saúde.

Os dados são artificiais e foram criados exclusivamente para demonstrar técnicas de programação e análise de dados.

A remoção de identificadores ou a generalização de dados não deve ser interpretada como garantia absoluta de anonimização.

Uma implementação real exigiria uma avaliação formal de risco, modelo de ameaça, definição adequada do orçamento de privacidade e análise do contexto de utilização.

🎓 Finalidade acadêmica

O projeto pode ser utilizado como base para estudos relacionados a:

Ciência de Dados;
Engenharia de Dados;
Inteligência Artificial;
Segurança da Informação;
Privacidade de Dados;
LGPD;
Estatística;
Python;
Saúde Digital;
Análise de Dados.
🚀 Possíveis melhorias

Como evolução do projeto, podem ser adicionados:

interface gráfica;
dashboard interativo;
banco de dados SQLite;
importação de arquivos CSV;
exportação para Excel;
gráficos interativos;
algoritmo de k-anonimato;
cálculo de risco de reidentificação;
privacidade diferencial mais rigorosa;
comparação entre dados originais e protegidos;
testes automatizados;
API REST;
sistema de autenticação;
geração automática de PDF.
👨‍💻 Execução rápida

Se o ambiente virtual já estiver criado e as bibliotecas instaladas, basta:

.\ambiente_saude\Scripts\python.exe main.py


Depois confira:

resultados/


e abra:

relatorio.txt

📌 Resumo

Este projeto demonstra um pipeline completo para trabalhar com dados sintéticos de saúde:

GERAR
  ↓
PROTEGER
  ↓
ANALISAR
  ↓
PSEUDOANALISAR
  ↓
VISUALIZAR
  ↓
GERAR RELATÓRIO


Projeto desenvolvido para fins acadêmicos e educacionais.
