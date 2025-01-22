#!/usr/bin/env bash

pipeline {
    agent any
    environment {
        VENV_DIR = "/var/lib/jenkins/workspace/Books-Management-Pipeline/venv"
        PROJECT_DIR = "/var/lib/jenkins/workspace/Books-Management-Pipeline"
        GIT_URL = 'https://github.com/marianadeem03/Books-Management'
        BRANCH = 'development'
        CREDENTIALS_ID = 'github-pat'
    }
    stages {
        stage('Checkout') {
            steps {
                git(
                    branch: "${BRANCH}",
                    url: "${GIT_URL}",
                    credentialsId: "${CREDENTIALS_ID}"
                )
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                #!/bin/bash
                echo pwd
                # Ensure the virtual environment exists
                if [ ! -d "$VENV_DIR" ]; then
                    virtualenv "$VENV_DIR"
                fi

                source "$VENV_DIR/bin/activate"

                # Install dependencies
                pip3 install -r requirements.txt
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                echo "Restarting services..."
                sudo supervisorctl restart django_server
                sudo systemctl restart nginx
                '''
            }
        }
    }
}
