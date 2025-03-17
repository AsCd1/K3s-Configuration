# Kompose

## ⚙️ Pre-requisiti

- [Sito ufficiale](https://kompose.io/)
- [Repository GitHub](https://github.com/kubernetes/kompose?tab=readme-ov-file)
- [Guida all'installazione su GitHub](https://github.com/kubernetes/kompose/blob/main/docs/installation.md#github-release)
- [Getting Started](https://github.com/kubernetes/kompose/blob/main/docs/getting-started.md)
- [Documentazione per Compose.YAML](https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/)
- Una versione di kuberntes

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
### 📌 Link Utili
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
>> service/web-tcp created
>> service/redis-leader created
>> service/redis-replica created
>> deployment.apps/web created
>> deployment.apps/redis-leader created
>>  deployment.apps/redis-replica created
```
### 📌 Verifica dei servizi
```bash
kubectl describe svc web-tcp
...
Type:                     LoadBalancer
LoadBalancer Ingress:     x.x.x.x (VIP)
Events:
  Type    Reason        Age   From                Message
  ----    ------        ----  ----                -------
  Normal  IPAllocated   12s   metallb-controller  Assigned IP ["x.x.x.x"]
  Normal  nodeAssigned  9s    metallb-speaker     announcing from node "ubuntuworker" with protocol "layer2"
```
### 📌 Test dell'accesso al servizio
```bash
curl http://x.x.x.x:8080
kubectl delete -f web-tcp-service.yaml,redis-leader-service.yaml,redis-replica-service.yaml,web-deployment.yaml,redis-leader-deployment.yaml,redis-replica-deployment.yaml
```

## 🚀 S4T - Stack4Things Deployment

Questa guida descrive come clonare, configurare e avviare **Stack4Things** su Kubernetes.  

---

### 📌 **1. Clonare il repository**
Cloniamo il repository ufficiale di Stack4Things:  

```bash
git clone https://github.com/MDSLab/Stack4Things_Container_Deployment.git
```

Spostiamoci nella cartella del progetto:
```bash
cd Stack4Things_Container_Deployment/
git checkout e6c8ad509e63fc5d77cfbe65a29470dee97f76ff  #(basta il token, magari cambiare)
```

### ⚙️ **2. Configurare le variabili d’ambiente** (VERIFICARE L'ONRDINE DI QUESTO COMANDO)
Carichiamo le variabili d'ambiente definite nel file .env:
```bash
export $(grep -v '^#' .env | xargs)   # Versione con `:`
                # Alternativa:
export $(grep -v '^#' .env | sed 's/: /=/' | tr -d '"' | xargs)   # Versione con `=`
```

### 🔄 3. Convertire il file docker-compose.yml in manifest Kubernetes
Kompose ci permette di convertire un file docker-compose in configurazioni Kubernetes:
```bash
kompose convert -f docker-compose.yml
```
Controlliamo il file iotronic-db-deployment.yaml per assicurarci che tutti i campi siano stati compilati correttamente:
```bash
cat iotronic-db-deployment.yaml
```

Se tutto è corretto, applichiamo i file al cluster:
```bash
kubectl apply -f .
```

Verifichiamo che i pod siano in esecuzione:
```bash
kubectl get pods
```

Verifichiamo i servizi (service) disponibili:
```bash
kubectl get svc
```

### 🛠 4. Creazione del Gateway e VirtualService per Istio
- 📁 Definizione file yaml [qui](./istioconf)

Creiamo una cartella per i file di configurazione di Istio:
```bash
mkdir istioconf
```

Apriamo un nuovo file per definire il Gateway e il VirtualService:
```bash
nano gateway-virtualservice-istio.yaml
kubectl apply -f .
```

Verifichiamo che le risorse siano state create correttamente:
```bash
kubectl describe virtualservice iotronic-ui
```

### 📡 5. Controllo del Servizio Istio-Ingress
Verifichiamo il servizio istio-ingress per ottenere l'IP pubblico del bilanciatore di carico:
```bash
kubectl get svc istio-ingress -n istio-ingress
```
🔎 Esempio di output:
```bash
NAME            TYPE           CLUSTER-IP    EXTERNAL-IP     PORT(S)                                      AGE
istio-ingress   LoadBalancer   10.x.x.x      x.x.x.x         15021:30152/TCP,80:31152/TCP,443:30936/TCP   3d3h
```

Verifichiamo la creazione del VirtualService:
```bash
kubectl get virtualservice
```

🔎 Esempio di output:
```bash
NAME          GATEWAYS                  HOSTS   AGE
iotronic-ui   ["iotronic-ui-gateway"]   ["*"]   11m
```

Controlliamo il Gateway:
```bash
kubectl get gateway
```

🔎 Esempio di output:
```bash
NAME                  AGE
iotronic-ui-gateway   12m
```

### 🌍 6. Test dell’accesso al servizio
Utilizziamo curl per testare l'accesso alla UI di Iotronic tramite l'IP di istio-ingress:
```bash
curl x.x.x.x/iotronic-ui
```

🔎 Output atteso:
```bash
>> Apache Default Page
```

🔄 7. Configurare il Port Forwarding --opzionale tramite tailscale
Per esporre il servizio localmente:
```bash
kubectl port-forward --address 0.0.0.0 svc/istio-ingress 8100:80 -n istio-ingress
```

Ora possiamo accedere alla UI da un browser utilizzando gli indirizzi seguenti:
```bash
>> http://100.122.136.8:8100/iotronic-ui
>> http://100.122.136.8:8100/horizon/auth/login/?next=/horizon/
```
