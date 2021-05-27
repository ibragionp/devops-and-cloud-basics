pipeline {

    agent any

    stages {
         
        stage('Prepare enviroment') {
               
            steps {
                sh 'sudo yum update -y'

                sh 'sudo yum install -y python3'
                sh 'sudo yum install python3-pip -y'

                
                sh 'sudo pip3 install datetime'
                sh 'sudo pip3 install mysql-connector-python'
                sh 'sudo pip3 install pandas'
                sh 'sudo pip3 install tweepy'
                
                sh 'sudo mkdir -p -m777 /home/ec2-user/devops-and-cloud-basics/tema09/output'
            }
        }


        stage('Build') {

            steps {
                
               sh '''
                cd /var/lib/jenkins/workspace/python-script-pipeline-jenkinsfile/tema06/
                python3 main.py
                '''

            }

        }

        stage('Deploy') {

            steps {

                sh 'sudo rm -rf /home/ec2-user/devops-and-cloud-basics/tema09/output/'

                sh 'sudo cp -r /var/lib/jenkins/workspace/python-script-pipeline-jenkinsfile/tema06/output/ /home/ec2-user/devops-and-cloud-basics/tema09/output/'
                
                sh 'sudo ls /home/ec2-user/devops-and-cloud-basics/tema09/output/'
                
                sh 'sudo -S su - ec2-user -c "aws s3 sync /home/ec2-user/devops-and-cloud-basics/tema09/output/ s3://jt-dataeng-isabellabragionpereira/tema09/output/"'
               
            }

        }

    }

}
