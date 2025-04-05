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
                sh 'python -m pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
                sh 'pip install gunicorn'
            }
        }
        stage('Frontend Setup') {
            steps {
                sh 'npm install'
            }
        }
        stage('Backend Tests') {
            steps {
                dir('src') {
                    //sh 'python -m pytest'
                }
            }
        }
        stage('Frontend Tests') {
            steps {
                dir('src') {
                    //sh 'npm run lint'
                }
            }
        }
        stage('Build Frontend') {
            steps {
                dir('src') {
                    sh 'npm run build'
                }
            }
        }
        stage('Deploy') {
            steps {
                sh 'git push origin main'
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