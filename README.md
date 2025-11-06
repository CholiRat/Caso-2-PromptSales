# Caso-2-PromptSales
### Instituto Tecnológico de Costa Rica
### Escuela de Ingeniería en Computación
### Students
- Alexander Brenes Garita - 2018191805
- Andrés Baldi Mora - 2024088934
- Lindsay Nahome Marín Sánchez - 2024163904
### Course
Software Design
### Delivery dates
🗓️ First delivery: October 26, 2025

🗓️ Second delivery: November 8, 2025

🗓️ Final delivery: November 23, 2025


### Project Structure:

```bash
Caso-2-PromptSales/
├── diagrams/
├── img/
├── kubernetConfig/
└── README.md
```

## 1. Introduction
This repository details the design of the application Prompt Sales

## 2. Scope
This project will be executed through three iterations.

## 3. Metrics for non-functional requirements

### 3.1 Performance

The software stack that will be used to build the project is as follows:

#### Programming Language
- Python

#### Database Management System
- SQL Server

#### Interface for System Integration
- REST APIs

#### API Framework
- FastAPI (compatible with Python)

### In-Memory Data Store
- Redis

The performance objectives for the project are:

- The average response time of the web portal should be **less than 2.5 seconds** per operation.  
- Queries must deliver results in **under 400 milliseconds** when using Redis.  
- Automated generation processes must complete in **under 7 seconds** for simple requests and **under 20 seconds** for complex executions.

By searching for benchmarks that use the same software stack and performance goals, we found the following:

