## MetalLB & Gateway API  

In un cluster bare-metal, **MetalLB** e la **Gateway API** lavorano insieme per esporre e instradare il traffico esterno in modo flessibile.  

### 🔹 MetalLB: Il Load Balancer per Bare-Metal  
- **Funzione Principale**:  
  - MetalLB fornisce la funzionalità tipica di un **load balancer esterno**, assegnando **indirizzi IP pubblici** ai servizi di tipo `LoadBalancer` in cluster senza un provider cloud.  
- **Come Funziona**:  
  - Quando crei un **Service Kubernetes** di tipo `LoadBalancer`, MetalLB assegna un **IP esterno** (dal pool configurato) a quel servizio.  
  - Questo IP diventa il **punto d’ingresso** per il traffico esterno.  

### 🔹 Gateway API  
- **Funzione Principale**:  
  - La **Gateway API** è una specifica più moderna e modulare per definire come il **traffico in ingresso** deve essere instradato all’interno del cluster.  
  - Suddivide la configurazione in più risorse (come **Gateway, HTTPRoute, TCPRoute**) rispetto all’oggetto `Ingress` tradizionale.  
- **Come Funziona**:  
  - **Gateway**: Definisce il punto d’ingresso, il listener (porta, protocollo, ecc.) e la configurazione di base.  
  - **HTTPRoute / TCPRoute**: Specificano come il traffico in ingresso deve essere indirizzato ai vari servizi interni.  

### 🔹 Come Lavorano Insieme  
1. **Esposizione Esterna con MetalLB**:  
   - In un cluster bare-metal, per esporre un **Gateway API** all’esterno, il controller del Gateway (es. **Contour, Kong, Istio**) viene eseguito come un servizio di tipo `LoadBalancer`.  
   - MetalLB assegna un **IP esterno** a questo servizio.  
2. **Instradamento del Traffico**:  
   - Il traffico arriva all'**IP esterno** gestito da MetalLB.  
   - Il **controller del Gateway** utilizza le risorse Gateway API (`Gateway`, `HTTPRoute`, ecc.) per **instradare il traffico** ai servizi interni.  
3. **Esempio Pratico**:  
   - Un **Gateway** ascolta sulla porta `80`.  
   - Grazie a un **HTTPRoute**, il traffico viene inoltrato a un **servizio Nginx** o un’applicazione `Hello World`.  

### 🔹 Scenario Complessivo  
| **Componente**  | **Funzione**  |
|----------------|-------------|
| **MetalLB**  | Fornisce l'IP esterno e gestisce il traffico in ingresso. |
| **Controller Gateway API**  | Gestisce il routing e l'instradamento del traffico interno con regole definite (`HTTPRoute`, ecc.). |

### 📌 In Sintesi  
✅ **MetalLB**: Assegna un **IP esterno** e agisce come **load balancer**.  
✅ **Gateway API**: Fornisce un **modello di routing avanzato** e modulare.  
✅ **Collaborazione**: MetalLB gestisce l’**esposizione**, mentre la **Gateway API** gestisce l’**instradamento**.  

---

## Ingress vs Gateway API  

| **Caratteristica**  | **Ingress**  | **Gateway API**  |
|--------------------|-------------|----------------|
| **Scopo**  | Esposizione base di servizi HTTP/HTTPS. | Gestione avanzata del traffico in ingresso. |
| **Controller**  | Richiede un **Ingress Controller** (es. Nginx Ingress). | Richiede un **controller Gateway API** (es. Contour, Kong). |
| **Flessibilità**  | Limitata, configurazione semplice. | Alta, separa le configurazioni in più risorse (`Gateway`, `HTTPRoute`, ecc.). |
| **Uso con MetalLB**  | Non direttamente compatibile. | Il controller viene esposto come `LoadBalancer` e usa un IP esterno assegnato da MetalLB. |

