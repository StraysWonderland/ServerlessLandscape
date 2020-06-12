
# Serverless Landscape

 [serverless landscape](https://landscape.cncf.io/format=serverless)

---

- knative skalierung testen
- Micronaut -> graalvm -> lambda
- micronaut and azure functions
- openFaas usw nutzen in der Industrie 

- performance vergleich; aws lambda vs knative 
  - container overhead?

- knative scale to zero kommt zu kubernetes?

# what is serverless?

# Development

- benefit of using microframework: reuse of developer knowledge, skillset and workflow
  - no new language or development method to "learn"


## Quarkus

- Java Microframework 
- optimised for graalVM
- fast startup time
- testing support:
  - hot reload
  - packages to gather metrics 
  - annotations to set up tests easily


## Micronaut

### Micronaut & Azure functions?

---

# Deployment


## Anywhere

- use language & infrastructure youre familiar with
- one system to manage and operate for all applications
- only serverless from a user perspective  
- avoid vendor lock-in
- avoid limitations of cloud vendors 
  - i.e. timeout
- build functions and microservices in any languange with same deployment mechanism
  - lambda "only" supports java, node, python, c# and go

### Knative


### OpenFaas


- run on any public or private cloud
- Run container based functions on own servers
- runs on docker swarm or kubernetes

- configuration overhead?
- architecture?

#### References

- [what is openfaas and why is it an alternative to aws lambda](https://www.contino.io/insights/what-is-openfaas-and-why-is-it-an-alternative-to-aws-lambda-an-interview-with-creator-alex-ellis)

### FN Project

The Fn project is, as the developers describe it on thei [homepage](https://fnproject.io/), an open-source container-native serverless platform that you can run anywhere.
So wether you want to deploy serverless functions on a cloud vendor architecture or on-premise, Fn project delivers easy to use deployment of functions written in any programming language.

- scaffolding
- function development kits for mapping in and output
- focus on ease of deployment on any cloud and on-premise
- load balancing
- hot containers for fast response time
- one system to manage and operate for all applications


- architecture?

## on FAAS
### Serverless Framework

- simplifies configuration and deployment of functions to aws lambda, azure functions etc.
- streamlines deployment across different vendors