pipeline {
    agent any
    
    environment {
        ACR_LOGIN_SERVER = 'acrsmarketing17567.azurecr.io'
        IMAGE_NAME = 'member'
        MANIFEST_REPO = 'https://github.com/won-ktds/smarketing-manifest.git'
        MANIFEST_PATH = 'member/deployment.yaml'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                dir('member') {
                    sh './gradlew clean build -x test'
                }
            }
        }
        
        stage('Test') {
            steps {
                dir('member') {
                    sh './gradlew test'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = "${BUILD_NUMBER}-${env.GIT_COMMIT.substring(0,8)}"
                    def fullImageName = "${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${imageTag}"
                    
                    dir('member') {
                        sh "docker build -t ${fullImageName} ."
                    }
                    
                    withCredentials([usernamePassword(credentialsId: 'acr-credentials', usernameVariable: 'ACR_USERNAME', passwordVariable: 'ACR_PASSWORD')]) {
                        sh "docker login ${ACR_LOGIN_SERVER} -u ${ACR_USERNAME} -p ${ACR_PASSWORD}"
                        sh "docker push ${fullImageName}"
                    }
                    
                    env.IMAGE_TAG = imageTag
                    env.FULL_IMAGE_NAME = fullImageName
                }
            }
        }
        
        stage('Update Manifest') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-credentials', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_TOKEN')]) {
                    sh '''
                        git clone https://${GIT_TOKEN}@github.com/won-ktds/smarketing-manifest.git manifest-repo
                        cd manifest-repo
                        
                        # Update image tag in deployment.yaml
                        sed -i "s|image: .*|image: ${FULL_IMAGE_NAME}|g" ${MANIFEST_PATH}
                        
                        git config user.email "jenkins@smarketing.com"
                        git config user.name "Jenkins"
                        git add .
                        git commit -m "Update ${IMAGE_NAME} image to ${IMAGE_TAG}"
                        git push origin main
                    '''
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
