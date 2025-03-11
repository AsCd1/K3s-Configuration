## MetalLB  

- [Concept](https://metallb.io/concepts/)  
- [Introduzione](https://metallb.io/)  
- [Sezione in Helm](https://artifacthub.io/packages/helm/metallb/metallb)  
- [Installazione](https://metallb.universe.tf/installation/)  
- [Configurazione](https://metallb.universe.tf/configuration/#layer-2-configuration)
- [l2advertisemnt.yaml](https://github.com/metallb/metallb/blob/main/config/crd/bases/metallb.io_l2advertisements.yaml)
- [MetalLB-Confing](MetalLB/metallb-config.yaml)

MetalLB è un Load Balancer per Kubernetes su cluster bare metal.  
In pratica, permette di assegnare un IP esterno ai servizi di tipo LoadBalancer, cosa che normalmente accade automaticamente sui cloud provider (come AWS, GCP, Azure) ma non in un cluster Kubernetes on-premise o su macchine fisiche.  

Kubernetes non offre un'implementazione di network load balancers (Services of type LoadBalancer) per cluster bare-metal. Le implementazioni che Kubernetes fornisce si basano su provider cloud (GCP, AWS, Azure). Se non si utilizza una di queste piattaforme, i LoadBalancers rimarranno nello stato “pending” indefinitamente.  

Gli operatori di cluster bare-metal possono usare "NodePort" ed "externalIPs" per il traffico in ingresso, ma entrambe le soluzioni presentano limitazioni in ambienti di produzione. MetalLB colma questa lacuna fornendo un'implementazione di network load balancer che si integra con l'infrastruttura di rete esistente.  

### Requirements  

MetalLB richiede:  

- Un cluster Kubernetes (versione 1.13.0 o successiva) senza network load-balancing preinstallato.  
- Una configurazione di rete compatibile con MetalLB.  
- Un pool di indirizzi IPv4 da assegnare ai servizi.  
- **BGP mode**: necessità di uno o più router compatibili con BGP.  
- **L2 mode**: il traffico sulla porta **7946 (TCP & UDP)** deve essere consentito tra i nodi.  

### Address Allocation  

Nei cloud provider, il bilanciatore assegna automaticamente un IP pubblico ai servizi di tipo LoadBalancer. In un cluster bare-metal, MetalLB gestisce questo processo.  

MetalLB non può generare IP da zero, quindi è necessario fornirgli pool di indirizzi. Assegnerà e rilascerà gli IP in base alle necessità, ma solo all'interno dei pool configurati.  

### External Announcement  

Dopo aver assegnato un IP esterno a un servizio, MetalLB deve renderlo accessibile alla rete esterna. Utilizza protocolli di rete standard:  

1. **Layer 2**: Un nodo del cluster annuncia l'IP sulla rete locale tramite **ARP (IPv4)** o **NDP (IPv6)**.  
2. **BGP**: Tutti i nodi stabiliscono sessioni BGP con router esterni e comunicano loro come instradare il traffico.  

- Maggiori dettagli su [BGP mode](https://metallb.io/concepts/bgp/)  
- Maggiori dettagli su [Layer 2 mode](https://metallb.io/concepts/layer2/) 
