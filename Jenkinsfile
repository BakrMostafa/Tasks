pipeline {
    agent any

    stages {
        stage('Docker Compose Build') {
            steps {
                echo 'Building Docker containers using docker-compose...'
                script {
                    // Run docker-compose up --build
                    sh 'docker-compose up --build -d'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded!'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}