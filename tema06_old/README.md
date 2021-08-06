## Objetivo: 
Usando Python e suas bibliotecas, você deve conectar no Twitter e recuperar os últimos 10 tweets a respeitos dos 10 atores que mais fizeram filmes nos últimos 10 anos com base nas informações de catálogo fornecidas pelo IMDB.

### Arquivos IMDB:
Para realizar o objetivo, foram utilizadas os arquivos fornecidos pelo IMDB (https://www.imdb.com/interfaces/) contendo as seguintes informações:

- #### title.basics.tsv.gz - Contém as seguintes informações para títulos:
    - tconst (string) - identificador alfanumérico exclusivo do título
    - titleType (string) - o tipo / formato do título (por exemplo, filme, curta, série de TV, episódio de TV, vídeo etc.)
    - primaryTitle (string) - o título mais popular / o título usado pelos cineastas em materiais promocionais no ponto de lançamento
    - originalTitle (string) - título original, no idioma original
    - isAdult (boolean) - 0: título não adulto; 1: título adulto
    - startYear (YYYY) - representa o ano de lançamento de um título. No caso da série de TV, é o ano de início da série
    - endYear (YYYY) - Ano de fim da série de TV. ‘\ N’ para todos os outros tipos de título
    - runtimeMinutes - tempo de execução principal do título, em minutos
    - gêneros (array de strings) - inclui até três gêneros associados ao título
    
    
- #### title.principals.tsv.gz - Contém o elenco / equipe principal para os títulos
    - tconst (string) - identificador alfanumérico exclusivo do título
    - ordenação (inteiro) - um número para identificar exclusivamente as linhas de um determinado titleId
    - nconst (string) - identificador alfanumérico exclusivo do nome / pessoa
    - categoria (string) - a categoria de trabalho em que a pessoa estava
    - job (string) - o cargo específico, se aplicável, caso contrário '\ N'
    - caracteres (string) - o nome do personagem jogado, se aplicável, caso contrário '\ N'
    
    
- #### name.basics.tsv.gz - Contém as seguintes informações para nomes:
    - nconst (string) - identificador alfanumérico exclusivo do nome / pessoa
    - PrimaryName (string) - nome pelo qual a pessoa é mais frequentemente creditada
    - birthYear - no formato AAAA
    - deathYear - no formato AAAA se aplicável, caso contrário '\ N'
    - PrimaryProfession (array de strings) - as 3 principais profissões da pessoa
    - knownForTitles (array de tconsts) - títulos pelos quais a pessoa é conhecida
    

### Banco de dados MySQL na EC2 AWS:
Os arquivos fornecidos pelo IMDB mencionados,  foram carregados para uma instância EC2 na AWS (Amazon Web Services) e armazenados no banco de dados MySQL que está instalado na instância.
O acesso ao banco de dados na instância está disponível para qualquer host.
Os comandos utilizados para criação de tabelas e upload dos arquivos no banco, encontram-se na pasta: commands_mysql_database -> commands_create_database_mysql e commands_import_data_mysql. 

### Estruturação dos arquivos e pastas:
#### /authentications:
Contém os arquivos para autenticação na API e no Banco de Dados.

#### /commands_mysql_database:
Contém arquivos com os comandos feitos no MySQL para criação do Banco de Dados e na máquina para importação dos dados.

#### /output:
Contém dois arquivos .csv, um com informações dos atores que mais fizeram filmes em um determinado range de anos (10 anos), ordenados pela quantidade, e outro arquivo com tweets referentes aos autores.

#### imdb_analysis.py:
Um arquivo Python que tem como função importar os dados do banco de dados MySQL para dataframes e assim tratá-los para gerar um arquivo .csv com as informações de atores e quantidades de filmes que realizaram.

#### twitter_analysis.py:
Um arquivo Python que tem como função importar os dados de atores/atrizes, buscar e retornar em um arquivo .csv uma quantidade de tweets referentes eles em um range de data.


### Estruturação dos códigos:

#### imdb_analysis funções:

database_connection: Cria uma conexão com o banco de dados na EC2 e retorna a mesma.

filter_df_title: Realiza o filtro do DataFrame para haja apenas registros de filmes 'movie'.

filter_df_title_principals: Realiza o filtro do DataFrame apenas pela categoria de atores e atrizes, somando a quantidade de filmes realizados, bem como o top dos que mais fizeram filmes.

create_lst_str: Realiza a criação de uma string em forma de lista para que seja usada no 'WHERE IN' do MySQL para filtrar os dados que serão importados do banco e melhorar a performance.

import_data_from_database: Realiza a importação dos dados do banco, porém com a utilização de chunk_size para pegar porções da consulta do sql, filtrá-las usando funções anteriores e assim não dar Out of Memory no sistema.

main: Chama todas as funções anteriores, filtrando os DataFrames e no final faz um merge de todos os DataFrames através do identificador do ator/atriz. Assim traz a informação dos nomes e quantidades de filmes realizados, exportando-os para um arquivo .csv

#### twitter_analysis funções:

api_connection: Cria uma conexão com a API do Twitter e retorna a mesma.

import_csv: Importa o arquivo .csv com os dados dos atores/atrizes para um dataframe.

search_tweets_by_name: Após conectar-se a API, busca as informações dos twitter e retorna um DataFrame

main: Itera na lista de nomes dos atores/atrizes e chama a função de buscar tweets passando cada um dos nomes como parâmetros e os DataFrames que retornam, são adicionados a um único que é exportado para um arquivo csv.


### Premissas para execução do script:
- Ter python 3 instalado na máquina
- Importar as bibliotecas os, tweepy, pandas, time e sqlalchemy através dos seguintes comandos:

        pip3 install os tweepy pandas time sqlalchemy

- Necessário clonar todo o repositório, pois nele contém arquivos de autenticação ao Banco de Dados e a API do Twitter.

### Output:
Estrutura do csv de saída para 10 atores que fizeram mais filmes nos últimos 10 anos:

![](/tema06/output/imdb_analysis_example.png)

Estrutura do csv de saída para tweets referentes aos 10 atores que fizeram mais filmes nos últimos 10 anos:

![](/tema06/output/twitter_analysis_example.png)




