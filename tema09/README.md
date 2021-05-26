## Objetivo: 
Até o momento você tem um código que faz a sincronia dos tweets, gerando um arquivo com o resultado e
sincronizando para o S3. Agora, como objetivo, queremos que você automatize o processo de deploy desse seu código,
onde puxará do seu github e fará o deploy dentro da sua EC2 Linux.até o momento você tem um código que faz a sincronia dos tweets, gerando um arquivo com o resultado e
sincronizando para o S3. Agora, como objetivo, queremos que você automatize o processo de deploy desse seu código,
onde puxará do seu github e fará o deploy dentro da sua EC2 Linux.

---

## Criação da pipeline através do Jenkinsfile:

### Preparação da máquina (AWS EC2) e configurar o Jenkins:
Antes de tudo, foi necessário realizar os seguintes passos:

1. Instalar o git
``` 
sudo yum update -y
sudo yum install git -y
``` 
2. Verificar se foi instalado o git
``` 
git version
``` 
3. Instalar o Jenkins
``` 
sudo yum update –y
sudo wget -O /etc/yum.repos.d/jenkins.repo \ https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
sudo yum upgrade
sudo yum install jenkins java-1.8.0-openjdk-devel -y
sudo systemctl daemon-reload
sudo systemctl start jenkins
``` 
4. Verificar se o jenkins está ativado
``` 
sudo systemctl status jenkins
``` 
5. Configurar o Jenkins
	1. Abrir no navegador a interface do Jenkins http://<DNS IPv4 público da ec2>:8080/
	
6. Entrar com a senha inicial do Jenkins que é obtida através do seguinte comando
``` 
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
``` 	
7. Criar o Admin User 

8. Instalar o plugin AWS EC2
	1. Dashboard
	2. Gerenciar Jenkins 
	3. Gerenciar plugins 
	4. Disponíveis 
	5. Pesquisar "EC2"
	6. Selecionar Amazon EC2 plugin 
	7. Download now and install after restart 
	8. Logar novamente com Admin user criado anteriormente
	
9. Adicionar Cloud
	1. Dashboard 
	2. Gerenciar Jenkins 
	3. Configurar Sitema 
	4. Cloud 
	5. Amazon EC2 
	6. Configure Clouds 
	7. Preencher com nome da cloud -
	8. Preencher Amazon EC2 Credentials 
	9. Preencher region com a região da sua EC2 
	10. Preencher EC2 Key Pair's Private Key 
	11. Test Connection para verificar se está tudo certo 
	12. Apply 
	13. Save
	
10. Dar autorização de super usuário ao Jenkins para que a pipeline possa executar comandos root como, por exemplo, instalar bibliotecas
	``` 
	sudo nano /etc/sudoers/
	``` 
	1. Inserir no fim do arquivo: jenkins ALL=(ALL) NOPASSWD: ALL
	2. Salvar alterações


### Criação do Webhook no repositório do Github:
Primeiramente, para que seja possível fazer o build e deploy do projeto que está no Github, é necessário criar um webhook com o servidor Jenkins da EC2

1. Ir ao repositório 
2. Configurações 
3. Webhooks 
4. Add webhook 
5. Em payload URL colocar a URL do jenkins da ec2 "/" e o nome do webhook 
6. Marcar Just the push event 
7. Marcar Active 
8. Save webhook


### Criar job para build e deploy:
No repositório há um arquivo chamado Jenkinsfile, é onde está configurado todo o passo a passo da pipeline. Iremos apenas "importar" para o Jenkins da EC2.

1. Dashboard 
2. Novo job 
3. Preencher com o nome python-script-pipeline-jenkinsfile
4. Selecionar pipeline 
5. Ok
6. Em general marcar GitHub project 
7. Em project url, colocar a URL do repositório sem "tree/master" 
8. Em build triggers marcar GitHub hook trigger for GITScm polling
9. Em pipeline, definition selecionar pipeline script from SCM (porque nossa pipeline está no repositório) 
10. SCM selecionar Git
11. Preencher repository URL com a url .git do projeto
12. Credentials adicionar a credencial do github
13. Brach specifier deixar */master
14. Navegar no repositório como Auto
15. Em script path, colocar o nome da pipeline que está no repositório, no caso Jenkinsfile mesmo
16. Aplicar 
17. Salvar

### O que a pipeline faz:
A pipeline irá fazer toda a preparação do ambiente e execução do script python de análise de dados do twitter e as saídas serão salvas na pasta "home/ec2-user/devops-and-cloud-basics/tema09/output/" dentro da EC2.

A pipeline está com o seguinte passo-a-passo:
1. Declarative: Checkout SCM - Irá fazer o checkout da master e irá salvar no workspace do jenkins.
2. Prepare enviroment - Irá preparar a EC2 para execução do script python:
	1. Instalação do python 3
	2. Instalação do pip 3
	3. Instalação das bibliotecas necessárias (datetime, mysql-connector-python, pandas e tweepy)
	4. Criação da pasta onde será feito o deploy do projeto, ou seja, ficarão as saídas do script python.
