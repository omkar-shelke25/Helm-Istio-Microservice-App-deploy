# Microservice Application with Helm, Istio, and Kubernetes

Welcome to the **Microservice Application**, a modern, cloud-native system featuring three interconnected services: `order-service`, `payment-service`, and `user-service`. Built with **FastAPI**, containerized using **Docker**, and deployed on **Kubernetes** with **Helm** for package management and **Istio** for service mesh capabilities, this application demonstrates scalable microservice architecture with advanced traffic management, observability, and security.

## Repository Structure

- `deployment.sh`: Automates Helm/Istio installation, namespace setup, and microservice deployment.
- `fastapi-microservice-app-*.tgz`: Helm chart versions (`1.0.0`, `1.2.0`, `1.3.0` - latest).
- `index.yaml`: Helm chart repository index.
- `microservice-app/`: Unpacked Helm chart for microservices.
- `notes.md`: Detailed setup, security, and networking notes.
- `src/`: Source code for `order-service`, `payment-service`, and `user-service`.
- `Dockerfile` (per service): Docker configurations for containerizing microservices.

## Microservices Overview

1. **Order Service**:
   - **Function**: Manages order creation, retrieval, and updates.
   - **Interactions**: Communicates with `payment-service` for payment processing and `user-service` for user validation.
   - **API**: RESTful endpoints (e.g., `/orders`).

2. **Payment Service**:
   - **Function**: Processes payments and tracks transaction status (mocked for demo purposes).
   - **Interactions**: Confirms payments with `order-service`.
   - **API**: RESTful endpoints (e.g., `/payments`).

3. **User Service**:
   - **Function**: Manages user profiles, authentication, and authorization.
   - **Interactions**: Provides user data to `order-service`.
   - **API**: RESTful endpoints (e.g., `/users`).

Each service is built with **FastAPI**, containerized with **Docker**, and deployed as Kubernetes pods managed by Helm charts.

## Prerequisites

Ensure the following are set up before deployment:
- A running **Kubernetes cluster** (e.g., Minikube, Kind, EKS, GKE, AKS).
- **kubectl**: Installed and configured to access your cluster.
- **Docker**: For building and pushing container images.
- **Helm**: Installed (or installed automatically by `deployment.sh`).
- **Istio**: Installed via `deployment.sh` for service mesh features.
- **sudo**: Required for modifying `/etc/hosts` for DNS configuration.
- **Internet Access**: To download Helm, Istio, and Helm chart dependencies.

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
- **Installs Helm**: Downloads and verifies Helm installation.
- **Installs Istio**: Deploys Istio with the `demo` profile for service mesh features like traffic management and observability.
- **Creates Namespaces**: Sets up `mongo` and `api` namespaces with Istio sidecar injection enabled.
- **Configures DNS**: Maps `microservice-gateway.k8s.dns` to the Istio ingress gateway's ClusterIP in `/etc/hosts`.
- **Deploys Microservices**: Adds the Helm chart repository (`https://omkar-shelke25.github.io/Helm-Istio-Microservice-App-deploy/`) and installs version `1.3.0` of the microservices.

## Accessing the Application

- **Base URL**: `http://microservice-gateway.k8s.dns`
- **Endpoints**:
  - `order-service`: `/orders`
  - `payment-service`: `/payments`
  - `user-service`: `/users`
- **DNS Requirement**: Ensure `/etc/hosts` includes the mapping for `microservice-gateway.k8s.dns` to the `istio-ingressgateway` ClusterIP.

### Example API Calls

Below are example API calls with their expected outputs, as demonstrated in the provided screenshots.

1. **Create a User**:
   ```bash
   curl -X POST http://microservice-gateway.k8s.dns/users/ \
   -H "Content-Type: application/json" \
   -d '{"name":"John Doe","email":"john@example.com"}' | jq
   ```
   ```bash
   curl -X POST http://microservice-gateway.k8s.dns/users/ \
   -H "Content-Type: application/json" \
   -d '{"name":"Omkar","email":"shelke"}' | jq
   ```
   *Output*: Creates users and stores them in MongoDB.
   ![User Creation Output](https://github.com/user-attachments/assets/63a021d9-8943-41d8-b975-971f1ef86fdc)

2. **List Users**:
   ```bash
   curl -X GET http://microservice-gateway.k8s.dns/users/ | jq
   ```
   *Output*: Displays a list of created users.
   ![User List Output](https://github.com/user-attachments/assets/4d769f5b-72e1-4269-a609-0f3ecfaed1fa)

3. **Create an Order** (requires `user_id` from user service):
   ```bash
   curl -X POST http://microservice-gateway.k8s.dns/orders/ \
   -H "Content-Type: application/json" \
   -d '{"user_id":"686aa16b1858e2c497a1cd93","product":"Laptop","amount":999.99}' | jq
   ```
   *Output*: Creates an order linked to a user.
   ![Order Creation Output](https://github.com/user-attachments/assets/ca4b4d37-eaee-4c46-9a45-a1b0b789d6fc)

4. **List Orders**:
   ```bash
   curl -X GET http://microservice-gateway.k8s.dns/orders/ | jq
   ```
   *Output*: Shows orders associated with user IDs.
   ![Order List Output](https://github.com/user-attachments/assets/545f0dd0-b852-4d00-bbdf-729a8404a8ec)

5. **Process a Payment** (requires `order_id` from order service):
   ```bash
   curl -X POST http://microservice-gateway.k8s.dns/payments/ \
   -H "Content-Type: application/json" \
   -d '{"order_id":"686aa21c9fb5eb202be21db8","amount":999.99,"status":"successful"}' | jq
   ```
   *Output*: Confirms payment for an order.
   ![Payment Creation Output](https://github.com/user-attachments/assets/afb43e81-366c-4411-ac8c-9b67438d69ca)

6. **List Payments**:
   ```bash
   curl -X GET http://microservice-gateway.k8s.dns/payments/ | jq
   ```
   *Output*: Displays payment records.
   ![Payment List Output](https://github.com/user-attachments/assets/b27c415a-d3c9-4feb-b35e-997588d6e677)

## Istio Features

- **Traffic Management**: Leverages `VirtualService` and `DestinationRule` for intelligent routing and load balancing.
- **Observability**: Integrates with Kiali, Prometheus, or Jaeger for metrics, logs, and tracing.
- **Security**: Enforces mutual TLS (mTLS) for secure service-to-service communication.


## Troubleshooting

- **kubectl Issues**: Ensure `kubectl` is installed and configured (`kubectl config view`).
- **DNS Errors**: Verify `/etc/hosts` entries and `sudo` permissions.
- **Helm Failures**: Check repository accessibility (`helm repo list`) and chart version.
- **Istio Issues**: Inspect the `istio-system` namespace (`kubectl get pods -n istio-system`).
- **Pod Failures**: Check logs with `kubectl logs <pod-name> -n api`.
- **MongoDB Issues**: Verify the `mongo` namespace and pod status (`kubectl get pods -n mongo`).

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Description"`).
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.




