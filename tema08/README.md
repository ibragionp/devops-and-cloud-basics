## Objetivo: 
Agora com uma VM local, necessitamos que você instale uma VM com Windows usando o software que você
desejar (podendo ser o VirtualBox, por exemplo). O objetivo é, usando esta VM Windows, fazer o mesmo processo do
exercício anterior. A diferença entre este exercício e o anterior, é que agora você precisará utilizar um agendamento
dentro do Windows executando um script powershell.

### Preparação da máquina:
Antes de tudo, foi necessário realizar os seguintes passos:

- Instalar na VM Windows o Python 3 e configurar as variáveis de ambiente
- Instalar as bibliotecas Python para execução dos arquivos 
- Clone do projeto do Github
- Instalação do AWS CLI para poder executar comandos aws na VM:
	https://docs.aws.amazon.com/pt_br/cli/latest/userguide/install-windows.html
- Configuração no Powershell para que fosse possível com as Key Access da AWS:
	```
	aws configure 
	```

### Scripts Poweshell:
Para realizar o objetivo foi utilizado o Agendador de Tarefas do Windows. E foram utilizados 2 scripts, pois um seria executado anualmente e outro diariamente:

- Script powershell para executar o arquivo python que faz a análise dos arquivos IMDB que estão no banco de dados MySQL na EC2 AWS.
	
	Editor de texto -> Salvar como... -> .ps1
	
	```
	python C:\Users\isabe\OneDrive\Documentos\devops-and-cloud-basics\tema06\imdb_analysis.py
	```

- Script powershell para executar o arquivo python que faz a análise dos tweets na API do Twitter e sincronizar o arquivo gerado para o Bucket S3 da AWS.
	
	Editor de texto -> Salvar como... -> .ps1
	```
	python C:\Users\isabe\OneDrive\Documentos\devops-and-cloud-basics\tema06\twitter_analysis.py

	aws s3 --region us-east-2 sync C:\Users\isabe\OneDrive\Documentos\devops-and-cloud-basics\tema06\output s3://jt-dataeng-isabellabragionpereira/tema08/output/
	```		

### Agendador de tarefas Windows:
Para agendar uma tarefa no Windows são os seguintes passos:

- "Criar uma tarefa básica"
	- Nome
	- Descrição
	
- Definir a frequência da tarefa

- "Iniciar um programa"

- Em "Programa/Script" deve-se colocar o caminho do executável do Powershell

	- Em "Adicione argumentos" colocar o caminho do script powershell que deseja que ser executado

- "Concluir"

