# K3s Configuration Guide
# K3s Cluster Setup Guide

## Guida al Setup di un Cluster K3s

Questa guida ti aiuterà a configurare un cluster K3s utilizzando una macchina come **server** (control plane) e una o più macchine come **worker nodes**. La guida segue un'installazione base con Calico disabilitato. Puoi trovare maggiori dettagli su questa guida [qui](https://www.fullstaq.com/knowledge-hub/blogs/setting-up-your-own-k3s-home-cluster).

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

## 4. Aggiungi i Worker Node

Ora puoi aggiungere i nodi di lavoro (worker nodes) al cluster.

### Aggiungi un Nodo Worker

1. **Accedi alla VM che fungerà da worker node**. Questo è il nodo che eseguirà i carichi di lavoro, ed è diverso dal nodo server.

2. **Esegui il seguente comando** sul nodo worker:

    ```bash
    curl -sfL https://get.k3s.io | K3S_URL=https://<Contol Plane IP>:6443 K3S_TOKEN=<YourToken> sh -
    ```

    Sostituisci `<Contol Plane IP>` con l'IP del server (control plane) e `<YourToken>` con il token che hai ottenuto in precedenza.

3. **Verifica la connessione al cluster**:

    Dopo aver eseguito il comando sul nodo worker, torna al server e esegui il comando:

    ```bash
    kubectl get nodes
    ```

    Esempio di output:

    ```
    NAME            STATUS  ROLES                   AGE VERSION
    ubuntuserver    Ready   control.plane,master    xx  xx
    ubuntuworker    Ready   <none>                  xx  xx
    ```

4. **Configurazione di `kubectl` sul Worker Node**:

    - Crea un file `~/.kube/config` sul nodo worker.
    - Copia il contenuto del file `k3s.yaml` dal server (control plane) in questo file.
    - Modifica il campo `server` per includere l'IP del server.

5. **Configura `kubectl`**:

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
[The Helm project](https://helm.sh/docs/intro/install/) provides two ways to fetch and install Helm. These are the official methods to get Helm releases. In addition to that, the Helm community provides methods to install Helm through different package managers. Installation through those methods can be found below the official methods.  

### From Script  
Helm now has an installer script that will automatically grab the latest version of Helm and install it locally.  

You can fetch that script, and then execute it locally. It's well documented so that you can read through it and understand what it is doing before you run it.  

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

you can also run if you want to live on the edge:
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```
## Install Cert-Manager  
 
- This step is only required to use certificates issued by Rancher's generated CA (`ingress.tls.source=rancher`) or to request Let's Encrypt issued certificates (`ingress.tls.source=letsEncrypt`).  

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
- [metallb-configuration](./MetalLB/metallb-config.yaml)
```bash
echo "Apri il file di configurazione: https://github.com/AsCd1/K3s-Configuration/blob/main/MetalLB/metallb-configuration.yaml"
nano metallb-configuration.yaml
```
Durante l'applicazione della configurazione si è verificato un errore risolto con un secondo apply:
- Creazione del file [L2Advertisement](./MetalLB/l2advertisement.yaml) separato.
```bash
nano l2advertisement.yaml
```
Apply della configurazione:
```bash
kubectl apply -f l2advertisement.yaml
kubectl apply -f metallb-config.yaml
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
- [🔗 Cartella esempi](../Esempi/Istio-Esempi)  

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

