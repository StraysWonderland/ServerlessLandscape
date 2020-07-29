
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

- startup time metriken erfassen
- container overhead?


- statistiken/version usw zu frameworks

# what is serverless?

quick description of what we consider as serverless functions.

- event-driven
- short lived

- fast startup 
- code centric paradigm

# Development

- benefit of using microframework: reuse of developer knowledge, skillset and workflow
  - no new language or development method to "learn"


# Quarkus

Quarkus is a full-stack, Kubernetes-native Java framework mainly aimed at building microservices and tailored for Java virtual machines (JVMs) and native compilation via GraalVM, optimising Java specifically for containers and enabling it to become an effective platform for serverless, cloud, and Kubernetes environments.


- Java Microframework optimized for kubernetes and graalVM
- "Designed for Developers"
  - Hot reload
  -  Unified imperative and reactive programming
  -  Unified configuration
  -  Easy native executable generation
  -  Best-of-Breed Libraries and Standards
- Fast Startup (tens of milliseconds)
  - allows automatic scaling up and down of microservices on containers and Kubernetes as well as FaaS on-the-spot execution
- Low memory utilization
  - Low memory utilization helps optimize container density
- Smaller application and container image footprint
- testing support:
  - hot reload
  - packages to gather metrics 
  - annotations to set up tests easily


#### References

