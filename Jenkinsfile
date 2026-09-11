pipeline {
    agent any
    
    environment {
        // Keep this so Jenkins has permission to talk to the Docker daemon
        DOCKER_HOST = "tcp://localhost:2375"
    }
    
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
                bat '"C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe" build -t network-mlops-api:latest .'
            }
        }
        
        stage('Deploy API (Docker Run)') {
            steps {
                bat '''
                "C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe" rm -f network-api-container || exit 0
                "C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe" run -d -p 8000:8000 --name network-api-container network-mlops-api:latest
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
            bat '"C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe" stop network-api-container || exit 0'
            bat '"C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe" rm network-api-container || exit 0'
            cleanWs()
        }
    }
}