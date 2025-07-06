#!/bin/bash

set -e

echo "📦 Installing Helm..."
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
echo "✅ Helm installed:"
helm version

echo "🚀 Installing Istio (demo profile)..."
istioctl install --set profile=demo -y

echo "📁 Creating Kubernetes namespaces..."
kubectl create namespace mongo || true
kubectl create namespace api || true

echo "🏷️ Enabling Istio sidecar injection for namespaces..."
kubectl label namespace api istio-injection=enabled 
kubectl label namespace mongo istio-injection=enabled 

echo "📡 Configuring DNS for istio-ingressgateway..."

DNS_NAME="microservice-gateway.k8s.dns"
NAMESPACE="istio-system"
SERVICE_NAME="istio-ingressgateway"
HOSTS_FILE="/etc/hosts"

# Check for kubectl
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Install kubectl and try again."
    exit 1
fi

# Get IP of istio-ingressgateway
IP=$(kubectl -n "$NAMESPACE" get service "$SERVICE_NAME" -o jsonpath='{.spec.clusterIP}')
if [ -z "$IP" ]; then
    echo "❌ Failed to get ClusterIP for $SERVICE_NAME."
    exit 1
fi

# Clean old entry if exists
sudo sed -i "/$DNS_NAME/d" "$HOSTS_FILE"

# Add new DNS entry
echo "$IP $DNS_NAME" | sudo tee -a "$HOSTS_FILE" > /dev/null

# Confirm entry added
if grep -q "$DNS_NAME" "$HOSTS_FILE"; then
    echo "✅ DNS mapped: $IP $DNS_NAME"
else
    echo "❌ Failed to update $HOSTS_FILE with DNS."
    exit 1
fi

echo "📦 Adding Helm repo and deploying FastAPI microservice..."
helm repo add fast-api-microservice-app https://omkar-shelke25.github.io/Helm-Istio-Microservice-App-deploy/
helm repo update

helm install fastapi-microservice-app fast-api-microservice-app/fastapi-microservice-app \
  --version 1.3.0

echo "🎉 Deployment complete!"
