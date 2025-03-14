# MetalLB  
## 🔗 Risorse Utili
- [Concept](https://metallb.io/concepts/)  
- [Introduzione](https://metallb.io/)  
- [Sezione in Helm](https://artifacthub.io/packages/helm/metallb/metallb)  
- [Installazione](https://metallb.universe.tf/installation/)  
- [Configurazione](https://metallb.universe.tf/configuration/#layer-2-configuration)
- [l2advertisemnt.yaml](https://github.com/metallb/metallb/blob/main/config/crd/bases/metallb.io_l2advertisements.yaml)
- [MetalLB-Confing](MetalLB/metallb-config.yaml)

## 🔎 Cos'è MetalLB?
MetalLB è un Load Balancer per Kubernetes su cluster bare metal.  
In pratica, permette di assegnare un IP esterno ai servizi di tipo LoadBalancer, cosa che normalmente accade automaticamente sui cloud provider (come AWS, GCP, Azure) ma non in un cluster Kubernetes on-premise o su macchine fisiche.  

Kubernetes non offre un'implementazione di network load balancers (Services of type LoadBalancer) per cluster bare-metal. Le implementazioni che Kubernetes fornisce si basano su provider cloud (GCP, AWS, Azure). Se non si utilizza una di queste piattaforme, i LoadBalancers rimarranno nello stato “pending” indefinitamente.  

Gli operatori di cluster bare-metal possono usare "NodePort" ed "externalIPs" per il traffico in ingresso, ma entrambe le soluzioni presentano limitazioni in ambienti di produzione. MetalLB colma questa lacuna fornendo un'implementazione di network load balancer che si integra con l'infrastruttura di rete esistente.  

## 📌 Requisiti per l'installazione  

- Un cluster Kubernetes (versione 1.13.0 o successiva) senza network load-balancing preinstallato.  
- Una configurazione di rete compatibile con MetalLB.  
- Un pool di indirizzi IPv4 da assegnare ai servizi.  
- **BGP mode**: necessità di uno o più router compatibili con BGP.  
- **L2 mode**: il traffico sulla porta **7946 (TCP & UDP)** deve essere consentito tra i nodi.
- Un'installazione di [Helm](../Helm)

## 📡 Allocazione degli indirizzi IP  

Nei cloud provider, il bilanciatore assegna automaticamente un IP pubblico ai servizi di tipo LoadBalancer. Su un cluster bare metal, MetalLB gestisce questa operazione assegnando IP dagli indirizzi configurati manualmente.  

⚠️ **Importante:** MetalLB non può generare IP da solo. È necessario fornirgli pool di indirizzi disponibili. Assegnerà e rilascerà gli IP in base alle necessità, ma solo all'interno dei pool configurati.  

## 🌎 Annuncio dell'IP esterno 

Dopo aver assegnato un IP pubblico a un servizio, MetalLB deve renderlo accessibile alla rete esterna. 
Usa due modalità principali:

1. **Layer 2**: Un nodo del cluster annuncia l'IP sulla rete locale tramite **ARP (IPv4)** o **NDP (IPv6)**.  
2. **BGP**: Tutti i nodi stabiliscono sessioni BGP con router esterni e comunicano loro come instradare il traffico.  

🔍 Maggiori dettagli:
- [BGP mode](https://metallb.io/concepts/bgp/)
- [Layer 2 mode](https://metallb.io/concepts/layer2/)

## ⚙️ Installazione con Helm
🔹 Aggiungi il repository Helm di MetalLB
```bash
helm repo add metallb https://metallb.github.io/metallb
```
🔹Installa MetalLB
```bash
helm install metallb metallb/metallb
```

## 🔧 Configurazione Layer2
📁 Creazione del file di configurazione per Layer 2:
- 📝 [metallb-configuration](./MetalLB/metallb-config.yaml)
```bash
echo "Apri il file di configurazione: https://github.com/AsCd1/K3s-Configuration/blob/main/MetalLB/metallb-configuration.yaml"
nano metallb-configuration.yaml
```
🚨 Durante l'applicazione della configurazione si è verificato un errore risolto con un secondo apply:
- 📝 Creazione del file [L2Advertisement](./MetalLB/l2advertisement.yaml) separato.
```bash
nano l2advertisement.yaml
```
📌 Apply della configurazione:
```bash
kubectl apply -f l2advertisement.yaml
kubectl apply -f metallb-config.yaml
```
📌 Verifica della configurazione:
```bash
kubectl get ipaddresspools -n metallb-system
>> Output: Lista dei range IP

kubectl get l2advertisements -n metallb-system
>> Output: Nome e range IP
```
