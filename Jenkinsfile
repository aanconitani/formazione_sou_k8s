pipeline {
    agent any

    environment {
        REGISTRY_URL = 'https://hub.docker.com/repository/docker/aanconitani/jenkins-app'  // E.g., DockerHub registry or your custom registry
        IMAGE_NAME = 'flask-app'      // E.g., flask-app
        BUILD_TAG = 'latest'                // You can change this dynamically based on branch/tag
        BUILD_ARGS = ''                     // Build arguments, if needed
    }

    stages {
        stage('Build and Push Docker Image') {
            steps {
                script {
                    // Call the buildAndPushTag function
                    buildAndPushTag(
                        registryUrl: env.REGISTRY_URL,
                        image: env.IMAGE_NAME,
                        buildTag: env.BUILD_TAG,
                        dockerfileDir: "./flask-app",  // Specify the directory where Dockerfile is located
                        dockerfileName: "Dockerfile",
                        buildArgs: env.BUILD_ARGS,
                        pushLatest: true
                    )
                }
            }
        }

        // Additional stages as needed, for example:
        // stage('Test') { steps { ... } }
        // stage('Deploy') { steps { ... } }
    }
}

def buildAndPushTag(Map args) {
    def defaults = [
        registryUrl: '***',  // Default registry URL
        dockerfileDir: "./",  // Default to the current directory
        dockerfileName: "Dockerfile",  // Default Dockerfile name
        buildArgs: "",       // Default build arguments
        pushLatest: true      // Default to pushing the "latest" tag
    ]
    args = defaults + args

    docker.withRegistry(args.registryUrl) {
        def image = docker.build(args.image, "${args.buildArgs} ${args.dockerfileDir} -f ${args.dockerfileName}")
        image.push(args.buildTag)
        
        if(args.pushLatest) {
            image.push("latest")
            sh "docker rmi --force ${args.image}:latest"
        }
        
        sh "docker rmi --force ${args.image}:${args.buildTag}"

        return "${args.image}:${args.buildTag}"
    }
}
