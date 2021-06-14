pipeline {

    agent any
  
    environment { 
        YOUR_CRED = credentials('amazon') 
    }

    stages {
         
        stage('Prepare enviroment') {
               
            steps {
                sh 'sudo yum update -y'

                sh 'sudo yum install -y python3'
                sh 'sudo yum install python3-pip -y'

                
                sh 'sudo pip3 install datetime'
                sh 'sudo pip3 install pandas'
                sh 'sudo pip3 install boto3'
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
        
        stage('Test') {

            steps {
                
               sh '''
                cd /var/lib/jenkins/workspace/python-script-pipeline-jenkinsfile/tema06/
                python3 analysis_test.py
                '''

            }

        }


        stage('Deploy') {

            steps {

                sh 'sudo rm -rf /home/ec2-user/devops-and-cloud-basics/tema09/output/'

                sh 'sudo cp -r /var/lib/jenkins/workspace/python-script-pipeline-jenkinsfile/tema06/output/ /home/ec2-user/devops-and-cloud-basics/tema09/output/'
              
            }

        }

    }

}
