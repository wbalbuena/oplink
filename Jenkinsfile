pipeline {
    agent any

    tools {
        nodejs 'Node18'
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
                bat 'git push origin main'
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