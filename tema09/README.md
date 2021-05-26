## Objetivo: 
Até o momento você tem um código que faz a sincronia dos tweets, gerando um arquivo com o resultado e
sincronizando para o S3. Agora, como objetivo, queremos que você automatize o processo de deploy desse seu código,
onde puxará do seu github e fará o deploy dentro da sua EC2 Linux.até o momento você tem um código que faz a sincronia dos tweets, gerando um arquivo com o resultado e
sincronizando para o S3. Agora, como objetivo, queremos que você automatize o processo de deploy desse seu código,
onde puxará do seu github e fará o deploy dentro da sua EC2 Linux.

---

## CRIAÇÃO DA PIPELINE ATRAVÉS DO JENKINSFILE:

### Preparação da máquina (AWS EC2) e configurar o Jenkins:
Antes de tudo, foi necessário realizar os seguintes passos:

- Instalar o git
		sudo yum update -y
		sudo yum install git -y
		
- Verificar se foi instalado o git
		git version

- Instalar o Jenkins
		sudo yum update –y
		sudo wget -O /etc/yum.repos.d/jenkins.repo \
https://pkg.jenkins.io/redhat-stable/jenkins.repo
		sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
		sudo yum upgrade
		sudo yum install jenkins java-1.8.0-openjdk-devel -y
		sudo systemctl daemon-reload
		sudo systemctl start jenkins
- Verificar se o jenkins está ativado
		sudo systemctl status jenkins
- Configurar o Jenkins
	- Abrir no navegador a interface do Jenkins http://<DNS IPv4 público da ec2>:8080/
	
- Entrar com a senha inicial do Jenkins que é obtida através do seguinte comando
		sudo cat /var/lib/jenkins/secrets/initialAdminPassword
		
- Criar o Admin User 

- Instalar o plugin AWS EC2
	- Dashboard -> Gerenciar Jenkins -> Gerenciar plugins -> Disponíveis -> Pesquisar EC2 -> Selecionar Amazon EC2 plugin -> Download now and install after restart -> Logar novamente com Admin user criado anteriormente
	
- Adicionar Cloud
	- Dashboard -> Gerenciar Jenkins - Configurar Sitema -> Cloud -> Amazon EC2 -> Configure Clouds -> Preencher com nome da cloud -> Preencher Amazon EC2 Credentials -> Preencher region com a região da sua EC2 -> Preencher EC2 Key Pair's Private Key -> Test Connection para verificar se está tudo certo -> Apply -> Save
	
- Dar autorização de super usuário ao Jenkins para que a pipeline possa executar comandos root como, por exemplo, instalar bibliotecas
		sudo nano /etc/sudoers/
	- Inserir no fim do arquivo: jenkins ALL=(ALL) NOPASSWD: ALL
	- Salvar alterações


### Criação do Webhook no repositório do Github:
Primeiramente, para que seja possível fazer o build e deploy do projeto que está no Github, é necessário criar um webhook com o servidor Jenkins da EC2. 

- Ir ao repositório -> Configurações -> Webhooks -> Add webhook -> Em payload URL colocar a URL do jenkins da ec2 "/" e o nome do webhook -> Marcar Just the push event -> Marcar Active -> Save webhook


### Criar job para build e deploy:
No repositório há um arquivo chamado Jenkinsfile, é onde está configurado todo o passo a passo da pipeline. Iremos apenas "importar" para o Jenkins da EC2.

- Dashboard -> Novo job -> Preencher com o nome python-script-pipeline-jenkinsfile (igual ao que está no jenkinsfile do github) -> Selecionar pipeline -> Ok
- Em general marcar GitHub project -> Em project url, colocar a URL do repositório sem "tree/master" -> Em build triggers marcar GitHub hook trigger for GITScm polling -> Em pipeline, definition selecionar pipeline script from SCM (porque nossa pipeline está no repositório) -> SCM selecionar Git -> Preencher repository URL com a url .git do projeto -> Credentials adicionar a credencial do github -> Brach specifier deixar */master -> Navegar no repositório como Auto -> Em script path, colocar o nome da pipeline que está no repositório, no caso Jenkinsfile mesmo -> Aplicar -> Salvar

### O que a pipeline faz:
A irá fazer toda a preparação do ambiente e execução do script python de análise de dados do twitter e as saídas serão salvas na pasta "home/ec2-user/devops-and-cloud-basics/tema09/output/" dentro da EC2.

A pipeline está com o seguinte passo-a-passo:
- Declarative: Checkout SCM - Irá fazer o checkout da master e irá salvar no workspace do jenkins.
- Prepare enviroment - Irá preparar a EC2 para execução do script python:
	- Instalação do python 3
	- Instalação do pip 3
	- Instalação das bibliotecas necessárias (datetime, mysql-connector-python, pandas e tweepy)
	- Criação da pasta onde será feito o deploy do projeto, ou seja, ficarão as saídas do script python.
