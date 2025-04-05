pipeline {
    agent any

    tools {
        nodejs 'Node18'
    }

    environment {
        RENDER_API_KEY = credentials('render-api-key')
        RENDER_BACKEND_SERVICE_ID = 'oplinkapi'
        RENDER_FRONTEND_SERVICE_ID = 'oplink'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Backend Setup') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
                bat 'pip install gunicorn'
            }
        }
        stage('Frontend Setup') {
            steps {
                bat 'npm install'
            }
        }
        stage('Backend Tests') {
            steps {
                dir('src') {
                    //bat 'python -m pytest'
                }
            }
        }
        stage('Frontend Tests') {
            steps {
                dir('src') {
                    //bat 'npm run lint'
                }
            }
        }
        stage('Build Frontend') {
            steps {
                dir('src') {
                    bat 'npm run build'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    bat '''
                    curl -X POST ^
                      -H "Authorization: Bearer ${RENDER_API_KEY}" ^
                      -d "serviceId=${RENDER_BACKEND_SERVICE_ID}" ^
                      https://api.render.com/v1/services/${RENDER_BACKEND_SERVICE_ID}/deploy
                    '''
                    bat '''
                    curl -X POST ^
                      -H "Authorization: Bearer ${RENDER_API_KEY}" ^
                      -d "serviceId=${RENDER_FRONTEND_SERVICE_ID}" ^
                      https://api.render.com/v1/services/${RENDER_FRONTEND_SERVICE_ID}/deploy
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Build and tests completed successfully.  Deploying to Render'
        }
        failure {
            echo 'Build or tests failed.  Deployment has not been triggered'
        }
    }
}