#### FastAPI + Python
[FastAPI + Python Benchmark](https://sharkbench.dev/web/python-fastapi)

**Hardware used in the benchmark:**
- **OS:** Linux/Docker  
- **CPU:** Ryzen 7 7800X3D  

**Results:**

![FastApi](img/FastApiBenchmark.jpg)

According to the benchmark, the **RPS (requests per second)** is **1185**, with a **latency of 21.0 ms** and **memory usage of 41.2 MB**.

#### SQL Server + Python
[SQL Server + Python Benchmark](https://devblogs.microsoft.com/python/mssql-python-vs-pyodbc-benchmarking-sql-server-performance/?utm_source=chatgpt.com)

This benchmark evaluates the performance of Python drivers connecting to SQL Server databases.

**Hardware used in the benchmark:**
- **OS:** Windows 11 Pro  
- **CPU:** Intel Core i7 (12th Gen)  
- **RAM:** 32 GB  
- **Database:** Azure SQL Database - 1 vCore  
- **Storage:** 32 GB  

**Performance Summary:**

![mssql](img/mssqlPython.jpg)

**Execution Times:**

![operationSQL](img/operationSQL.png)

Now, extrapolating this data to our project’s software and performance targets:

#### RQS (Requests per Second)

- Total RPS = **1,667**  
- Cache hits = **0.5 × 1,667 = 833 RPS**  
- DB writes = **0.30 × 1,667 = 500 RPS**  
- DB reads = **0.20 × 1,667 = 334 RPS**  
- Total database operations ≈ **834 RPS (500 + 334)**  

#### Pods for FastAPI

For database-bound operations, we use the following formula:

$$
pods_{db} = ⌈\frac{834\ (RPS)}{300\ (processes)}⌉ = 3\ pods
$$

#### Database Sizing (vCores)

- Required DB TPS ≈ **834 TPS (transactions per second)**  
- Assuming **100 TPS per vCore**, the formula is:  

$$
vCores = ⌈834(RPS)/100(TPS)⌉ = 9vCores
$$

**Note:** Azure SQL **Business Critical** will be used to minimize latency.

#### Redis

To maintain latency below **400 ms**, and given that cache hits ≈ **833 RPS × 2 ≈ 1700 ops (operations per second)**:

**Note:** Azure **Cache for Redis** will be used, with capacity ≥ **5k ops/s** and latency **< 10 ms** to guarantee ≤ **400 ms** response times.

#### AI Generation

For AI workloads, we estimate **AI RPS ≈ 83**.  
Average execution time: **(simple + complex) ≈ 5.4 s**, thus:  
**Required concurrency ≈ 83 × 5.4 ≈ 448 concurrent tasks.**

**Note:** Azure **OpenAI Service** will be used to ensure processing times of **<7s / <20s**.

#### Storage

The formula for storage estimation is:

$$
GB_{per\_day} = \frac{PPM \times bytes/prompt}{1024^2} \times 60
$$

Where:
- **PPM** = prompts per minute  
- **bytes/prompt** = average prompt size  
- **1024²** = bytes to megabytes conversion  
- **60** = minutes to hours conversion  

**Note:** Azure **Blob Storage** will be used to store this information.

### 3.2 Scalability
To transform PromptSales into a highly scalable system, **Azure Kubernetes Service (AKS)** will be used. 

To assure horizontal scaling capabilities in all the databases, **Azure SQL Database** will be used.

In the case of mongoDB, **Azure Cosmos DB** will be used to create regional replicas and scale the PromptContent database. 

The Kubernetes network, managed by AKS, is responsible for dynamically scaling the stateless application pods.

Based on the benchmark results in section 3.1, the databases require a **minimum of 3 pods** to handle the expected load. To meet this requirement, the deployments use a Horizontal Pod Autoscaler (HPA) that dynamically adjusts the number of replicas up to 30, providing up to 10x capacity as demand increases.

Here is the HPA file that demonstrates scalability:

```yaml
# NAMESPACE: promptads-app
# This HorizontalPodAutoscaler (HPA) file fulfills the goal of scalability in the system.

apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: promptads-hpa
  namespace: promptads-app
spec:
  scaleTargetRef:				# This file targets the deployment of promptads.
    apiVersion: apps/v1
    kind: Deployment
    name: promptads-deployment
  minReplicas: 3
  maxReplicas: 30				# x10 the scale
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 80		# The autoscale will take place when more than 80% of a pod's cpu is being used
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 85		# The autoscale will take place when more than 85% of a pod's memory is being used

```
It declares a minimum of 3 replicas and maximum of 30. 

The scale takes place when more than 80% of CPU is being consumed in one pod or 85% of memory is being used instead. These are high values that assure better balancing through the pods.

All scaling rules and pod configurations are defined and managed through declarative YAML files.

[Check kubernetes configuration folder]( https://github.com/CholiRat/Caso-2-PromptSales/tree/main/kubernetConfig)

For the SQL databases, scalability is managed directly by Azure SQL Database. This plataform offering provides robust horizontal scaling through two primary mechanisms:

-	**Elastic Pools**: To efficiently manage performance and cost for multiple databases with variable usage patterns.
-	**Sharding with Elastic Database Tools**: To distribute data across multiple databases to handle high-volume transactions.

For more information check the oficial documentation: [Elastic scale - Azure SQL Database | Microsoft Learn](https://learn.microsoft.com/es-es/azure/azure-sql/database/elastic-scale-introduction?view=azuresql)

To meet the requirement of handling 100,000 transactions, the data will be partitioned across 3 sharded set of databases. This is according to the data retrieved from the perfomance benchmarks
-	**Number of Shards**: The system will be configured with 3 shards.
-	**Data Distribution**: Information will be partitioned into 3 distinct parts using a hash function over the campaignIDs. In this way, distribution is balanced according to the amount of campaigns in the system.

### 3.3 Reliability

The project must guarantee continuous service availability and automatic fault detection.  
The **error rate** must not exceed **0.1% of total daily transactions**.

**Example:**  
If 100,000 transactions are processed per day, the maximum allowed failures are **≤ 100**.

**Azure Monitor Alerts** will be used to detect and notify critical failures.

The configured alert thresholds are as follows:

- **Deadlocks > 3 / 10 min →** SQL Server alert  
- **Redis Hit Rate < 85% →** preventive alert  
- **Pod restarts > 3 / hour →** instability alert  

If issues persist for more than **10 minutes**, a ticket will automatically be created in **Azure DevOps**.  

All detailed diagnostic information will be stored in **Azure Log Analytics Workspace**.

### 3.4 Availability

To ensure system resilience, high availability is implemented across both the databases and application using a combination of Azure SQL database, Azure Cosmos DB and AKS.

For the data layer, high availability is achieved using the **Geo-Replication** feature of Azure SQL Database (PaaS). This service is configured for every database shard (PromptSales, PromptAds, PromptCRM) and provides two critical functions:
- **Real-time Replication:** A constant, synchronized replica of each primary database is maintained in a secondary geographic region (West Europe) which is constantly being synced with the primary region. This ensures data is duplicated in near real-time, protecting against High availability disaster recovery.
- **Automatic Failover:** In the event of an outage in the primary region (US), Azure automatically redirects all connections to the secondary database without manual intervention. This failover process takes less than 25 seconds, guaranteeing high availability. Once the primary region is restored, connections are moved back.

In the case of the documental database PromptContent, Azure Cosmos DB includes:
- **Real-time Global Replication:** A synchronized replica of the database is automatically maintained in all configured Azure regions.
- **Automatic Failover:** In the event of an outage in one region, Azure Cosmos DB automatically redirects all connections to the next available region without manual intervention.

The connection endpoints for these configurations are managed within the cluster via a ConfigMap:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: azure-config
  namespace: default
data:
  # Primary regions
  AZURE_PRIMARY_REGION: "US"
  PROMPTSALES_DB_PRIMARY: "promptsales-db-us.database.windows.net"
  PROMPTADS_DB_PRIMARY: "promptads-db-us.database.windows.net"
  PROMPTCONTENT_DB_PRIMARY: "promptcontent-db-us.database.windows.net"
  PROMPTCRM_DB_PRIMARY: "promptcrm-db-us.database.windows.net"
  
  # Secondary regions
  AZURE_SECONDARY_REGION: "West Europe" 
  PROMPTSALES_DB_SECONDARY: "promptsales-db-westeurope.database.windows.net"
  PROMPTADS_DB_SECONDARY: "promptads-db-westeurope.database.windows.net"
  PROMPTCONTENT_DB_SECONDARY: "promptcontent-db-westeurope.database.windows.net"
  PROMPTCRM_DB_SECONDARY: "promptcrm-db-westeurope.database.windows.net"
```
Check the [azure configuration for sql databases](kubernetConfig/azure-config.yaml)

For more information about Geo-replication, visit: [Active-Geo-replication](https://learn.microsoft.com/en-us/azure/azure-sql/database/active-geo-replication-configure-portal?view=azuresql&tabs=portal)

For information about replication in Azure Cosmos DB visit: [Distribute your data globally with Azure Cosmos DB](https://learn.microsoft.com/en-us/azure/cosmos-db/distribute-data-globally)

---

On another note, AKS will assure replication and failover using K8s a LoadBalancer and HPA.

Kubernetes automatically maintains the desired number of application pod replicas as defined in the Horizontal Pod Autoscaler (HPA). If a pod fails, AKS immediately restarts it or schedules a new one.

This is a section of the HPA file for the promptads backend
```yaml
  scaleTargetRef:				# This file targets the deployment of promptads.
    apiVersion: apps/v1
    kind: Deployment
    name: promptads-deployment
  minReplicas: 3
  maxReplicas: 30	
```
Check the [HPA.yaml](kubernetConfig/prompt-ads/deployment.yaml) file for promptads.

With the LoadBalancer type service, the application efficiently distributes incoming network requests across all available, healthy application pods.
```yaml
# NAMESPACE: promptsales-app
# The service file establishes the point of connection for promptsales in our kubernet

apiVersion: v1
kind: Service
metadata:
  name: promptsales-service
  namespace: promptsales-app
spec:
  type: LoadBalancer		# Balances the requests between different replicas
  selector:
    app: promptsales-app
  ports:
    - protocol: TCP
      port: 80                    
      targetPort: 8080      
```

Check the [service.yaml](kubernetConfig/prompt-sales/service.yaml) file for promptsales.

#### Downtimes
Azure guarantees 99.95% availability for their SQL Database services, which forms the foundation of our high-availability architecture.
Assuming a 31 day month, this means:
-	Total minutes in month: 44,640 min
-	Available minutes per Azure SLA: 44,617.68 min
-	Azure SLA downtime allowance: 22.32 min

According to Azure documentation, databases are down for up to 25 seconds while the regions are being switched. For this calculation, we assume the worst scenario, 25 seconds of downtime.
- Assumed fail frequency: 2 times per day through all Prompt Sales services
- Daily downtime: 50 seconds (2 × 25 seconds)
- Monthly downtime (31 days): 1,550 seconds (25.833 minutes)
- Azure infrastructure: 22.32 min
- Planned failovers: 25.833 min
- Total downtime: 48.153 min
- Available total minutes: 44,591.847 min

Monthly availability: 99.892%

The system achieves 99.89% availability, comfortably meeting the standards for this requirement.

### 3.5 Security

Confidentiality, integrity, and availability of user and transaction data in the PromptSales system must be guaranteed.  
The following technologies will be used to ensure security:

#### Authentication and Authorization

**OAuth 2.0 + OpenID Connect** will be used for the API Gateway component, with access control managed through signed **JWT tokens**.

#### Data Protection

To protect data in our SQL Server database, **Transparent Data Encryption (TDE) with AES-256** will be used, with master keys distributed and secured using **Azure Key Vault**.

#### Controls

- To protect our API, **Azure API Management** will be used to limit requests per IP and validate tokens.  
- To protect against attacks, **Azure Front Door WAF** will be used with **OWASP Core Rule Set v3.2** rules.  
- For traceability, **Azure Monitor + Sentinel SIEM** will be used for log correlation, anomaly detection, and threat analysis.

### 3.6 Maintainability
To ensure the maintainability of the system in both the short and long term, standardized processes will be implemented for both development and post-production support.

#### 3.6.1 During Development

Source code and task management will adhere to the following methodologies:

- Task Management: All work will be managed through a ticketing system in Trello. Each team member is responsible for keeping their tickets updated on a weekly basis.
- Version Control: A Gitflow-based workflow will be used, with the following branches:

    - Main Branch / Master
      - Contains stable production code of all project, including versions (release tag, eg: v1.2.3), production configuration (environment variables or config files) and documentation for releases that should be update or include somewhere else in the branch, like release notes or a CHANGELOG.md for example.
    
    - HotFixes Branch
      - Branches for critical fixes in production, based on main. This branch is used for fixing issues on the master branch. Is employed for quickly fix critical issues and for urgent bugs that can not wait until the next release cycle. For example, Security vulnerabilities.

    - Release Branch
      - Is used to stabilize the codebase before deploying to production. Allows to do things like this ones:
        - Freeze development for the current sprint/release cycle.
        - Perform final QA, bug fixing, and versioning.
        - Continue development of new features in parallel (in develop).
    
    - Develop Branch
      - Is the central integration branch for all new code that’s being prepared for the next release. Is where all the developers work on and all the features are merged once they are done. Is where the lastest stable development version of the software lives in.
    
    - Feature Branch
      - Is used to develop a single feature or improvement in isolation. Isolated from develop until the feature is complete. Focused on a specific goal or story. Temporary: deleted after being merged into develop.

      GitFlow Image

      ![GitFlow](img/Gitflow.jpg)

- Other things that are going to be employ for Maintainability during development are the following:


- Pull Requests (PRs): All code must be integrated into develop or main exclusively through Pull Requests. Each PR must be reviewed and approved by at least one team member before merging.

- Release Process: Production releases will be carried out on a scheduled basis every two weeks (sprint cycle), merging the develop branch into main after successful validation in the staging environment.

- Hotfix Process: Critical fixes (hotfixes) will be developed in their own branch (hotfix/) based on main. Once approved, they will be merged into both main (for immediate deployment) and develop (to prevent regressions).

#### 3.6.2 Post-Development Support

A tiered support model (L1, L2, L3) is established to manage incidents and inquiries:

- Level 1 (L1 – Basic Support):

  - Channel: User manuals, tutorial videos, and an RAG (Retrieval-Augmented Generation) system via WhatsApp for common questions.

  - Objective: Self-service and resolution of frequent doubts.

- Level 2 (L2 – Technical Support):

  - Channel: Email (support@promptsales.com).

  - Response Time (Service Level Agreement): Acknowledgment between 8 and 12 business hours.

  - Resolution Time (Service Level Agreement): Incident resolution between 4 and 7 business days.

- Level 3 (L3 – Specialized Support):

  - Channel: Internal issue tracking system (e.g., Trello or GitHub Issues), escalated from L2.

  - Objective: Resolution of complex bugs, infrastructure failures, or integration problems requiring development team intervention.

### 3.7 Interoperability
To ensure that the PromptSales modules (Ads, Content, and CRM) operate in an integrated manner and can connect with external services, we have chosen REST APIs as our primary communication method.

This approach will be used for all communication between services built with Flask and FastAPI, as well as for managing automation processes.
When designing our APIs, we will follow RESTful principles, including the use of Redis caching to optimize interactions and improve platform performance, in line with performance requirements.

Finally, for specialized communication among various AI services (which have different requirements), the use of MCP (Model Context Protocol) servers will be reserved.
### 3.8 Compliance

The system will be designed in accordance with international standards for security and data protection:

#### Payment Management

All credit card, transfer, or monetary transaction data will not be stored in our systems. These operations will be fully delegated to third-party payment gateways that comply with PCI DSS certification.

#### Application Security

- Web applications (Vercel) will follow the OWASP Top 10 2.0 recommendations.

- Backend services (REST APIs in Flask/FastAPI) will be developed mitigating OWASP Top 10 3.x vulnerabilities, with particular emphasis on access control (OAuth 2.0) and data injection.

#### Data Protection (GDPR/CCPA)

- Encryption of sensitive data at rest (AES-256) and in transit (TLS 1.3).
- Implementation of the least privilege principle (minimum necessary access).
- Mechanisms for user consent management and the right to be forgotten.

### 3.9 Extensibility
Design choices have been made to guarantee the extensibility of the system across its lifetime. In this section, design patterns and other tools are discussed to demonstrate their ability to expand the application.
#### 3.9.1 REST
The REST architecture employed across the entire system enables integration with new sub-businesses and third-party services. 

When a new business is incorporated into PromptSales, the frontend layer remains unaffected, allowing to add new services. Also, the stateless nature of REST architecture further enhances independence between the different architectural layers, ensuring clean separation and modularity.
#### 3.9.2 Kubernetes
Kubernetes provides foundation for system extensibility by allowing integration of new services and capabilities without disrupting existing operations. Its architecture is specifically designed to support continuous growth and modular expansion. AKS extends these capabilities with cloud-specific features that further simplify extensibility.
#### 3.9.3 MCP 
MCP servers centralize the connection point for various AI models. This architecture allows new sub-businesses to immediately leverage existing AI tools available to develop. Furthermore, the system is extensible at the MCP layer; new tools, context sources, or AI models can be added to the MCP server, thereby expanding its capabilities without requiring modifications across every other system component.
#### 3.9.4 Domain Driven Design
The Domain-Driven Design architecture for the backend is crucial for extensibility. It ensures that new functionalities are added as entirely new domains, rather than by modifying existing ones. This prevents regressions and maintains system stability. Consequently, development teams can work independently on different domains, accelerating feature development and enabling parallel workstreams without creating interdependencies or conflicts.

## 4. Domain Driven Design

#### 4.1 Prompt Content Domains
Prompt content focuses on requests to AI services to produce ad material such as text, images and videos. As such, the following list illustrates the domains that compose this business.
- User domain
- AI domain
- Target domain
- Prompt domain
- Generated content domain
- Channel domain
#### 4.2 Prompt Ads Domains
Prompt ads manages the creation of new marketing campaigns.
- User domain
- AI domain
- Organization domain
- Campaign domain
- Ad domain
- Target domain
- Reaction domain
- Channel domain
- Client domain
- Payment domain
#### 4.3 Prompt CRM Domains
Prompt CRM has the goal to follow activity of interested customers.
- User domain
- AI domain
- Target domain
- Channel domain
- Client domain
- Sales domain
- Marketing services domain
- Payment domain
#### 4.4 Prompt Sales Domains
- User domain
- AI domain
- Organization domain
- Campaign domain
- Ad domain
- Target domain
- Channel domain
- Client domain
- Payment domain
- Services domain

#### Diagram
The following is an image of the Domain Driven Design backend. The frontend communicates through an API and has access to all sub-businesses. 

The main application PromptSales gains access to Prompt Content, Prompt Ads and Prompt CRM through the infrastructure layer with a facade. From this point, it uses an ETL approach to obtain data from sub-businesses and syncronize information.

![DDD Diagram](img/DomainDrivenDesign.png)
Check the pdf file to gain a better look of this diagram: [DomainDrivenDesign-Diagram](diagrams/DomainDrivenDesign.pdf)
