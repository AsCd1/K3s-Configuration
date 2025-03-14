# Kompose

## ⚙️ Pre-requisiti

- [Sito ufficiale](https://kompose.io/)
- [Repository GitHub](https://github.com/kubernetes/kompose?tab=readme-ov-file)
- [Guida all'installazione su GitHub](https://github.com/kubernetes/kompose/blob/main/docs/installation.md#github-release)
- [Getting Started](https://github.com/kubernetes/kompose/blob/main/docs/getting-started.md)
- [Documentazione per Compose.YAML](https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/)

## 🔹 Installation

Kompose è rilasciato tramite GitHub:

```bash
curl -L https://github.com/kubernetes/kompose/releases/download/v1.35.0/kompose-linux-amd64 -o kompose

chmod +x kompose
sudo mv ./kompose /usr/local/bin/kompose

kompose version
>> 1.35.0
```
## 🔹 Esempio
###📌 Link Utili
- [🔗docker-compose.yaml](../Esempi/kompose/docker-compose.yaml)
### 📌 Creazione Repository
```bash
mkdir kompose-example
cd kompose-example
nano docker-compose.yaml  # (vedi compose.yaml sopra)
kompose convert
>> INFO Kubernetes file "redis-leader-service.yaml" created
>> INFO Kubernetes file "redis-replica-service.yaml" created
>> INFO Kubernetes file "web-tcp-service.yaml" created
>> INFO Kubernetes file "redis-leader-deployment.yaml" created
>> INFO Kubernetes file "redis-replica-deployment.yaml" created
>> INFO Kubernetes file "web-deployment.yaml" created
```
### 📌 Configurazione
```bash
kubectl apply -f web-tcp-service.yaml,redis-leader-service.yaml,redis-replica-service.yaml,web-deployment.yaml,redis-leader-deployment.yaml,redis-replica-deployment.yaml
service/web-tcp created
service/redis-leader created
service/redis-replica created
deployment.apps/web created
deployment.apps/redis-leader created
deployment.apps/redis-replica created
```
### 📌 Verifica dei servizi
```bash
kubectl describe svc web-tcp
...
Type:                     LoadBalancer
LoadBalancer Ingress:     192.168.1.240 (VIP)
Events:
  Type    Reason        Age   From                Message
  ----    ------        ----  ----                -------
  Normal  IPAllocated   12s   metallb-controller  Assigned IP ["192.168.1.240"]
  Normal  nodeAssigned  9s    metallb-speaker     announcing from node "ubuntuworker" with protocol "layer2"
```
### 📌 Test dell'accesso al servizio
```bash
curl http://192.168.1.240:8080
kubectl delete -f web-tcp-service.yaml,redis-leader-service.yaml,redis-replica-service.yaml,web-deployment.yaml,redis-leader-deployment.yaml,redis-replica-deployment.yaml
```


