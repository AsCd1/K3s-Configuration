# K3s-Configuration
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
    $ curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server --disable traefik --disable servicelb" sh -
    ```

    Questo comando installerà K3s sul server host e disabiliterà Traefik e il bilanciamento del servizio (service load balancer).

## 2. Recupera il Token del Nodo

Dopo aver installato K3s sul server, recupera il **token del nodo** che sarà utilizzato per aggiungere i worker nodes al cluster.

1. **Esegui il seguente comando** sul server per ottenere il token:

    ```bash
    $ cat /var/lib/rancher/k3s/server/node-token
    ```

    oppure:

    ```bash
    $ sudo cat /var/lib/rancher/k3s/server/node-token
    ```

2. Il **token** che otterrai servirà per il comando successivo = `YourToken`.

## 3. Recupera il Certificato del Cluster

Per poter comunicare con il cluster, è necessario recuperare il certificato di configurazione di K3s.

1. **Esegui il seguente comando** per ottenere il file di configurazione:

    ```bash
    $ cat /etc/rancher/k3s/k3s.yaml
    ```

    oppure:

    ```bash
    $ sudo cat /etc/rancher/k3s/k3s.yaml
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
    $ curl -sfL https://get.k3s.io | K3S_URL=https://<Contol Plane IP>:6443 K3S_TOKEN=<YourToken> sh -
    ```

    Sostituisci `<Contol Plane IP>` con l'IP del server (control plane) e `<YourToken>` con il token che hai ottenuto in precedenza.

3. **Verifica la connessione al cluster**:

    Dopo aver eseguito il comando sul nodo worker, torna al server e esegui il comando:

    ```bash
    $ kubectl get nodes
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
    $ export KUBECONFIG=~/.kube/config
    $ kubectl get nodes
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
    $ kubectl create -f https://raw.githubusercontent.com/
    projectcalico/calico/v3.29.2/manifests/
    tigera-operator.yaml

    $ kubectl create -f https://raw.githubusercontent.com/projectcalico/
    calico/v3.29.2/manifests/custom-resources.yaml

    $ kubectl get nodes -o wide (da eseguire anche sul worker)
    $ kubectl get pods -n calico-system -o wide
    $ ip route show
    $ kubectl get pods -A | grep -E "calico|flannel"
    '''



