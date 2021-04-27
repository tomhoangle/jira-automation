pipeline {
    agent {
        label 'docker'
    }
    environment {
        DOCKER_TAG = ""
    }
    stages {
        stage('git tag') {
            steps {
                sh "ls"
                sh "pwd"
                sh """docker run --rm -v "$WORKSPACE:/repo" gittools/gitversion:5.3.5-linux-alpine.3.10-x64-netcoreapp3.1 /repo /showvariable MajorMinorPatch"""
                sh '''git tag ("run-" + $(docker run --rm -v "$WORKSPACE:/repo" gittools/gitversion:5.3.5-linux-alpine.3.10-x64-netcoreapp3.1 /repo /showvariable MajorMinorPatch))'''
            }
        }
    }
}
