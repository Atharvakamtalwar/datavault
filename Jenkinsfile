pipeline {
    agent {
        label 'Node'
    }
    
    environment {
        DOCKER_IMAGE = "datavault"
        DOCKER_TAG = "${BUILD_NUMBER}"
        SONAR_PROJECT_KEY = "datavault"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Security Scan') {
            parallel {
                stage('OWASP') {
                    steps {
                        dependencyCheck additionalArguments: '--format HTML --failOnCVSS 7', odcInstallation: 'OWASP-Dependency-Check'
                    }
                }
                stage('Trivy') {
                    steps {
                        sh 'trivy fs --security-checks vuln,config --severity HIGH,CRITICAL .'
                    }
                }
            }
        }
        
        stage('Code Quality') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
                        sonar-scanner \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.sources=. \
                        -Dsonar.python.coverage.reportPaths=coverage.xml
                    """
                }
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
        stage('Build') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }
        
        stage('Test') {
            steps {
                sh 'pytest --cov=src --cov-report=xml'
            }
        }
        
        stage('Push') {
            steps {
                script {
                    docker.withRegistry('', 'docker-credentials') {
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push('latest')
                    }
                }
            }
        }
        
        stage('Deploy to EKS') {
            steps {
                script {
                    sh """
                        aws eks update-kubeconfig --region us-west-1 --name datavault-cluster
                        kubectl apply -f k8s/
                    """
                }
            }
        }
        
        stage('Update ArgoCD') {
            steps {
                sh """
                    argocd app set datavault --kustomize-image ${DOCKER_IMAGE}=${DOCKER_TAG}
                    argocd app sync datavault
                """
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            emailext (
                subject: "Pipeline Success: ${currentBuild.fullDisplayName}",
                body: "Pipeline completed successfully for commit ${GIT_COMMIT}",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
        }
        failure {
            emailext (
                subject: "Pipeline Failed: ${currentBuild.fullDisplayName}",
                body: "Pipeline failed for commit ${GIT_COMMIT}",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
        }
    }
}
