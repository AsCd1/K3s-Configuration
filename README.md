# K3s Configuration Guide

Di seguito sonno fornite diverse guide:
- una configurazione veloce di k3s, vedi [K3s Rapid Setup](#k3s-rapid-setup-)
- una configurazzione completa, vedi [K3s Multi-Cluster Setup Guide](#k3s-multi-cluster-setup-guide-)

## K3s Deployment Guide

| **K3s Deployment Guide** | **Steps**                                 |
|--------------------------|-------------------------------------------|
| 📁 **K3s-S4T Rapid Setup ⚡** | 1. 🚀 Installazione di K3s             |
|                          | 2. 🔗 Clonazione S4T - OPZIONE2           |
|                          | 3. 🔄 Conversione YAML (Kompose) - none   |
|                          | 4. 📌 Deploy su Kubernetes                |
|                          | 5. ✅ Verifica dei Pod e dei Servizi      |
|                          |                                           |
| 📁 **K3s-Calico-MetalLB-Istio-S4T Multi-Cluster Setup** | 1. ⚙️ Installazione di K3s (senza Traefik) |
|                          | 2. 🌐 Configurazione di Calico            |
|                          | 3. 📡 Setup di MetalLB                    |
|                          | 4. 🚀 Deploy di Istio                    |
|                          | 5. 🔗 Clonazione S4T - OPZIONE2           |
|                          | 6. 🔄 Conversione YAML (Kompose) - none   |
|                          | 7. 📌 Deploy su Kubernetes                |
|                          | 8. ✅ Verifica dei Pod e dei Servizi      |




# K3s Rapid Setup ⚡
- [Quick-Start-K3s](https://docs.k3s.io/quick-start)

## 🚀 Installazione di K3s (Master Node Unico)
```bash
curl -sfL https://get.k3s.io | sh -
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
kubectl get nodes
```
🔹 Cosa fa questo comando?
- Installa K3s come master node
- Avvia automaticamente il servizio
- ⚠️ Nota: Configura kubectl per gestire il cluster
 S4T - Stack4Things Deployment 
- ⚠️ Nota: In questa configurazione non sono presenti Calico, istio e MetalLb necessari per alcuni esempi
- ⚠️ Con questa configurazione si otterrà S4T con servizi interni al cluster in una configurazione minimale ma configurabile a piacere.

## [Muoversi direttamente alla sezione S4t](#-s4t---stack4things-deployment)

# K3s Multi-Cluster Setup Guide 🛠
Con la seguente guida si otterrà una configurazione con:
1. Calico come CNI
2. MeatalLB come Loadbalancer
3. Istio come Gateway
4. S4T

## Guida al Setup di un Cluster K3s

Questa guida ti aiuterà a configurare un cluster K3s utilizzando una macchina come **server** (control plane) e una o più macchine come **worker nodes**.

### Nota:
1. Se preferisci eseguire un'installazione pulita di Calico, salta alla sezione dedicata a Calico più avanti.
2. Potrebbe essere necessario utilizzare gli IP interni delle macchine. (LASCIARE?)

## 1. Installazione del Server K3s

### Configurazione del Server (Control Plane)

1. **Accedi alla VM che fungerà da server**, chiamato anche *server host*. Utilizza SSH per connetterti alla macchina.

2. **Esegui il seguente comando** per installare K3s sul server:

    ```bash
    curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server --disable traefik --disable servicelb" sh -
    ```

    Questo comando installerà K3s sul server host e disabiliterà Traefik e il bilanciamento del servizio (service load balancer).

## 2. Recupera il Token del Nodo

Dopo aver installato K3s sul server, recupera il **token del nodo** che sarà utilizzato per aggiungere i worker nodes al cluster.

1. **Esegui il seguente comando** sul server per ottenere il token:

    ```bash
    cat /var/lib/rancher/k3s/server/node-token
    ```

    oppure:

    ```bash
    sudo cat /var/lib/rancher/k3s/server/node-token
    ```

2. Il **token** che otterrai servirà per il comando successivo = `YourToken`.

## 3. Recupera il Certificato del Cluster

Per poter comunicare con il cluster, è necessario recuperare il certificato di configurazione di K3s.

1. **Esegui il seguente comando** per ottenere il file di configurazione:

    ```bash
    cat /etc/rancher/k3s/k3s.yaml
    ```

    oppure:

    ```bash
    sudo cat /etc/rancher/k3s/k3s.yaml
    ```

2. **Salva il contenuto del file `k3s.yaml`** sul tuo computer nella directory `~/.kube/` come un file di configurazione personalizzato (`<nome del tuo file>.yaml`).

3. **Modifica il file** sostituendo l'IP del server con l'IP corretto del control plane (Server Host) e assicurati che il server utilizzi HTTPS.

    Esempio di modifica del file `k3s.yaml`:
    ```yaml
    server: https://<Contol Plane IP>:6443
    ```
4. **Verifica la connessione al cluster**:

   ⚠️ Configura il tuo ambiente:
    ```bash
    export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
    ```

    Esegui il comando:
    ```bash
    kubectl get nodes
    ```
   
    Esempio di output:

    ```
    NAME            STATUS  ROLES                   AGE VERSION
    ubuntuserver    Ready   control.plane,master    xx  xx
    ```

## 4. Aggiungi i Worker Node

Ora puoi aggiungere i nodi di lavoro (worker nodes) al cluster.

### Aggiungi un Nodo Worker

1. **Accedi alla VM che fungerà da worker node**. Questo è il nodo che eseguirà i carichi di lavoro, ed è diverso dal nodo server.

2. **Esegui il seguente comando** sul nodo worker:

    ```bash
    curl -sfL https://get.k3s.io | K3S_URL=https://<Contol Plane IP>:6443 K3S_TOKEN=<YourToken> sh -
    ```

    Sostituisci `<Contol Plane IP>` con l'IP del server (control plane) e `<YourToken>` con il token che hai ottenuto in precedenza.


5. **Configurazione di `kubectl` sul Worker Node**:

    - Crea un file `~/.kube/config` sul nodo worker.
    - Copia il contenuto del file `k3s.yaml` dal server (control plane) in questo file.
    - Modifica il campo `server` per includere l'IP del server.

6. **Configura `kubectl`**:

    Esegui i seguenti comandi sul nodo worker per impostare il tuo ambiente Kubernetes:

    ```bash
    export KUBECONFIG=~/.kube/config
    kubectl get nodes
    ```

    Esempio di output:

    ```
    NAME            STATUS  ROLES                   AGE VERSION
    ubuntuserver    Ready   control.plane,master    xx  xx
    ubuntuworker    Ready   <none>                  xx  xx
    ```

---

Con questi passaggi avrai un cluster K3s funzionante con un server e uno o più nodi worker.

## Calico

Calico è un plugin di rete per Kubernetes che fornisce networking e sicurezza per i pod. Può essere installato in due modi principali:

- Installazione sul control plane.
- Installazione manuale tramite manifest anche sul worker.
- Installazione tramite operator, che applica automaticamente su entrambi se eseguito sul control plane.

### Operator vs Manifest

Calico può essere installato tramite due approcci principali:

1. **Operator**: Un metodo automatizzato e gestito per l'installazione e l'aggiornamento di Calico.
2. **Manifest**: Un metodo manuale che applica direttamente i file di configurazione YAML nel cluster.

### Installazione con Operator

1. Installa l'operatore Calico e le definizioni delle risorse personalizzate.
2. Repository di Calico: [Link al repository Calico](https://github.com/projectcalico/calico/tree/master)
3. Guida all'installazione: [Guida ufficiale all'installazione di Calico su K3s](https://docs.tigera.io/calico/latest/getting-started/kubernetes/k3s/multi-node-install)
4. Installazione tramite Helm: [Guida per l'installazione tramite Helm](https://docs.tigera.io/calico/latest/getting-started/kubernetes/helm)

#### Comandi per installare l'operatore Calico:

```bash
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.2/manifests/tigera-operator.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.2/manifests/custom-resources.yaml
kubectl get nodes -o wide  # Da eseguire anche sul worker --opzionale
kubectl get pods -n calico-system -o wide
ip route show
kubectl get pods -A | grep -E "calico|flannel" #flannel è presente di default se non si segue l'installazione pulita
```

## Installing Helm   
Il [progetto Helm](https://helm.sh/docs/intro/install/) offre due metodi ufficiali per scaricare e installare Helm. Oltre a questi, la community di Helm fornisce anche altri metodi di installazione tramite diversi gestori di pacchetti.

### 🚀 Installazione tramite Script  
Helm fornisce uno script di installazione che scarica e installa automaticamente l'ultima versione di Helm sul tuo sistema.
  
Puoi scaricare lo script ed eseguirlo localmente. È ben documentato, quindi puoi leggerlo in anticipo per capire cosa fa prima di eseguirlo.
```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

Se vuoi usare l'ultima versione instabile, puoi anche eseguire:
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```
## Install Cert-Manager  
 
- Questo passaggio è necessario solo se devi utilizzare certificati emessi dalla CA generata da Rancher (ingress.tls.source=rancher) o richiedere certificati emessi da Let's Encrypt (ingress.tls.source=letsEncrypt).

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
## Installing Rancher via Helm --Opzionale

- [Link qui](https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/install-upgrade-on-a-kubernetes-cluster#3-choose-your-ssl-configuration) Site  
- [Link qui](https://artifacthub.io/packages/helm/rancher-stable/rancher) Artifact Hub  
- Aggiungi il repository Helm di Rancher:  

```bash
# Add the Rancher Helm repository
helm repo add rancher-latest https://releases.rancher.com/server-charts/latest

# Update Helm repositories
helm repo update

# Create the Rancher namespace
kubectl create namespace cattle-system

# Install Rancher using Helm
helm install rancher rancher-latest/rancher \
    --namespace cattle-system \
    --create-namespace \
    --set hostname="hostname" \
    --set bootstrapPassword="YourPassword"
```
Usare il seguente comando:
```bash
kubectl port-forward -n cattle-system svc/rancher 8443:443
>> FORWARD TRAMITE x.x.x.x:443 -> 444

# Check the rollout status of the Rancher deployment
kubectl -n cattle-system rollout status deploy/rancher
>> OUTPUT: deployment "rancher" successfully rolled out

# Get the deployment details
kubectl -n cattle-system get deploy rancher
NAME      DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
rancher   3         3         3            3           3m
```

## MetalLB
- [Documentazione qui](MetalLB/README.md)

### Installazione con Helm
```bash
# Aggiungi il repository Helm di MetalLB
helm repo add metallb https://metallb.github.io/metallb

# Installa MetalLB
helm install metallb metallb/metallb
```

### Configurazione Layer2
Creazione del file di configurazione per Layer 2:
- [metallb-configuration](./MetalLB/metallb-configuration.yaml)
```bash
echo "Apri il file di configurazione: https://github.com/AsCd1/K3s-Configuration/blob/main/MetalLB/metallb-configuration.yaml"
nano metallb-configuration.yaml
```
⚠️ **Importante:** Durante l'applicazione della configurazione si è verificato un errore risolto con un secondo apply:
- Creazione del file [L2Advertisement](./MetalLB/l2advertisement.yaml) separato.
```bash
nano l2advertisement.yaml
```
Apply della configurazione:
```bash
kubectl apply -f l2advertisement.yaml
kubectl apply -f metallb-configuration.yaml
```
Verifica della configurazione:
```bash
kubectl get ipaddresspools -n metallb-system
>> Output: Lista dei range IP

kubectl get l2advertisements -n metallb-system
>> Output: Nome e range IP
```
## Esempi
### 1. Prova per verificare il funzionamento
- [Deployment nginx-hello-deployment](Esempi/ngnix-prova/nginx-hello-deployment.yaml)
- [Git originale del deployment](https://gist.githubusercontent.com/sdenel/1bd2c8b5975393ababbcff9b57784e82/raw/f1b885349ba17cb2a81ca3899acc86c6ad150eb1/nginx-hello-world-deployment.yaml)

Creazione della directory di prova:
```bash
mkdir nginx-prova
cd nginx-prova
```
Creazione del file di configurazione:
```bash
nano nginx-hello-deployment.yaml
```
Applicazione della configurazione:
```bash
kubectl apply -f .
    oppure
kubectl apply -f nginx-hello-deployment.yaml
```
Controllo dei servizi:
```bash
kubectl get svc -A
```
Output atteso:
```
>>> default nginx   LoadBalancer    InternalIP  ExternalIP <- deve essere quello del yaml
```
Testare l'accesso al servizio:
```bash
curl 192.x.x.x
```
Output atteso:
```
>>> Hello World!
```
In caso di problemi, provare:
```bash
wget -qO- 192.x.x.x
```
Output atteso:
```
>> Hello World!
```

### 2. Hello World 3 Replicas
- [Deployment nginx-hello-deployment-3Rep](Esempi/ngnix-prova/nginx-hello-deployment-3Rep.yaml)

Applica il Deployment per aumentare le repliche a 3:
```bash
kubectl apply -f nginx-hello-world-deployment-3Rep.yaml
kubectl get pods -l app=nginx
>> OUTPUT: 3 pod
curl 192.x.x.x
>> Hello World!
```

### 3. Ottenere il nome del Pod
- [Deployment nginx-monitoring](Esempi/ngnix-prova/nginx-monitoring.yaml)

Restituzione di Hello World! con il nome del pod che lo ha eseguito:
```bash
nano ngnix-monitoring.yaml
kubectl apply -f ngnix-monitoring.yaml
curl 192.x.x.x
>> Hello world from pod: nginx-<Podid>
kubectl get pods -o wide
```

## Riepilogo della tua configurazione Kubernetes + MetalLB + Calico
Hai creato un cluster K3s con:  
- **Control Plane** su una VM  
- **Worker Node** su un'altra VM  
- **Calico** come CNI (Container Network Interface)  
- **MetalLB** per assegnare IP pubblici ai servizi di tipo LoadBalancer  

E infine, hai testato un **Deployment Nginx** con un **Servizio LoadBalancer** per verificare la corretta esposizione delle applicazioni.  

---

### 🏗️ Cluster Kubernetes (K3s)  
1. **Control Plane**: gestisce il cluster (schedulazione, stato, API Server).  
2. **Worker Node**: esegue i pod e gestisce il traffico.  
3. **Container Network Interface (CNI) - Calico**: permette la comunicazione tra i pod.  

---

### 🌐 MetalLB - LoadBalancer per Bare Metal  
- **MetalLB** gestisce gli IP pubblici su cluster Kubernetes senza cloud provider.  
- **Modalità Layer 2**:  
  - MetalLB annuncia l'IP assegnato a un servizio LoadBalancer tramite **ARP**.  
  - I nodi del cluster rispondono direttamente alle richieste ricevute.  

---

### 🚀 Test con Nginx  
- Hai creato un **Deployment Nginx** con più repliche.  
- Il **Service** con `type: LoadBalancer` ha ricevuto un **IP pubblico** da MetalLB.  
- Il traffico verso l’**IP pubblico** viene distribuito ai pod di Nginx.

## 🔹 Istio Install with Helm  

🔗 **Guida ufficiale**: [Istio Helm Installation](https://istio.io/latest/docs/setup/install/helm/)  

#### 📌 Aggiunta del repository Helm di Istio  
```bash
helm repo add istio https://istio-release.storage.googleapis.com/charts
>> Output atteso: "istio" has been added to your repositories
```

### 📌 Aggiornamento dei repository
```bash
helm repo update
>> Output atteso: Update Complete. Happy Helming!
```

### 📌 Installazione della base di Istio
```bash
helm install istio-base istio/base -n istio-system --set defaultRevision=default --create-namespace
>> Output atteso:
- NAME: istio-base
- LAST DEPLOYED: Tue Feb 25 09:19:24 2025
- NAMESPACE: istio-system
- STATUS: deployed
- REVISION: 1
- TEST SUITE: None
- NOTES:
- Istio base successfully installed!
```

### 📌 Verifica dello stato di istio-base
```bash
helm status istio-base -n istio-system
helm get all istio-base -n istio-system
helm ls -n istio-system
```
### 📌 Installazione del servizio istiod
```bash
helm install istiod istio/istiod -n istio-system --wait
```

### 📌 Verifica dell'installazione
```bash
helm ls -n istio-system
helm status istiod -n istio-system
```

### 📌 Controllo dello stato dei pod di istiod
```bash
kubectl get deployments -n istio-system --output wide
>> Output atteso:
NAME     READY   UP-TO-DATE   AVAILABLE   AGE  CONTAINERS  SELECTOR
istiod   1/1     1            1           23m  discovery   istio=pilot
```

### 📌 Creazione dello spazio dei nomi per il gateway
```bash
kubectl create namespace istio-ingress
>> Output atteso: namespace/istio-ingress created
```

### 📌 Installazione del gateway di Istio
```bash
helm install istio-ingress istio/gateway -n istio-ingress --wait
```

### 📌 Verifica dei servizi
```bash
kubectl get svc -A
>> Output atteso: Istio ha creato il suo LoadBalancer.
```

## 🎯 Cosa abbiamo ottenuto  

### 📌 Verifica dei pod di Istio Ingress  
```bash
kubectl get pods -n istio-ingress
>>OUTPUT atteso:
NAME                             READY   STATUS
istio-ingress-<PodID>   1/1     Running
```

### 📌 Verifica del Service di Istio Ingress
```bash
kubectl get svc -n istio-ingress
>> OUTPUT atteso:
NAME            TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)
istio-ingress   LoadBalancer   x.x.x.x         x.x.x.x         15021:30268/TCP,80:31240/TCP,443:32410/TCP
```

## 🚀 Hello World! in Istio

- [🔗 Gateway VirtualService YAML](https://github.com/istio/istio/blob/master/samples/helloworld/helloworld-gateway.yaml) **--Modificare il controller col tuo**
- [🔗 HelloPod YAML](https://github.com/istio/istio/blob/master/samples/helloworld/helloworld.yaml)
- [🔗 Cartella esempi](./Esempi/Istio-Esempi/) -- funzionante con l'ultima release di Istio: 17/03/25

### 📌 Creazione dei file di configurazione  
```bash
mkdir istiohello
cd istiohello
nano gateway-virtualservice.yaml
nano podhello.yaml
```

### 📌 Verifica del controller Istio Ingress
```bash
kubectl get pods -n istio-ingress --show-labels
>> Restituisce il nome del controller da inserire in gateway-virtualservice.yaml
```

### 📌 Applicazione delle configurazioni
```bash
kubectl apply -f gateway-virtualservice.yaml
kubectl apply -f podhello.yaml
```

### 📌 Controllo delle risorse
```bash
kubectl get pods
kubectl get virtualservice
kubectl get gateway
```

### 📌 Test dell'accesso al servizio
```bash
curl http://x.x.x.x/hello
```

## Kompose

### ⚙️ Pre-requisiti

- [Sito ufficiale](https://kompose.io/)
- [Repository GitHub](https://github.com/kubernetes/kompose?tab=readme-ov-file)
- [Guida all'installazione su GitHub](https://github.com/kubernetes/kompose/blob/main/docs/installation.md#github-release)
- [Getting Started](https://github.com/kubernetes/kompose/blob/main/docs/getting-started.md)
- [Documentazione per Compose.YAML](https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/)

### 🔹 Installation

Kompose è rilasciato tramite GitHub:

```bash
curl -L https://github.com/kubernetes/kompose/releases/download/v1.35.0/kompose-linux-amd64 -o kompose

chmod +x kompose
sudo mv ./kompose /usr/local/bin/kompose

kompose version
>> 1.35.0
```
### 🔹 Esempio
### 📌 Link Utili
- [🔗docker-compose.yaml](./Esempi/kompose/docker-compose.yaml)
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

### 📌 **1. Clonare il repository**  --OPZIONE 1 NON DISPONIBILE
Cloniamo il repository ufficiale di Stack4Things:  

```bash
git clone https://github.com/MDSLab/Stack4Things_Container_Deployment.git
```

Spostiamoci nella cartella del progetto:
```bash
cd Stack4Things_Container_Deployment/
git checkout e6c8ad509e63fc5d77cfbe65a29470dee97f76ff  #(basta il token, magari cambiare)
```

## 📌 **1. .zip**  -- OPZIONE 2 DISPONIBILE
### 📂 Contenuto della Cartella S4T

All'interno della cartella troverai:
- [**ComposeDeployment**](./S4T/ComposeDeployment)
    - **`deployments/`** → Contiene i file YAML per la definizione dei **Pod**, **Deployment** e **Service** di S4T.
    - **`storage/`** → Definizioni di **PersistentVolumeClaim (PVC)** per la gestione dei dati.
    - **`.env`** → File con le variabili d’ambiente necessarie per l'installazione.  
    - **`configmaps/`** → Configurazioni personalizzate per i servizi di S4T in Kubernetes.
- [ConfigurazioneIstio](./S4T/istioconf)
    - - **`istio/`** → Configurazioni di **Istio** per il bilanciamento del traffico e il gateway di accesso.

### 🚀 **Come Utilizzare i File**
1. **Estrarre la cartella ZIP** sul proprio sistema.
2. **Accedere alla cartella**
3. Applicare i file YAML al cluster Kubernetes:
```bash
Kubectl apply -f .
```
4. Verificare che i Pod siano attivi:
```bash
kubectl get pods
```
5. Verificare i servizi disponibili:
```bash
kubectl get svc
```

### ⚙️ **2. Configurare le variabili d’ambiente** -- SOLO CON OPZIONE 1
Carichiamo le variabili d'ambiente definite nel file .env:
```bash
export $(grep -v '^#' .env | xargs)   # Versione con `:`
                # Alternativa:
export $(grep -v '^#' .env | sed 's/: /=/' | tr -d '"' | xargs)   # Versione con `=`
```

### 🔄 3. Convertire il file docker-compose.yml in manifest Kubernetes -- SOLO CON OPZIONE 1
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

### 🛠 4. Creazione del Gateway e VirtualService per Istio -- VALIDO PER ENTRAMBE LE OPZIONI
- 📁 Definizione file yaml [qui](./S4T/istioconf)

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
>> http://x.x.x.x:8100/iotronic-ui
>> http://x.x.x.x:8100/horizon/auth/login/?next=/horizon/
```
