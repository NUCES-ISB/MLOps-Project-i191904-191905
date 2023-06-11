pipeline {
    agent any

    stages {
        stage('Checkout - SCM') {
            checkout scm
        }
        stage('Install dependencies and fixes') {
            steps {
                sh 'pip install "apache-airflow[celery]==2.6.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.6.1/constraints-3.8.txt"'
                sh 'pip install dvc[gdrive]'
                sh 'pip install mlf-core'
                sh 'mlf-core fix-artifact-paths mlruns/'
            }
        }
        stage('Data fetching - DVC') {
            steps {
                sh "dvc pull"
            }
        }
        stage('Data cleaning and augmentation - Airflow') {
            steps {
                echo 'Airflow'
                sh 'cp data.csv processed_data.csv'
            }
        }
        stage('Train, track, and upload model - MLflow') {
            steps {
                sh "python training.py"
                sh "#git commit -m 'MLflow run [no ci]'"
                sh "#git push origin"
            }
        }
        stage('Build image - Docker') {
            steps {
                sh '#cd MLOps-Project-i191904-i191905/'
                sh '#docker build -t projectimage .'
            }
        }
        stage('Deploy image - Docker') {
            steps {
                sh '#docker run projectimage:latest -p 8000:8000'
            }
        }
    }
}