- Build - Irá navegar até a pasta do tema06 e executar o script python
- Deploy - Irá excluir qualquer coisa que esteja na pasta onde será feito o deploy, criada anteriormente, caso tenha algo referente a um build anterior. E irá copiar os arquivos de build gerados, após a execução do script python, do workspace do jenkins para a nossa pasta criada anteriormente. Assim qualquer atualização no repositório, será atualizado também na EC2.

---

## CRIAÇÃO DA PIPELINE NO JENKINS:

### Preparação da máquina (AWS EC2) e configurar o Jenkins:
Antes de tudo, foi necessário realizar os seguintes passos:

- Instalar o git
		sudo yum update -y
		sudo yum install git -y
		
- Verificar se foi instalado o git
		git version

- Instalar o Jenkins
		sudo yum update –y
		sudo wget -O /etc/yum.repos.d/jenkins.repo \
		https://pkg.jenkins.io/redhat-stable/jenkins.repo
		sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
		sudo yum upgrade
		sudo yum install jenkins java-1.8.0-openjdk-devel -y
		sudo systemctl daemon-reload
		sudo systemctl start jenkins
- Verificar se o jenkins está ativado
		sudo systemctl status jenkins
- Configurar o Jenkins
	- Abrir no navegador a interface do Jenkins http://<DNS IPv4 público da ec2>:8080/
	
- Entrar com a senha inicial do Jenkins que é obtida através do seguinte comando
		sudo cat /var/lib/jenkins/secrets/initialAdminPassword
		
- Criar o Admin User 

- Instalar o plugin AWS EC2
	- Dashboard -> Gerenciar Jenkins -> Gerenciar plugins -> Disponíveis -> Pesquisar EC2 -> Selecionar Amazon EC2 plugin -> Download now and install after restart -> Logar novamente com Admin user criado anteriormente
	
- Adicionar Cloud
	- Dashboard -> Gerenciar Jenkins - Configurar Sitema -> Cloud -> Amazon EC2 -> Configure Clouds -> Preencher com nome da cloud -> Preencher Amazon EC2 Credentials -> Preencher region com a região da sua EC2 -> Preencher EC2 Key Pair's Private Key -> Test Connection para verificar se está tudo certo -> Apply -> Save


### Criação do Webhook no repositório do Github:
Primeiramente, para que seja possível fazer o build e deploy do projeto que está no Github, é necessário criar um webhook com o servidor Jenkins da EC2. 

- Ir ao repositório -> Configurações -> Webhooks -> Add webhook -> Em payload URL colocar a URL do jenkins da ec2 "/" e o nome do webhook -> Marcar Just the push event -> Marcar Active -> Save webhook


### Criar job para build e deploy:
No repositório há um arquivo chamado Jenkinsfile, é onde está configurado todo o passo a passo da pipeline. Iremos apenas "importar" para o Jenkins da EC2.

- Dashboard -> Novo job -> Preencher com um nome -> Selecionar pipeline -> Ok
- Em general marcar GitHub project -> Em project url, colocar a URL do repositório sem "tree/master" -> Em build triggers marcar GitHub hook trigger for GITScm polling -> Em pipeline, definition selecionar pipeline script -> SCM selecionar Git -> Preencher repository URL com a url .git do projeto -> Escrever ou colar o conteúdo da pipeline -> Aplicar -> Salvar

### O que a pipeline faz:
A irá fazer toda a preparação do ambiente e execução do script python de análise de dados do twitter e as saídas serão salvas na pasta "home/ec2-user/devops-and-cloud-basics/tema09/output/" dentro da EC2.

A pipeline está com o seguinte passo-a-passo:
- Checkout - Irá fazer o checkout do repositório para branch master
- Clone - Irá clonar o repositório
- Prepare enviroment - Irá preparar a EC2 para execução do script python:
	- Instalação do python 3
	- Instalação do pip 3
	- Instalação das bibliotecas necessárias (datetime, mysql-connector-python, pandas e tweepy)
	- Criação da pasta onde será feito o deploy do projeto, ou seja, ficarão as saídas do script python.
- Build - Irá navegar até a pasta do tema06 e executar o script python
- Deploy - Irá excluir qualquer coisa que esteja na pasta onde será feito o deploy, criada anteriormente, caso tenha algo referente a um build anterior. E irá copiar os arquivos de build gerados, após a execução do script python, do workspace do jenkins para a nossa pasta criada. Assim qualquer atualização no repositório, será atualizado também na EC2.




