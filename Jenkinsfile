pipeline {
    agent any
    
    stages {
        stage('Setup & Train Model') {
            steps {
                bat '''
                "C:\\Users\\TCET\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m venv venv
                call venv\\Scripts\\activate
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                python src/train.py
                '''
            }
        }
        
        stage('Package Model (Docker Build)') {
            steps {
                bat 'docker build -t network-mlops-api:latest .'
            }
        }
        
        stage('Deploy API (Docker Run)') {
            steps {
                // Remove old container if it exists, run new one detached (-d)
                bat '''
                docker rm -f network-api-container || exit 0
                docker run -d -p 8000:8000 --name network-api-container network-mlops-api:latest
                '''
            }
        }
        
        stage('Automated Smoke Test') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                python tests/test_api.py
                '''
            }
        }
    }
    
    post {
        cleanup {
            echo "Tearing down deployment and cleaning workspace..."
            bat 'docker stop network-api-container || exit 0'
            bat 'docker rm network-api-container || exit 0'
            cleanWs()
        }
    }
}