# Microservice Application with Helm, Istio, and Kubernetes

This repository contains a microservice-based application consisting of three services: `order-service`, `payment-service`, and `user-service`. Each service is containerized using Docker and deployed on a Kubernetes cluster using Helm for package management and Istio for service mesh capabilities, including traffic management, observability, and security.

## Repository Structure

- `deployment.sh`: Bash script to install Helm, deploy Istio, configure namespaces, and deploy the microservices.
- `fastapi-microservice-app-1.0.0.tgz`: Helm chart version 1.0.0 (initial release).
- `fastapi-microservice-app-1.2.0.tgz`: Helm chart version 1.2.0 (minor updates).
- `fastapi-microservice-app-1.3.0.tgz`: Helm chart version 1.3.0 (latest patch).
- `index.yaml`: Helm chart repository index.
- `microservice-app/`: Unpacked Helm chart directory for the microservices.
- `notes.md`: Notes on setup, security, and networking configurations.
- `src/`: Source code for `order-service`, `payment-service`, and `user-service` (FastAPI-based).
- `Dockerfile` (per service): Docker configuration for containerizing each microservice.

## Microservices Overview

1. **Order Service**:
   - Manages order creation, retrieval, and updates.
   - Interacts with `payment-service` for payment processing and `user-service` for user validation.
   - Exposed via RESTful APIs.

2. **Payment Service**:
   - Handles payment processing and transaction status.
   - Communicates with external payment gateways (mocked for demo purposes).
   - Integrates with `order-service` for payment confirmation.

3. **User Service**:
   - Manages user profiles, authentication, and authorization.
   - Provides user data to `order-service` for order validation.

Each service is built with **FastAPI**, containerized using **Docker**, and deployed as a Kubernetes pod managed by Helm charts.

## Prerequisites

- **Kubernetes Cluster**: A running cluster (e.g., Minikube, Kind, EKS, GKE, or AKS).
- **kubectl**: Installed and configured to interact with your cluster.
- **Docker**: For building and pushing container images.
- **Helm**: For deploying the application (installed by `deployment.sh` if not present).
- **Istio**: For service mesh features (installed by `deployment.sh`).
- **sudo**: Required for modifying `/etc/hosts` for DNS configuration.
- **Internet Access**: To download Helm, Istio, and the Helm chart repository.

## Deployment Instructions

The `deployment.sh` script automates the setup and deployment process. Follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Make the Script Executable**:
   ```bash
   chmod +x deployment.sh
   ```

3. **Run the Deployment Script**:
   ```bash
   ./deployment.sh
   ```

### What the Script Does

1. **Installs Helm**:
   - Downloads and installs Helm using the official script.
   - Verifies installation with `helm version`.

2. **Installs Istio**:
   - Deploys Istio with the `demo` profile using `istioctl`.
   - Enables service mesh features like traffic management and observability.

3. **Creates Kubernetes Namespaces**:
   - Creates `mongo` and `api` namespaces (if they don't exist).
   - Enables Istio sidecar injection for both namespaces.

4. **Configures DNS**:
   - Maps `microservice-gateway.k8s.dns` to the `istio-ingressgateway` ClusterIP in `/etc/hosts`.
   - Verifies the DNS entry.

5. **Deploys the Microservices**:
   - Adds the Helm chart repository: `https://omkar-shelke25.github.io/Helm-Istio-Microservice-App-deploy/`.
   - Installs the microservices using the Helm chart version 1.3.0.
   - Deploys `order-service`, `payment-service`, and `user-service` as Kubernetes workloads.

## Accessing the Application

- Access the microservices via the Istio ingress gateway at `microservice-gateway.k8s.dns`.
- Ensure `/etc/hosts` contains the mapping to the `istio-ingressgateway` ClusterIP.
- Example endpoints (depending on configuration):
  - `order-service`: `http://microservice-gateway.k8s.dns/orders`
  - `payment-service`: `http://microservice-gateway.k8s.dns/payments`
  - `user-service`: `http://microservice-gateway.k8s.dns/users`

## Istio Features

- **Traffic Management**: Uses Istio's VirtualService and DestinationRule for routing and load balancing.
- **Observability**: Integrates with Istio for metrics, logs, and tracing (e.g., via Kiali or Prometheus).
- **Security**: Enforces mutual TLS (mTLS) for service-to-service communication.

## Building and Pushing Docker Images

Each microservice has its own `Dockerfile` in the `src/` directory. To build and push images:

1. **Build Docker Images**:
   ```bash
   cd src/order-service
   docker build -t <your-registry>/order-service:latest .
   cd ../payment-service
   docker build -t <your-registry>/payment-service:latest .
   cd ../user-service
   docker build -t <your-registry>/user-service:latest .
   ```

2. **Push to Registry**:
   ```bash
   docker push <your-registry>/order-service:latest
   docker push <your-registry>/payment-service:latest
   docker push <your-registry>/user-service:latest
   ```

3. Update the Helm chart (`microservice-app/values.yaml`) with your image repository details before running `deployment.sh`.

## Notes

- Refer to `notes.md` for additional setup, security, and networking details.
- Ensure `kubectl` is configured to access your Kubernetes cluster.
- The script requires `sudo` privileges to modify `/etc/hosts`.
- Customize Helm chart values (e.g., `microservice-app/values.yaml`) for specific configurations like resource limits or replicas.

## Troubleshooting

- **kubectl not found**: Install `kubectl` and add it to your PATH.
- **DNS mapping failure**: Verify `sudo` permissions and check `/etc/hosts`.
- **Helm chart issues**: Ensure the Helm repository is accessible and the chart version is correct.
- **Istio issues**: Verify the `istio-system` namespace and `istio-ingressgateway` service.
- **Pod failures**: Check pod logs with `kubectl logs <pod-name> -n api`.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for enhancements, bug fixes, or documentation improvements.
