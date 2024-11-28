pipeline {
    agent any

    environment {
        REGISTRY_URL = 'https://hub.docker.com/repository/docker/aanconitani/jenkins-app'  // E.g., Podman registry or your custom registry
        IMAGE_NAME = 'flask-app'      // E.g., flask-app
        BUILD_TAG = 'latest'          // Change dynamically based on branch/tag
        BUILD_ARGS = ''               // Build arguments, if needed
    }

    stages {
        stage('Build and Push Image') {
            steps {
                script {
                    // Call the buildAndPushTag function
                    buildAndPushTag(
                        registryUrl: env.REGISTRY_URL,
                        image: env.IMAGE_NAME,
                        buildTag: env.BUILD_TAG,
                        dockerfileDir: "./flask-app",  // Specify Dockerfile directory
                        dockerfileName: "Dockerfile",
                        buildArgs: env.BUILD_ARGS,
                        pushLatest: true
                    )
                }
            }
        }

        // Additional stages as needed, e.g., Test, Deploy, etc.
    }
}

// Updated function to use Podman instead of Docker
def buildAndPushTag(Map args) {
    def defaults = [
        registryUrl: '***',        // Default registry URL
        dockerfileDir: "./",       // Default to the current directory
        dockerfileName: "Dockerfile",  // Default Dockerfile name
        buildArgs: "",             // Default build arguments
        pushLatest: true           // Default to pushing the "latest" tag
    ]
    args = defaults + args

    // Use Podman to build and push the image
    podman.withRegistry(args.registryUrl) {
        // Build the image using Podman
        def image = podman.build(args.image, "${args.buildArgs} ${args.dockerfileDir} -f ${args.dockerfileName}")
        
        // Push the image with the specific tag
        image.push(args.buildTag)

        // Optionally push the latest tag
        if (args.pushLatest) {
            image.push("latest")
            sh "podman rmi --force ${args.image}:latest" // Remove the latest tag locally
        }

        // Remove the image with the specific build tag locally
        sh "podman rmi --force ${args.image}:${args.buildTag}"

        return "${args.image}:${args.buildTag}"
    }
}
