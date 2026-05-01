pipeline {
    agent any

    environment {
        PYTHON_VERSION = "3"
        VIRTUAL_ENV = "venv"
        DEVPI_USER = credentials('devpi-test-user')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . ./${VIRTUAL_ENV}/bin/activate
                    pip install --upgrade pip
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    . ./${VIRTUAL_ENV}/bin/activate
                    pip install -r requirements.txt
                    pip install -r requirements-tests.txt
                    pip install devpi-client
                    mkdir -p reports
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . ./${VIRTUAL_ENV}/bin/activate
                    python3 -m unittest
                '''
            }
        }

        stage('Code Quality') {
            parallel {
                stage('Lint') {
                    steps {
                        sh '''
                            . ./${VIRTUAL_ENV}/bin/activate
                            flake8 src/ tests/ --output-file=reports/flake8-report.txt || true
                            python3 -m pylint src/partsdb_tools --output-format=parseable --reports=no > reports/pylint-report.txt || true
                        '''
                        recordIssues enabledForFailure: true, aggregatingResults: true, tool: pyLint(pattern: 'reports/pylint-report.txt')
                    }
                }

                stage('Type Checking') {
                    steps {
                        sh '''
                            . ./${VIRTUAL_ENV}/bin/activate
                            mypy src/ --junit-xml reports/mypy-report.xml || true
                        '''
                        recordIssues enabledForFailure: true, aggregatingResults: true, tool: myPy(pattern: 'reports/mypy-report.xml')
                    }
                }

                stage('Security Scan') {
                    steps {
                        sh '''
                            . ./${VIRTUAL_ENV}/bin/activate
                            bandit -r src/ -f json -o reports/bandit-report.json || true
                            bandit -r src/ -f html -o reports/bandit-report.html || true
                        '''
                        archiveArtifacts artifacts: 'reports/bandit-report.json, reports/bandit-report.html', allowEmptyArchive: true
                    }
                }
            }
        }

        stage('Build') {
            steps {
                 sh '''
                    . ./${VIRTUAL_ENV}/bin/activate
                    python3 -m pip install --upgrade build && python3 -m build
                 '''
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([string(credentialsId: 'devpi_dev_index', variable: '$DEVPI_INDEX')]) {
                    sh '''
                    . ./${VIRTUAL_ENV}/bin/activate
                    ls
                    devpi use $DEVPI_INDEX
                    devpi login ${DEVPI_USER_USR} --password=${DEVPI_USER_PSW}
                    devpi upload --from-dir dist
                    '''
                }
            }
        }
    }

    post {
        always {
            junit testResults: 'reports/*.xml', skipPublishingChecks: true
            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'bandit-report.html',
                reportName: 'Bandit Security Report'
            ])
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'coverage.xml',
                reportName: 'Coverage Report'
            ])
            cleanWs()
        }
    }
}