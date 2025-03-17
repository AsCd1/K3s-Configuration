# 🛠 Creazione del Gateway e VirtualService per Istio
- 📁 Definizione file yaml [qui](./istioconf)

## ⚙️ Pre-requisiti
- Una versione di kubernetes
- Istio
- La versione di [S4T](./ComposeDeployment) per kubernetes

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
