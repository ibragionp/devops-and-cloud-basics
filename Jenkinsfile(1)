pipeline {

    agent any
    
    environment {
        USER_CREDENTIALS = credentials('Amazon')
    }

    stages {
    
        stage('Prepare enviroment') {
               
            steps {
                sh'''
                sudo yum update -y
                sudo amazon-linux-extras install docker
                sudo yum install docker
                sudo service docker start
                sudo usermod -a -G docker ec2-user
                '''
                
                sh'''
                sudo chmod 777 /var/run/docker.sock
                '''
               
            }
        }


        stage('Build') {

            steps {
                sh '''
                    docker build -t testing --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --build-arg AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY .
                    docker run testing main.py
                    '''
            }

        }
        
        stage('Test') {

            steps {
                
               sh '''
                docker run testing main_test.py
                '''

            }

        }



    }

}
