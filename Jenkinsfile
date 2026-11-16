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

    
stage('Deployment Approval') {
    steps {
        input message: 'CI passed. Deploy the Excel file?',
              ok: 'Deploy'
    }
}

stage('Deploy') {
    steps {
        sh '''
            set -eu
            DEST="/var/jenkins_home/deployments"

            mkdir -p "$DEST/releases"

            cp employees_updated.xlsx \
               "$DEST/releases/employees_build_${BUILD_NUMBER}.xlsx"

            cp employees_updated.xlsx "$DEST/current.xlsx"

            echo "Excel deployed successfully!"
        '''
    }
}

stage('Verify Deployment') {
    steps {
        sh '''
            .venv/bin/python -c 'from openpyxl import load_workbook; s=load_workbook("/var/jenkins_home/deployments/current.xlsx", read_only=True)["Employees"]; assert s.max_row-1 == 110; print("Deployment verified: 110 records")'
        '''
    }
}
    
    }
}