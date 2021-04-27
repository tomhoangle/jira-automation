pipeline {
    agent {
        label 'docker'
    }
    environment {
        VERSION_NUMBER = ""
        DOCKER_TAG = ""
        TOM_USER = credentials('gittom')
        REPO_ADDRESS = ""
    }
    stages {
        stage('git tag') {
            steps {
                echo repoUrl
                script {
                    def repoUrl = checkout(scm).GIT_URL
                    VERSION_NUMBER = sh (
                        script: 'docker run --rm -v "$WORKSPACE:/repo" gittools/gitversion:5.3.5-linux-alpine.3.10-x64-netcoreapp3.1 /repo /showvariable MajorMinorPatch',
                        returnStdout: true
                        ).trim()
                   DOCKER_TAG = "run-" + VERSION_NUMBER
                   echo DOCKER_TAG
                   sh "git tag $DOCKER_TAG"
                   sh 'git push https://tomhoangle1:$TOM_USER@github.com/tomhoangle/gitversioning.git --tags'
                }
            }
        }
    }
     post { 
        always { 
            cleanWs()
        }
    }
}
