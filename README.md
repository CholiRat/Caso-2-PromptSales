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

### 3.2 Scalability
>>THE DATA IN THIS SECTION IS PROVISIONAL AND REQUIRES FURTHER ADJUSTMENTS

In order to manage scalability, Kubernetes is used to host both the application and its associated databases. It enables dynamic resource allocation and automated deployment of containerized services

The four databases are:
- PromptContent
- PromptAds
- PromptCRM
- Redis cache
The main application is PromptSales. It is the access door to all the related services.

[Check kubernetes configuration folder]( https://github.com/CholiRat/Caso-2-PromptSales/tree/main/kubernetConfig)

Regarding database scalability, SQL Server replicas are inherently limited due to their stateful nature and data consistency requirements. Which is why the scaling will occur in the redis module and the main app.

Here is an example of Horizontal Pod Autoscaling (HPA). 
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: redis-hpa
  namespace: redis-cache
spec:
  scaleTargetRef:				# This file targets the deployment of redis.
    apiVersion: apps/v1
    kind: Deployment
    name: redis-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70		# The autoscale will take place when more than 70% of a pod's cpu is being used
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 75		# The autoscale will take place when more than 75% of a pod's memory is being used
```
It declares a minimum of 2 replicas and maximum of 10. The scale takes place when more than 70% of CPU is being consumed in one pod or 75% of memory is being used instead.

### 3.3 Reliability

### 3.4 Availability

### 3.5 Security

### 3.6 Maintainability

### 3.7 Interoperability

### 3.8 Compliance

### 3.9 Extensibility

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
- Marketing services domain
- Payment domain




