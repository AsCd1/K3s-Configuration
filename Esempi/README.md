# 📂 Esempi
## Pre-requisiti
- Un LoadBalncer: Vedi [MetalLB](../MetalLB)
- Un CNI: vedi [Calico](../Calico)

## 🟢 1. Prova per verificare il funzionamento
- [Deployment nginx-hello-deployment](Esempi/ngnix-prova/nginx-hello-deployment.yaml)
- [Git originale del deployment](https://gist.githubusercontent.com/sdenel/1bd2c8b5975393ababbcff9b57784e82/raw/f1b885349ba17cb2a81ca3899acc86c6ad150eb1/nginx-hello-world-deployment.yaml)

📁 Creazione della directory di prova:
```bash
mkdir nginx-prova
cd nginx-prova
```
📝 Creazione del file di configurazione:
```bash
nano nginx-hello-deployment.yaml
```
🚀 Applicazione della configurazione:
```bash
kubectl apply -f .
    oppure
kubectl apply -f nginx-hello-deployment.yaml
```
🔍 Controllo dei servizi:
```bash
kubectl get svc -A
```
📌 Output atteso:
```
>>> default nginx   LoadBalancer    InternalIP  ExternalIP <- deve essere quello del yaml
```
🌐 Testare l'accesso al servizio:
```bash
curl 192.x.x.x # Sostituire col proprio externalIP
```
📌 Output atteso:
```
>>> Hello World!
```
⚠️ Se ci sono problemi, provare:
```bash
wget -qO- 192.x.x.x
```

📌  Output atteso:
```
>> Hello World!
```

## 🔵 2. Hello World con 3 Repliche
- [Deployment nginx-hello-deployment-3Rep](Esempi/ngnix-prova/nginx-hello-deployment-3Rep.yaml)

📌 Applicare il Deployment con 3 repliche
```bash
kubectl apply -f nginx-hello-world-deployment-3Rep.yaml
kubectl get pods -l app=nginx
>> OUTPUT: 3 pod
```
🌐 Verifica accesso al servizio
```bash
curl 192.x.x.x
>> Hello World!
```

## 🟠 3. Ottenere il nome del Pod
- [Deployment nginx-monitoring](Esempi/ngnix-prova/nginx-monitoring.yaml)

📝 Applicare la configurazione
```bash
nano ngnix-monitoring.yaml
kubectl apply -f ngnix-monitoring.yaml
```
🌐 Verifica accesso al servizio
```bash
curl 192.x.x.x
>> Hello world from pod: nginx-<Podid>
```
🔍 Visualizzare i dettagli dei Pod
```bash
kubectl get pods -o wide
```



