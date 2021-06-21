## Objetivo: 
Com base no que você desenvolveu até o momento, transforme o seu código paraa rodar em um contêiner
Docker.

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
	7. Preencher com nome da cloud que devera ser "Amazon"
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
9. Em pipeline, definition selecionar pipeline SCM
10. Preencher repository URL com a url .git do projeto 
11. Indicar "Jenkinsfile"
12. Aplicar 
13. Salvar

### O que a pipeline faz:
A pipeline irá fazer toda a preparação do ambiente e execução do script python de análise de dados do twitter e as saídas serão salvas na pasta "home/ec2-user/devops-and-cloud-basics/tema09/output/" dentro da EC2.

A pipeline está com o seguinte passo-a-passo:
1. Declarative: Checkout SCM - Irá fazer o checkout do repositório para branch master e irá clonar o repositório
2. Enviroment - Irá indicar que as credenciais do Jenkins que iremos usar é a criada anteriormente "Amazon"
3. Prepare enviroment - Irá preparar a EC2 para execução do script python:
	1. Instalar o docker
	2. Dar permissões ao docker
4. Build - Irá subir uma imagem docker com as configurações do nosso Dockerfile, que nada mais é do que uma imagem python para executar nossos scripts e como argumento do build da imagem, irá as variáveis de ambiente do Jenkins com as credenciais do "Amazon" criadas anteriormente e definida como ambiente na pipeline:
	1. Build da imagem
	2. Rodar o script python main.py
5. Test - Irá rodar o script de main_test.py da nossa imagem.
	
