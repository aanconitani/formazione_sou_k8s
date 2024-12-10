import sys
from kubernetes import client, config
from kubernetes.client.rest import ApiException

def check_deployment_attributes(deployment):
    issues = []
    containers = deployment.spec.template.spec.containers
    for container in containers:
        # Check Liveness Probe
        if not container.liveness_probe:
            issues.append(f"Missing Liveness Probe in container {container.name}")
        # Check Readiness Probe
        if not container.readiness_probe:
            issues.append(f"Missing Readiness Probe in container {container.name}")
        # Check Resources (Limits and Requests)
        if not container.resources:
            issues.append(f"Missing resource requirements in container {container.name}")
        else:
            if not container.resources.limits:
                issues.append(f"Missing resource limits in container {container.name}")
            if not container.resources.requests:
                issues.append(f"Missing resource requests in container {container.name}")
    return issues

def main():
    # Load the Kubernetes configuration
    try:
        config.load_incluster_config()  # For in-cluster authentication
    except:
        config.load_kube_config()  # For local kubeconfig
    
    # Initialize the API client
    apps_v1 = client.AppsV1Api()
    
    # Define the namespace and deployment name
    namespace = "formazione-sou"  
    deployment_name = "flask-app" 
    
    try:
        # Get the Deployment
        deployment = apps_v1.read_namespaced_deployment(name=deployment_name, namespace=namespace)
        
        # Check the Deployment attributes
        issues = check_deployment_attributes(deployment)
        if issues:
            print("Errors found in Deployment:")
            for issue in issues:
                print(f"  - {issue}")
            sys.exit(1)
        else:
            print("Deployment meets all requirements.")
    
    except ApiException as e:
        print(f"Exception when calling AppsV1Api->read_namespaced_deployment: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
