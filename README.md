# MicroDeploy-HelmIstio

## Description
This repository contains a microservice-based application deployed on Kubernetes using Helm and Istio. The project includes three microservices: `order-service`, `payment-service`, and `user-service`. Each service is containerized with Docker and managed within a Kubernetes cluster, leveraging Istio for service mesh capabilities like traffic management, observability, and security.

## Project Structure
```
MicroDeploy-HelmIstio/
├── order-service/
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
├── payment-service/
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
├── user-service/
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
├── charts/
│   ├── order-service/
│   ├── payment-service/
│   ├── user-service/
│   ├── istio-config/
└── README.md
```

- **`order-service/`**: Contains the Order Service microservice with its Dockerfile, main application code (`main.py`), and Python dependencies (`requirements.txt`).
- **`payment-service/`**: Contains the Payment Service microservice with its Dockerfile, main application code (`main.py`), and Python dependencies (`requirements.txt`).
- **`user-service/`**: Contains the User Service microservice with its Dockerfile, main application code (`main.py`), and Python dependencies (`requirements.txt`).
- **`charts/`**: Contains Helm charts for deploying each microservice and Istio configurations (e.g., VirtualServices, DestinationRules).

## Prerequisites
- Docker: For building container images.
- Kubernetes: A running cluster (e.g., Minikube, Kind, or a cloud provider like GKE/EKS/AKS).
- Helm: For deploying the microservices and Istio.
- Istio: For service mesh features (installed via Helm).
- kubectl: For interacting with the Kubernetes cluster.

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/MicroDeploy-HelmIstio.git
   cd MicroDeploy-HelmIstio
   ```

2. **Build Docker Images**
   For each service (`order-service`, `payment-service`, `user-service`), build the Docker images:
   ```bash
   docker build -t your-username/order-service:latest ./order-service
   docker build -t your-username/payment-service:latest ./payment-service
   docker build -t your-username/user-service:latest ./user-service
   ```

3. **Push Images to a Container Registry**
   Push the images to a registry (e.g., Docker Hub):
   ```bash
   docker push your-username/order-service:latest
   docker push your-username/payment-service:latest
   docker push your-username/user-service:latest
   ```

4. **Install Istio**
   Install Istio using Helm:
   ```bash
   helm repo add istio https://istio-release.storage.googleapis.com/charts
   helm install istio-base istio/base -n istio-system --create-namespace
   helm install istiod istio/istiod -n istio-system --wait
   helm install istio-ingress istio/gateway -n istio-ingress --create-namespace
   ```

5. **Enable Istio Injection**
   Enable automatic Istio sidecar injection for the namespace where microservices will be deployed:
   ```bash
   kubectl create namespace microservices
   kubectl label namespace microservices istio-injection=enabled
   ```

6. **Deploy Microservices with Helm**
   Deploy each microservice using the Helm charts in the `charts/` directory:
   ```bash
   helm install order-service ./charts/order-service -n microservices
   helm install payment-service ./charts/payment-service -n microservices
   helm install user-service ./charts/user-service -n microservices
   ```

7. **Apply Istio Configurations**
   Apply Istio resources (e.g., VirtualServices, DestinationRules) for traffic management:
   ```bash
   kubectl apply -f charts/istio-config -n microservices
   ```

8. **Verify Deployment**
   Check the status of the deployed services:
   ```bash
   kubectl get pods -n microservices
   kubectl get svc -n microservices
   ```

9. **Access the Application**
   Access the application via the Istio ingress gateway:
   ```bash
   export INGRESS_HOST=$(kubectl -n istio-ingress get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
   curl http://$INGRESS_HOST/order
   ```

## Istio Features
- **Traffic Management**: Uses VirtualServices and DestinationRules to route traffic between `order-service`, `payment-service`, and `user-service`.
- **Observability**: Integrates with Kiali, Prometheus, and Jaeger for monitoring (configured via Helm charts).
- **Security**: Enforces mTLS between services for secure communication.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any improvements or bug fixes.

## License
This project is licensed under the MIT License.
