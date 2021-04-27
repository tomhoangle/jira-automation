pipeline {
    agent {
        label 'docker'
    }
    environment {
        VERSION_NUMBER = ""
        DOCKER_TAG = ""
    }
    stages {
        stage('git tag') {
            steps {
                script {
                    VERSION_NUMBER = sh (
                        script: 'docker run --rm -v "$WORKSPACE:/repo" gittools/gitversion:5.3.5-linux-alpine.3.10-x64-netcoreapp3.1 /repo /showvariable MajorMinorPatch',
                        returnStdout: true
                        ).trim()
                   DOCKER_TAG = "run-" + VERSION_NUMBER
                   echo DOCKER_TAG
                    sh 'git tag ${DOCKER_TAG}'
                   sh 'git push --tags'
                }
            }
        }
    }
}
