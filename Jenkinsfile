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
                docker run --rm -v "$PWD:/repo" gittools/gitversion:5.3.5-linux-alpine.3.10-x64-netcoreapp3.1 /repo
            }
        }
    }
}
