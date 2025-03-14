# 🐆 Calico

Calico è un plugin di rete per Kubernetes che fornisce networking e sicurezza per i pod. Può essere installato in due modi principali:

- Installazione sul control plane.
- Installazione manuale tramite manifest anche sul worker.
- Installazione tramite operator, che applica automaticamente su entrambi se eseguito sul control plane.

## 🔶 Operator vs Manifest

Calico può essere installato tramite due approcci principali:

1. **Operator**: Un metodo automatizzato e gestito per l'installazione e l'aggiornamento di Calico.
2. **Manifest**: Un metodo manuale che applica direttamente i file di configurazione YAML nel cluster.

## 🔶 Installazione con Operator

1. 🛠 Installa l'operatore Calico e le definizioni delle risorse personalizzate.
2. 📌 Repository di Calico: [Link al repository Calico](https://github.com/projectcalico/calico/tree/master)
3. 📖 Guida all'installazione: [Guida ufficiale all'installazione di Calico su K3s](https://docs.tigera.io/calico/latest/getting-started/kubernetes/k3s/multi-node-install)
4. 🚀 Installazione tramite Helm: [Guida per l'installazione tramite Helm](https://docs.tigera.io/calico/latest/getting-started/kubernetes/helm) -- Necessario [Helm]Inserirelink

### 🔧 Comandi per installare l'operatore Calico:

```bash
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.2/manifests/tigera-operator.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.2/manifests/custom-resources.yaml
kubectl get nodes -o wide  # Da eseguire anche sul worker --opzionale
kubectl get pods -n calico-system -o wide
ip route show
kubectl get pods -A | grep -E "calico|flannel" #flannel è presente di default se non si segue l'installazione pulita
```
