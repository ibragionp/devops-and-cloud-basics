pipeline {

     agent any

     stages {
     
        stage("Prepare enviroment") {

                sh "sudo yum update -y"

                sh "sudo yum install -y python3"
                sh "sudo yum install python3-pip -y"
                
                sh "sudo wget https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm"
                sh "sudo md5sum mysql80-community-release-el7-3.noarch.rpm"
                sh "sudo rpm –ivh mysql80-community-release-el7-3.noarch.rpm"
                sh "sudo yum install mysql-server"
                
                sh "sudo pip3 install datetime"
                sh "sudo pip3 install mysql-connector-python"
                sh "sudo pip3 install os"
                sh "sudo pip3 install pandas"
                sh "sudo pip3 install pandas.io"
                sh "sudo pip3 install time"
                sh "sudo pip3 install tweepy"

        }

      

     
        stage("Build") {

            steps {

                sh "sudo npm install"

                sh "sudo npm run build"

            }

        }

        stage("Build") {

            steps {

                sh "sudo npm install"

                sh "sudo npm run build"

            }

        }

        stage("Deploy") {

            steps {

                sh "sudo rm -rf /var/www/jenkins-react-app"

                sh "sudo cp -r ${WORKSPACE}/build/ /var/www/jenkins-react-app/"

            }

        }

    }

}
