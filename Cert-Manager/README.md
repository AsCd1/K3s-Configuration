# 🔐 Install Cert-Manager  
 
- This step is only required to use certificates issued by Rancher's generated CA (`ingress.tls.source=rancher`) or to request Let's Encrypt issued certificates (`ingress.tls.source=letsEncrypt`).  

## 📌 Passaggi per l'installazione:
```bash
# Set the KUBECONFIG environment variable
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

# Apply the Cert-Manager Custom Resource Definitions (CRDs)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.crds.yaml

# Add the Jetstack Helm repository
helm repo add jetstack https://charts.jetstack.io

# Update your local Helm chart repository cache
helm repo update

# Install Cert-Manager using Helm
helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace

# Verify Cert-Manager pods are running
kubectl get pods --namespace cert-manager
>> OUTPUT: 3 PODS IN RUNNING STATE

# Check installed Custom Resource Definitions (CRDs)
kubectl get crds | grep cert-manager
>> OUTPUT: 6 cert-manager CRDs found
```
