## Objetivo: 
Crie uma máquina linux no free-tier dentro da AWS. Esta máquina deverá rodar de forma agendada o código
criado no exercício 06. Você deverá melhorar o seu código, gerando arquivos texto para o resultado; os arquivos texto
devem ser sincronizados com o seu bucket na conta AWS.

### Comandos Cron:
Para realizar o objetivo foi utilizado o Cron para o agendamento das tarefas.

- Para criar editar/inserir um novo agendamento foi utilizado o seguinte comando no terminal:

	crontab -e

- A estrutura do crontab é a seguinte:

	[minutos] [horas] [dias do mês] [mês] [dias da semana] [usuário] [comando]

Minutos: informe números de 0 a 59;
Horas: informe números de 0 a 23;
Dias do mês: informe números de 0 a 31;
Mês: informe números de 1 a 12;
Dias da semana: informe números de 0 a 7;
Usuário: é o usuário que vai executar o comando (não é necessário especificá-lo se o arquivo do próprio usuário for usado);
Comando: a tarefa que deve ser executada.

- A minha estrutura criada ficou da seguinte forma:

	00 18 1 1 * /home/ec2-user/jt-dataeng-isabella/imdb/imdb_analysis.py
	00 13 * * * /home/ec2-user/jt-dataeng-isabella/imdb/twitter_analysis.py

O script python imdb_analysis.py será executado sempre no primeiro mês do ano, no primeiro dia do ano as 18:00 UTC, ou seja 15:00 horário de Brasília.
O script python twitter_analysis.py será executado todos os dias as 13:00 UTC, 10:00 horário de Brasília.

Obs.: Nesse caso o crontab está trabalhando com horário UTC (Universal Time Cordinated), por isso a diferença nos horários com do Brasil.


- Para listar o crontab utiliza-se:

	crontab -l

### Arquivo executável .sh:
Para a sincronização da ec2 com o bucket, foi feito um arquivo executável. 

- Para criar e editar usando o editor nano, foram utilizados os comandos:

	sudo touch sync_ec2_bucket.sh
	sudo nano sync_ec2_bucket.sh

- Para tornar o arquivo criado um executável:

	sudo chmod 777 sync_ec2_bucket.sh

- Por fim bastou colocá-lo no crontab agendamento dessa forma:

	02 13 * * * /home/ec2-user/sync_ec2_bucket.sh
	