4. Build - Irá navegar até a pasta do tema06 e executar o script python
5 Deploy - Irá excluir qualquer coisa que esteja na pasta onde será feito o deploy, criada anteriormente, caso tenha algo referente a um build anterior. E irá copiar os arquivos de build gerados, após a execução do script python, do workspace do jenkins para a nossa pasta criada anteriormente. Assim qualquer atualização no repositório, será atualizado também na EC2.

---

## Criação da pipeline no Jenkins:

### Preparação da máquina (AWS EC2) e configurar o Jenkins:
Antes de tudo, foi necessário realizar os seguintes passos:

1. Instalar o git
``` 
sudo yum update -y
sudo yum install git -y
``` 
2. Verificar se foi instalado o git
``` 
git version
``` 
3. Instalar o Jenkins
``` 
sudo yum update –y
sudo wget -O /etc/yum.repos.d/jenkins.repo \ https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
sudo yum upgrade
sudo yum install jenkins java-1.8.0-openjdk-devel -y
sudo systemctl daemon-reload
sudo systemctl start jenkins
``` 
4. Verificar se o jenkins está ativado
``` 
sudo systemctl status jenkins
``` 
5. Configurar o Jenkins
	1. Abrir no navegador a interface do Jenkins http://<DNS IPv4 público da ec2>:8080/
	
6. Entrar com a senha inicial do Jenkins que é obtida através do seguinte comando
``` 
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
``` 	
7. Criar o Admin User 

8. Instalar o plugin AWS EC2
	1. Dashboard
	2. Gerenciar Jenkins 
	3. Gerenciar plugins 
	4. Disponíveis 
	5. Pesquisar "EC2"
	6. Selecionar Amazon EC2 plugin 
	7. Download now and install after restart 
	8. Logar novamente com Admin user criado anteriormente
	
9. Adicionar Cloud
	1. Dashboard 
	2. Gerenciar Jenkins 
	3. Configurar Sitema 
	4. Cloud 
	5. Amazon EC2 
	6. Configure Clouds 
	7. Preencher com nome da cloud -
	8. Preencher Amazon EC2 Credentials 
	9. Preencher region com a região da sua EC2 
	10. Preencher EC2 Key Pair's Private Key 
	11. Test Connection para verificar se está tudo certo 
	12. Apply 
	13. Save
	
10. Dar autorização de super usuário ao Jenkins para que a pipeline possa executar comandos root como, por exemplo, instalar bibliotecas
	``` 
	sudo nano /etc/sudoers/
	``` 
	1. Inserir no fim do arquivo: jenkins ALL=(ALL) NOPASSWD: ALL
	2. Salvar alterações


### Criação do Webhook no repositório do Github:
Primeiramente, para que seja possível fazer o build e deploy do projeto que está no Github, é necessário criar um webhook com o servidor Jenkins da EC2

1. Ir ao repositório 
2. Configurações 
3. Webhooks 
4. Add webhook 
5. Em payload URL colocar a URL do jenkins da ec2 "/" e o nome do webhook 
6. Marcar Just the push event 
7. Marcar Active 
8. Save webhook

### Criar job para build e deploy:
No repositório há um arquivo chamado Jenkinsfile, é onde está configurado todo o passo a passo da pipeline. Iremos apenas "importar" para o Jenkins da EC2.

1. Dashboard 
2. Novo job 
3. Preencher com o nome python-script-pipeline-jenkinsfile
4. Selecionar pipeline 
5. Ok
6. Em general marcar GitHub project 
7. Em project url, colocar a URL do repositório sem "tree/master" 
8. Em build triggers marcar GitHub hook trigger for GITScm polling
9. Em pipeline, definition selecionar pipeline script
10. Preencher repository URL com a url .git do projeto 
11. Escrever ou colar o conteúdo da pipeline 
12. Aplicar 
13. Salvar

### O que a pipeline faz:
A pipeline irá fazer toda a preparação do ambiente e execução do script python de análise de dados do twitter e as saídas serão salvas na pasta "home/ec2-user/devops-and-cloud-basics/tema09/output/" dentro da EC2.

A pipeline está com o seguinte passo-a-passo:
1. Checkout - Irá fazer o checkout do repositório para branch master
2. Clone - Irá clonar o repositório
3. Prepare enviroment - Irá preparar a EC2 para execução do script python:
	1. Instalação do python 3
	2. Instalação do pip 3
	3. Instalação das bibliotecas necessárias (datetime, mysql-connector-python, pandas e tweepy)
	4. Criação da pasta onde será feito o deploy do projeto, ou seja, ficarão as saídas do script python.
4. Build - Irá navegar até a pasta do tema06 e executar o script python
5. Deploy - Irá excluir qualquer coisa que esteja na pasta onde será feito o deploy, criada anteriormente, caso tenha algo referente a um build anterior. E irá copiar os arquivos de build gerados, após a execução do script python, do workspace do jenkins para a nossa pasta criada. Assim qualquer atualização no repositório, será atualizado também na EC2.




