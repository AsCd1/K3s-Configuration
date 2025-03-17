# 📌 **1. .zip**
## 📂 Contenuto della Cartella ComposeDeployment

All'interno della cartella troverai:
- [**ComposeDeployment**](../S4T/ComposeDeployment)
    - **`deployments/`** → Contiene i file YAML per la definizione dei **Pod**, **Deployment** e **Service** di S4T.
    - **`storage/`** → Definizioni di **PersistentVolumeClaim (PVC)** per la gestione dei dati.
    - **`.env`** → File con le variabili d’ambiente necessarie per l'installazione.  
    - **`configmaps/`** → Configurazioni personalizzate per i servizi di S4T in Kubernetes.

## 🚀 **Come Utilizzare i File**
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


