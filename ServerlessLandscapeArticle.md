
# Serverless Landscape

 [serverless landscape](https://landscape.cncf.io/format=serverless)


## TODO:

- knative skalierung testen
- Micronaut -> graalvm -> lambda
- micronaut and azure functions
- openFaas usw nutzen in der Industrie 

- performance vergleich; aws lambda vs knative 
  - container overhead?

- knative scale to zero kommt zu kubernetes?



# what is serverless?

quick description of what we consider as serverless functions.

- event driven
- short lived



# Development

- benefit of using microframework: reuse of developer knowledge, skillset and workflow
  - no new language or development method to "learn"


# Quarkus

- Java Microframework 
- optimised for graalVM
- fast startup time
- testing support:
  - hot reload
  - packages to gather metrics 
  - annotations to set up tests easily


# Micronaut

## Micronaut & Azure functions?

---

# Deployment Anywhere

- use language & infrastructure youre familiar with
- one system to manage and operate for all applications
- only serverless from a user perspective  
- avoid vendor lock-in
- avoid limitations of cloud vendors 
  - i.e. timeout
- build functions and microservices in any languange with same deployment mechanism
  - lambda "only" supports java, node, python, c# and go

# Knative
"Kubernetes-based platform to deploy and manage modern serverless workloads."

## Benefits
- Focused API with higher level abstractions for common app use-cases.
- Stand up a scalable, secure, stateless service in seconds.
- Loosely coupled features let you use the pieces you need.
- Pluggable components let you bring your own logging and monitoring, networking, and service mesh.
- Knative is portable: run it anywhere Kubernetes runs, never worry about vendor lock-in.
- Idiomatic developer experience, supporting common patterns such as GitOps, DockerOps, ManualOps.
- Knative can be used with common tools and frameworks such as Django, Ruby on Rails, Spring, and many more. 
- 
# OpenFaas
OpenFaaS makes it easy for developers to deploy event-driven functions and microservices to Kubernetes without repetitive, boiler-plate coding. Package your code or an existing binary in a Docker image to get a highly scalable endpoint with auto-scaling and metrics.


- Ease of use through UI portal and one-click install
- Write functions in any language for Linux or Windows and package in Docker/OCI image format
- Portable - runs on existing hardware or public/private cloud - Kubernetes and Docker Swarm native
- CLI available with YAML format for templating and defining functions
- Auto-scales as demand increases


## workflow

https://github.com/openfaas/workshop

## benfits
- run on any public or private cloud
- Run container based functions on own servers
- runs on docker swarm or kubernetes

- configuration overhead?

## architecture?

## References

- [openfaas on minikube](https://medium.com/faun/getting-started-with-openfaas-on-minikube-634502c7acdf)
- [what is openfaas and why is it an alternative to aws lambda](https://www.contino.io/insights/what-is-openfaas-and-why-is-it-an-alternative-to-aws-lambda-an-interview-with-creator-alex-ellis)


# FN Project

The Fn project is, as the developers describe it on thei [homepage](https://fnproject.io/), an open-source container-native serverless platform that you can run anywhere.
So wether you want to deploy serverless functions on a cloud vendor architecture or on-premise, Fn project delivers easy to use deployment of functions written in any programming language.


## Deployment workflow?
[Getting started with FN Guide](https://fnproject.io/tutorials/JavaFDKIntroduction/)

- setup server 
    ```bash
    fn start
    ```

- scaffolding per cli
    ```bash
    fn init --runtime java breakevencalculator
    ```
- edit code

- Create your app
    ```bash
    fn create app breakeven-app
    ```

- deploy your function
    ```bash
    fn deploy --app breakeven-app --local
    ```

- invoke the deployed function
    ```bash
    fn invoke breakeven-app breakevencalculator
    ```

## Benefits
- scaffolding
- function development kits for mapping in and output
- focus on ease of deployment on any cloud and on-premise
- load balancing
- hot containers for fast response time
- one system to manage and operate for all applications

## Drawbacks


## architecture?





# Deployment on FAAS vendors

# Serverless Framework

- simplifies configuration and deployment of functions to aws lambda, azure functions etc.
- streamlines deployment across different vendors