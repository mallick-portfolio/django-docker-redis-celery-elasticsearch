pipeline {
  agent any
  
   tools {nodejs "node"}
    
  stages {
    stage("Clone code from GitHub") {
            steps {
                script {
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'GITHUB_CREDENTIAL', url: 'https://github.com/mallick-portfolio/jenkis-nextapp.git']])
                }
            }
        }
     
    stage('Node JS Build') {
      steps {
        sh 'npm install'
      }
    }
  
     stage('Build Node JS Docker Image') {
            steps {
                script {
                  sh 'docker build -t tamal008/jenkins_nextapp .'
                }
            }
        }


      stage('Deploy Docker Image to DockerHub') {
            steps {
                script {
                    withDockerRegistry(credentialsId: 'DOCKER_CREDENTIAL', url: 'https://index.docker.io/v1/') {
                        // Tag the image with the correct version before pushing
                        sh 'docker tag tamal008/jenkins_nextapp:latest tamal008/jenkins_nextapp:1.3'
                        // Push the tagged image to DockerHub
                        sh 'docker push tamal008/jenkins_nextapp:1.3'
                    }
                }
            }   
        }

         
     stage('Deploying Node App to Kubernetes') {
      steps {
        script {
            // Set KUBECONFIG environment variable to Jenkins' Minikube configuration
            withEnv(['KUBECONFIG=/var/lib/jenkins/.minikube/config']) {
                sh "kubectl config use-context minikube"
                sh "kubectl apply -f deployment.yaml --validate=false"
                sh "kubectl apply -f service.yaml --validate=false"
            }
        }
      }
    }

  }
}