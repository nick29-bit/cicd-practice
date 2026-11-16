pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install openpyxl
                '''
            }
        }

        stage('Run Python') {
            steps {
                sh '.venv/bin/python update_employees.py'
            }
        }

        stage('Validate') {
            steps {
                sh '''
                    .venv/bin/python -c 'from openpyxl import load_workbook; s = load_workbook("employees_updated.xlsx", read_only=True)["Employees"]; assert s.max_row - 1 == 110; print("Validation Passed: 110 records")'
                '''
            }
        }

        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'employees_updated.xlsx', fingerprint: true
            }
        }
    }
}