- [Red Hat: Quarkus introduction](https://developers.redhat.com/blog/2019/03/07/quarkus-next-generation-kubernetes-native-java-framework/)

- [Red Hat: what is quarkus](https://www.redhat.com/en/topics/cloud-native-apps/what-is-quarkus)



## Scaffolding

Quarkus allows to easily setup a scaffold project that includes a simple hello world function and a test.
This boilerplate project helps to quickly set-up a function with minimal effort.

```bash
mvn io.quarkus:quarkus-maven-plugin:1.1.1.Final:create \
    -DprojectGroupId=info.novatec \
    -DprojectArtifactId=breakevencalculator \
    -DclassName="info.novatec.BreakEvenCalculator" \
    -Dpath="/run"
```

- or create via https://code.quarkus.io/

## BreakEvenFunction

Example of a simple BreakEvenFunction achieved via Quarkus.

No Additional code or classes ( no application class either ) needed.

Spring like, self-explanatory annotations:

```java
@GET
@Produces({MediaType.APPLICATION_JSON})
public BreakEvenResponse calculate(@QueryParam double price, 
                                   @QueryParam double fixedCost, 
                                   @QueryParam double unitCost) { 
    int breakEvenPoint =  (int) Math.ceil(fixedCost / (price - unitCost));
    BreakEvenResponse response = new BreakEvenResponse(breakEvenPoint);
    return response;
}
```

### Run the Application in development mode with hot reload

Making changes to the code will automatically and instantly recompile and update the application, making local testing easy.

```bash
./mvnw compile quarkus:dev
```



## Testing

Example of creating a Test for the BreakEvenFunction.
Quarkus annotations for easy setup.

```java
@Inject
BreakEvenResponse response;

@ParameterizedTest
@CsvSource({
        "20.00, 100.00, 10.00, 10",
        "6.00, 1000.00, 4.00, 500",
        "2.30, 333.33, 2.10, 1667",
        "3.00, 8000.00, 1.50, 5334"}
)
public void testBreakEvenFunction(double price, double fixedCost, double unitCost, int breakEvenPoint) {
    response.breakEvenPoint = breakEvenPoint;
    given().queryParam("price", price)
            .queryParam("fixedCost", fixedCost)
            .queryParam("unitCost", unitCost)
            .when().get("/run")
            .then()
            .statusCode(200)
            .equals(response);
}
```

### Run the test
when compiling the quarkus project, all tests will be run automatically.

Explicit test run possible as well via:
```bash
./mvnw test
```

## Extensions: Health

Quarkus provides a set if bst-of-Breed Libraries and Standards to extend your functions with additional metric collection, health services or security tools.

### Adding the package
```bash
./mvnw quarkus:add-extension -Dextensions="health"
```

### Or add following to pom.xml
```xml
<dependency>
    <groupId>io.quarkus</groupId>
    <artifactId>quarkus-smallrye-health</artifactId>
</dependency>
```
### Anotation

- the liveness check accessible at /health/live
    ```java
    @Liveness
    ``` 

- the readiness check accessible at /health/ready
    ```java 
    @Readiness
    ``` 

### Implementing Health check

```java
@Liveness
@ApplicationScoped
public class SimpleHealthCheck 
    implements HealthCheck {

    @Override
    public HealthCheckResponse call() {
        return HealthCheckResponse.
            up("Simple health check");
    }
}
```  

## Extensions: Metrics

### Adding the package
```bash
./mvnw quarkus:add-extension -Dextensions="metrics"
```

### Anotation
```java
@Timed(name = "breakEvenTimer", description = "execution time of breakEvenFunction",
            unit = MetricUnits.MILLISECONDS)
```

### Review generated metrics
```
localhost:8080/metrics/
```

## Running & Packaging

### using maven

- compile in development mode
```bash
./mvnw compile quarkus:dev
```

- package into native executable
```bash
 ./mvnw package -Pnative
```
    add to pom.xml
    ```xml
    <profiles>
        <profile>
            <id>native</id>
            <properties>
                <quarkus.package.type>native</quarkus.package.type>
            </properties>
        </profile>
    </profiles>
    ```

### - using dockerfile

```yaml
## Stage 1 : build with maven builder image with native capabilities
FROM quay.io/quarkus/centos-quarkus-maven:19.2.1 AS build
COPY src /usr/src/app/src
COPY pom.xml /usr/src/app
USER root
RUN chown -R quarkus /usr/src/app
USER quarkus
RUN mvn -f /usr/src/app/pom.xml -Pnative clean package

## Stage 2 : create the docker final image
FROM registry.access.redhat.com/ubi8/ubi-minimal
WORKDIR /work/
COPY --from=build /usr/src/app/target/*-runner /work/application
RUN chmod 775 /work
EXPOSE 8080
CMD ["./application", "-Dquarkus.http.host=0.0.0.0"]
```




# Micronaut

"A modern, JVM-based, full-stack framework for building modular, easily testable microservice and serverless applications."


- tailored for graalvm
- fast startup time

## Micronaut & Azure functions?



# Kotless

"Kotlin serverless framework"

Focus on simplifying serverless deployment creation workflow

consists of:
- DSL to define serverless applications
  - also offers support for ktor or spring boot
- Gradle Plugin to deploy to AWS (or locally)

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

--- 

# OpenFaas
OpenFaaS is a framework for building Serverless functions on top of containers and deployment on any cloud or on-premise.
The goal is to enable developers to deploy event-driven functions and microservices to Kubernetes without repetitive, boiler-plate coding.

OpenFaas allows you to write functions in any language for Linux or Windows and package in Docker/OCI image format.
The faas-cli can build a container for your code using a yaml file configuration and language template either from its own template store, or any github repository specifying a template such as [this template for quarkus](https://github.com/pmlopes/openfaas-quarkus-native-template).
This workflow adds a watchdog component to the container and thus allows any process to become a serverless function with auto-scaling and metrics.

(drawback?? applies to all plattforms?)
However, the fact that you have to build your images from the ground up can be considered a major drawback.
You cant just ship and deploy your already existing images for functions that have been build for other vendors directly to openfaas. 
Youll have to specify the yaml configuration tailored for openfaas and let the faas-cli build it.

- Ease of use through UI portal and one-click install
- 
- Portable 
  - runs on existing hardware or public/private cloud 
  -  Kubernetes and Docker Swarm native
- Auto-scales as demand increases

OpenFaas also offers a function-store with some useful predefined functions such as sentiment analysis, face detection, text to speech and nsfw detection.
These functions can easily be deployed via the faas-cli directly from the store.
Developers can also contribute to the function store, which may lead to a great variety of ready to use functions in the future.
 
## workflow

https://github.com/openfaas/workshop


- create kubernetes or docker swarm cluster
- install openfaas using either helm or arkade
- install faas-cli
- create a function scaffold using faas-cli and specifying desired language
- build image for your function and deploy it directly to openfaas via 
    ```bash faas-cli up```

## benfits
- run on any public or private cloud
- Run container based functions on own servers
- runs on docker swarm or kubernetes

- configuration overhead?

## architecture?

## stats

- 18.1 stars
- 1.5k forks
- 1,912 regular commits ( mostly lass than a week between commits)
- 150 contributors
## References

- [openfaas on minikube](https://medium.com/faun/getting-started-with-openfaas-on-minikube-634502c7acdf)
- [what is openfaas and why is it an alternative to aws lambda](https://www.contino.io/insights/what-is-openfaas-and-why-is-it-an-alternative-to-aws-lambda-an-interview-with-creator-alex-ellis)

---
---
---

# FN Project

The Fn project is, as the developers describe it on thei [homepage](https://fnproject.io/), an open-source container-native functions-as-a-servuce platform that you can run anywhere.
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

    an app is a collection of functions that you can use to organise your functions

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
- avoid vendor lock-in

## Drawbacks


## architecture?


# stats
- 4.7K stars
- 348 forks
- 3393 commits (last in dec 2019)
  - semi active
- 86 contributors
  
# RIFF is for functions

riff is an Open Source platform for building and running Functions, Applications, and Containers on Kubernetes. 

- simplifies deployment and iteration workflow
  ```bash
  riff function create breakeven \
    --git-repo https://example.com/my/repo \
    --image my/breakeven
  ```
- CLI to create and deploy functions
- create knative deployments easily
- streaming??
  
---

# Deployment on FAAS vendors

# Serverless Framework

- simplifies configuration and deployment of functions to aws lambda, azure functions etc.
- streamlines deployment across different vendors