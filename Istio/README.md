# MetalLB & Istio

In un cluster bare-metal, **MetalLB** e la **Gateway API** lavorano insieme per esporre e instradare il traffico esterno in modo flessibile. 

## ⚙️ Pre-requisiti  

- 🛠 **Una configurazione di Kubernetes:** [Vedi configurazione]()  
- 🌐 **Un LoadBalancer:** [Vedi configurazione MetalLB](../MetalLB/README.md) 

## 📖 Indice

- [🔹 MetalLB: Il Load Balancer per Bare-Metal](#-metallb-il-load-balancer-per-bare-metal)
- [🔹 Gateway API](#-gateway-api)
- [🔹 Come Lavorano Insieme](#-come-lavorano-insieme)
- [🔹 Scenario Complessivo](#-scenario-complessivo)
- [🔹 In Sintesi](#-in-sintesi)
- [🔹 Ingress vs Gateway API](#-ingress-vs-gateway-api)
- [🔹 Istio Install with Helm](#-istio-install-with-helm)
  - [📌 Aggiunta del repository Helm di Istio](#-aggiunta-del-repository-helm-di-istio)
  - [📌 Aggiornamento dei repository](#-aggiornamento-dei-repository)
  - [📌 Installazione della base di Istio](#-installazione-della-base-di-istio)
  - [📌 Verifica dello stato di istio-base](#-verifica-dello-stato-di-istio-base)
  - [📌 Installazione del servizio istiod](#-installazione-del-servizio-istiod)
  - [📌 Verifica dell'installazione](#-verifica-dellinstallazione)
  - [📌 Controllo dello stato dei pod di istiod](#-controllo-dello-stato-dei-pod-di-istiod)
  - [📌 Creazione dello spazio dei nomi per il gateway](#-creazione-dello-spazio-dei-nomi-per-il-gateway)
  - [📌 Installazione del gateway di Istio](#-installazione-del-gateway-di-istio)
  - [📌 Verifica dei servizi](#-verifica-dei-servizi)
- [🎯 Cosa abbiamo ottenuto](#-cosa-abbiamo-ottenuto)
  - [📌 Verifica dei pod di Istio Ingress](#-verifica-dei-pod-di-istio-ingress)
  - [📌 Verifica del Service di Istio Ingress](#-verifica-del-service-di-istio-ingress)
- [🚀 Hello World! in Istio](#-hello-world-in-istio)
  - [📌 Creazione dei file di configurazione](#-creazione-dei-file-di-configurazione)
  - [📌 Verifica del controller Istio Ingress](#-verifica-del-controller-istio-ingress)
  - [📌 Applicazione delle configurazioni](#-applicazione-delle-configurazioni)
  - [📌 Controllo delle risorse](#-controllo-delle-risorse)
  - [📌 Test dell'accesso al servizio](#-test-dellaccesso-al-servizio)

## 🔹 MetalLB: Il Load Balancer per Bare-Metal 

- **Funzione Principale**:  
  - MetalLB fornisce la funzionalità tipica di un **load balancer esterno**, assegnando **indirizzi IP pubblici** ai servizi di tipo `LoadBalancer` in cluster senza un provider cloud.  
- **Come Funziona**:  
  - Quando crei un **Service Kubernetes** di tipo `LoadBalancer`, MetalLB assegna un **IP esterno** (dal pool configurato) a quel servizio.  
  - Questo IP diventa il **punto d’ingresso** per il traffico esterno.  

## 🔹 Gateway API

- **Funzione Principale**:  
  - La **Gateway API** è una specifica più moderna e modulare per definire come il **traffico in ingresso** deve essere instradato all’interno del cluster.  
  - Suddivide la configurazione in più risorse (come **Gateway, HTTPRoute, TCPRoute**) rispetto all’oggetto `Ingress` tradizionale.  
- **Come Funziona**:  
  - **Gateway**: Definisce il punto d’ingresso, il listener (porta, protocollo, ecc.) e la configurazione di base.  
  - **HTTPRoute / TCPRoute**: Specificano come il traffico in ingresso deve essere indirizzato ai vari servizi interni.  

## 🔹 Come Lavorano Insieme  
1. **Esposizione Esterna con MetalLB**:  
   - In un cluster bare-metal, per esporre un **Gateway API** all’esterno, il controller del Gateway (es. **Contour, Kong, Istio**) viene eseguito come un servizio di tipo `LoadBalancer`.  
   - MetalLB assegna un **IP esterno** a questo servizio.  
2. **Instradamento del Traffico**:  
   - Il traffico arriva all'**IP esterno** gestito da MetalLB.  
   - Il **controller del Gateway** utilizza le risorse Gateway API (`Gateway`, `HTTPRoute`, ecc.) per **instradare il traffico** ai servizi interni.  
3. **Esempio Pratico**:  
   - Un **Gateway** ascolta sulla porta `80`.  
   - Grazie a un **HTTPRoute**, il traffico viene inoltrato a un **servizio Nginx** o un’applicazione `Hello World`.  

## 🔹 Scenario Complessivo  
| **Componente**  | **Funzione**  |
|----------------|-------------|
| **MetalLB**  | Fornisce l'IP esterno e gestisce il traffico in ingresso. |
| **Controller Gateway API**  | Gestisce il routing e l'instradamento del traffico interno con regole definite (`HTTPRoute`, ecc.). |

## 🔹 In Sintesi  
✅ **MetalLB**: Assegna un **IP esterno** e agisce come **load balancer**.  
✅ **Gateway API**: Fornisce un **modello di routing avanzato** e modulare.  
✅ **Collaborazione**: MetalLB gestisce l’**esposizione**, mentre la **Gateway API** gestisce l’**instradamento**.  

---

## 🔹 Ingress vs Gateway API  

| **Caratteristica**  | **Ingress**  | **Gateway API**  |
|--------------------|-------------|----------------|
| **Scopo**  | Esposizione base di servizi HTTP/HTTPS. | Gestione avanzata del traffico in ingresso. |
| **Controller**  | Richiede un **Ingress Controller** (es. Nginx Ingress). | Richiede un **controller Gateway API** (es. Contour, Kong). |
| **Flessibilità**  | Limitata, configurazione semplice. | Alta, separa le configurazioni in più risorse (`Gateway`, `HTTPRoute`, ecc.). |
| **Uso con MetalLB**  | Non direttamente compatibile. | Il controller viene esposto come `LoadBalancer` e usa un IP esterno assegnato da MetalLB. |


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










