

pipeline {
    agent any
    environment {
    TIME = sh(script: 'date "+%Y-%m-%d %H:%M:%S"', returnStdout: true).trim()
      }
    stages {
      stage('git clone') {
            steps {
                sh 'git clone https://github.com/sivanmarom/project-flask-app.git'
                sh 'ls project-flask-app'
            }
        }
        stage('Build Docker image') {
           steps {
                sh 'sudo docker build -t flask_image .'
               sh "sudo docker run -it --name flaskApp -p 5000:5000 -d flask_image"
          }
    }
      stage('Testing') {
            steps {
                sh 'cd project-flask-app'
                sh 'pytest test-try.py::Test_class --html=report.html'
            }
        }
//
//
//         stage("build user") {
//   steps{
//     wrap([$class: 'BuildUser', useGitAuthor: true]) {
//       sh 'echo ${BUILD_USER} >> Result.json'
//     }
//   }
// }
//       stage("testing") {
//     steps {
//         script {
//            STATUS = sh(script: "curl -I \$(dig +short myip.opendns.com @resolver1.opendns.com):5000 | grep \"HTTP/1.1 200 OK\" | tr -d \"\\r\\n\"", returnStdout: true).trim()
//             sh 'echo "$STATUS" >> Result.json'
//             sh 'echo "$TIME" >> Result.json'
//             withAWS(credentials: 'awscredentials', region: 'us-east-1') {
//                 sh "aws dynamodb put-item --table-name test-result --item '{\"user\": {\"S\": \"${BUILD_USER}\"}, \"date\": {\"S\": \"${TIME}\"}, \"state\": {\"S\": \"${STATUS}\"}}'"
//             }
//         }
//     }
//       }
//
//         stage ('upload to s3 bucket'){
//             steps{
//                 withAWS(credentials: 'awscredentials'){
//                      sh 'aws s3 cp Result*.json s3://test-result-flask-app'
//                 }
//             }
//         }
// //
// //         stage('stop conatiner'){
// //             steps {
// //
// //                 sh' sudo docker stop flaskApp'
// //                 sh 'sudo docker rm flaskApp'
// //             }
// //         }
    }
    post {
        always {
            deleteDir()
        }
    }
}
