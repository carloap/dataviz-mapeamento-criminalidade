# DataViz Team - Mapeamento de Criminalidade no Ceará

Nossa missão é tratar dos problemas relacionados à crimes por arma de fogo, roubos e homicídios no estado do Ceará, para melhorar a eficiência de serviços de segurança, policiamento e vigilância, e manter a ordem sob controle.

## Objetivos e resultados chave

Vamos ajudar na tomada de decisão para a resolução de problemas de criminalidade no estado do Ceará.

Inicialmente vamos identificar as variáveis e possíveis fatores ligados na ocorrência de crimes por arma de fogo, roubos e homicídios, e posteriormente, criar *insights* de como podemos melhorar a eficiência de serviços de segurança pública, baseado em dados.

Os dados são extraídos do sistema SSPDS-CE (Secretaría de Segurança Pública e Defesa Social do Ceará), e este conjunto de dados reflete incidentes de crimes relatados de 2015 até o presente, exceto os 30 dias mais recentes.

> DISCLAIMER: As classificações preliminares de crimes podem ser alteradas posteriormente com base em investigações adicionais, e sempre há a possibilidade de erro mecanico ou humano nos dados.

Os objetivos e resultados-chave são:

 - Realizar uma análise exploratória de dados (EDA) de crimes por arma de fogo, roubos e homicídios
    - Preparação dos dados 
    - Identificar variáveis, descrevê-las e definir os tipos de dados
    - Realizar transformação e sanitização dos dados (codificação)
    - Tratar valores faltantes e discrepantes
 - Mapear o comportamento de criminalidade
    - Aplicar dados de densidade populacional
    - Aplicar dados socio-econômicos
    - Determinar o fator ocorrência por tipologia (Natureza da causa)
 - Criar modelo de predição de crimes
    - Determinar o índice relativo de ocorrências
    - Simular e otimizar modelo preditivo


## Conteúdo

O notebook #01 consiste em explorar os dados consolidados de crimes relatados pelo SSPDS-CE, a fim de encontrar padrões nos dados, ou informações relevantes que ajudem a explicar, pelo menos parcialmente, a causa das ocorrências de crime.

 - Notebook: 01-analise-exploratoria
    - Identificação das variáveis, definição de tipos de dados e descrição
    - Transformação e sanitização de dados

## Utilização

Para reproduzir os notebooks do projeto, essencialmente é recomendável ter o ```Python 3.8``` instalado, e a versão mais recente do [Poetry](https://python-poetry.org/) como gerenciador de dependências e ambientes virtuais.

> OBS: Também é recomendável ter o ```Java 7+``` instalado, caso queira executar as funções de processamento de arquivos PDF, que é uma dependência do módulo [Tika](https://github.com/chrismattmann/tika-python) para o Python

### 1. Clonar o projeto
```shell
git clone git@github.com:carloap/dataviz-mapeamento-criminalidade.git
cd dataviz-mapeamento-criminalidade
```

### 2. Instalar as dependências
```shell
poetry install
```

### 3. (Não obrigatório) Gerar novo dataset consolidado

Este passo não é necessário, pois o dataset consolidado para analise já consta no repositório. 

No futuro, se for necessário coletar mais dados para atualização do dataset, esses passos serão necessários.
```shell
poetry run invoke extrairPDF
poetry run invoke gerarDataset
```

### 4. Definir o Ambiente Virtual para reproduzir os Notebooks
Feito isso, defina o ambiente virtual criado pelo Poetry em sua aplicação para reprodução dos notebooks, no ```JupyterLab``` ou ```VSCode``` por exemplo.

Para ajudar, verifique qual é o nome do ambiente virtual ```ativo``` no momento, com esse comando.
```shell
poetry env list
```

## Desenvolvedores
 - [Carlos Alberto](https://github.com/carloap)
 - [Fernando Junior](https://github.com/jfernandojr)
 - [Luis Fernando](https://github.com/LuisFernandoASilva)
 - [Marcos Andrey](https://github.com/marcosandrey85)
 - [Willian Martins](https://github.com/WIllianMartins2018)

