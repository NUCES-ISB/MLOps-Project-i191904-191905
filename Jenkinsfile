pipeline {
    agent any

    stages {
        stage('Checkout - SCM') {
            steps {
                checkout scm
            }
        }
        stage('Install dependencies and fixes') {
            steps {
                sh 'pip3 install "apache-airflow[celery]==2.6.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.6.1/constraints-3.7.txt"'
                sh 'pip3 install dvc[gdrive]==2.10.2'
                sh 'pip3 install --force-reinstall -v "fsspec==2022.11.0"'
                sh 'pip3 install mlf-core'
                sh 'pip3 uninstall -y pyOpenSSL'
                sh '# /var/lib/jenkins/.local/bin/mlf-core fix-artifact-paths mlruns/'
            }
        }
        stage('Data fetching - DVC') {
            steps {
                sh "# /var/lib/jenkins/.local/bin/dvc init -f"
                sh "# /var/lib/jenkins/.local/bin/dvc remote add -d myremote gdrive://13V42ItETmWb3PJwCZPiGsdpx2KJHERJP"
                sh "# /var/lib/jenkins/.local/bin/dvc pull"
                sh "cp data.csv processed_data.csv"
            }
        }
        stage('Data cleaning - Airflow') {
            steps {
                sh 'mkdir ~/airflow/'
                sh 'mkdir ~/airflow/dags/'
                sh 'cp dags/data_cleaning_dag.py ~/airflow/dags/'
                sh '/var/lib/jenkins/.local/bin/airflow scheduler -D'
                sh '/var/lib/jenkins/.local/bin/airflow dags trigger data_cleaning_dag'
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
