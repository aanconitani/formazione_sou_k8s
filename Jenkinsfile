pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub') // Configura il tuo ID di credenziali Jenkins
        DOCKER_IMAGE_NAME = 'aanconitani/flask-app-example'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set Image Tag') {
            steps {
                script {
                    def branchName = env.GIT_BRANCH.replace('origin/', '')
                    if (env.GIT_TAG) {
                        env.DOCKER_IMAGE_TAG = env.GIT_TAG
                    } else if (branchName == 'master') {
                        env.DOCKER_IMAGE_TAG = 'latest'
                    } else if (branchName == 'develop') {
                        env.DOCKER_IMAGE_TAG = "develop-${env.GIT_COMMIT.substring(0, 7)}"
                    } else {
                        error "Unsupported branch ${branchName}"
                    }
                    echo "Docker Image Tag: ${env.DOCKER_IMAGE_TAG}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                    docker build \
                        --platform=linux/amd64 \
                        --build-arg BUILDKIT_INLINE_CACHE=1 \
                        -t ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG} ./flask-app
                    """
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh """
                    echo "${DOCKERHUB_CREDENTIALS_PSW}" | docker login -u "${DOCKERHUB_CREDENTIALS_USR}" --password-stdin
                    docker push ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG}
                    docker logout
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully. Image ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG} pushed to DockerHub."
        }
        failure {
            echo "Pipeline failed. Check logs for more details."
        }
    }
}

