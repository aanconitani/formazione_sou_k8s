pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub') // Configure your Jenkins credentials ID
        DOCKER_IMAGE_NAME = 'aanconitani/flask-app'
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
                    echo "Podman Image Tag: ${env.DOCKER_IMAGE_TAG}"
                }
            }
        }

        stage('Build Podman Image') {
            steps {
                script {
                    sh """
                    podman build \
                        --platform=linux/arm64 \
                        --build-arg BUILDKIT_INLINE_CACHE=1 \
                        -f flask-app/Dockerfile \
                        -t ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG} \
                        flask-app
                    """
                }
            }
        }

        stage('Push Podman Image') {
            steps {
                script {
                    sh """
                    echo "${DOCKERHUB_CREDENTIALS_PSW}" | podman login docker.io -u "${DOCKERHUB_CREDENTIALS_USR}" --password-stdin
                    podman push ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG}
                    podman logout docker.io
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
