
# Serverless Landscape

- [serverless landscape](https://landscape.cncf.io/format=serverless)

- [faastener](https://faastener.github.io/explorer)

# what is serverless?
Serverless in the course of this article will be defined as paradigm to simplify and speed up deployment of code that is 
- event driven
- short lived
- has fast startup 
- abstracted or "hidden" infrastructure

and where this paradigm enables event triggered autoscaling and scale to zero.

---
# Development: using Microframeworks
Using Microframeworks that ease the creation of serverless functions has the benefit of reusing the skillset, knowledge and workflow of developers familiar with microservices.
No need to switch to a new framework or workflow if the framework you are using for your microservices also is suited for the creation of serverless functions.

A major benefit of using microframeworks to develop serverless functions is that developers reuse their knowledge and skillset of creating microservices.
There is no new language or development method to "learn" and the workflow remains the same, so that creating serverless functions are seemlessly integrated into the usual workflow.

---
## Quarkus
---
Quarkus is a full-stack, Kubernetes-native Java framework mainly aimed at building microservices and tailored for Java virtual machines (JVMs) and native compilation via GraalVM, optimising Java specifically for containers and enabling it to become an effective platform for serverless, cloud, and Kubernetes environments.


### Benefits

- "Designed for Developers"
- Hot reload
- Unified imperative and reactive programming
- Unified configuration
- Easy native executable generation
- best-of-Breed Libraries and Standards to extend your functions withadditional metric collection, health services or security tools.
- Fast Startup (tens of milliseconds)
  - allows automatic scaling up and down of microservices on containers and Kubernetes as well as FaaS on-the-spot execution
- Low memory utilization
  - Low memory utilization helps optimize container density
- Smaller application and container image footprint
  
- #### Project scaffolding
  - Quarkus allows to easily setup a scaffold project that includes a simple hello world function and a test. This boilerplate project helps to quickly set-up a function with minimal effort.
    ```bash
    mvn io.quarkus:quarkus-maven-plugin:1.1.1.Final:create \
        -DprojectGroupId=info.novatec \
        -DprojectArtifactId=breakevencalculator \
        -DclassName="info.novatec.BreakEvenCalculator" \
        -Dpath="/run"
    ```

- #### testing support:
  - hot reload
  - packages to gather metrics 
  - annotations to set up tests easily
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
    public void testBreakEvenFunction(double price, double fixedCost, doubleunitCost, int breakEvenPoint) {
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
### BreakEvenFunction

Example of a simple BreakEvenFunction achieved via Quarkus.
No Additional code or classes ( no application class either ) needed.

- Spring like, self-explanatory annotations:
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


### package into native executable

- either package on your machine
    ```bash
    ./mvnw package -Pnative
    ```
- add to pom.xml
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

- or use Dockerimage
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

---
## Micronaut
---
"A modern, JVM-based, full-stack framework for building modular, easily testable microservice and serverless applications."

It enables you to write applications in Java, Kotlin or Groovy.

### Benefits

- also tailored for graalvm
- fast startup time
- reduced memory footprint
- compile time dependency injection instead of reflection
- provides packages to ease development for different tasks

### Micronaut & AWS Lambda
Micronaut offers packages/features to create functions designed for deployment on aws lambda.
These packages are mainly the "aws-lambda" package, and when planing to deploy a native executable created via graalvm, also the "graal-vm" and "aws-lambda-custom-runtie" packages.

Either add these packages to new projects via the _Micronaut_Launch_ website or the CLI, or add them into an existing project.

When writing the function, simply include the ```java extends MicronautRequestHandle<T,T> ```
  ```java
  @Introspected
  public class BreakEvenRequestHandler extends MicronautRequestHandler<BreakEvenRequest, BreakEvenResponse> { 
  
      @Override
      public BreakEvenResponse execute(BreakEvenRequest request) {
          BreakEvenResponse breakEvenResponse = new BreakEvenResponse();
          breakEvenResponse.breakEvenPoint = (int) Math.ceil(request.fixedCosts / (request.price - request.unitCosts));
          return breakEvenResponse;
      }
  }
  ```
If you include the _graalvm_ and _aws-lambda-custom-runtime_ packages, building the project will generate a function.zip archive, that can be uploaded directly to aws lambda.

### Micronaut & Azure functions

- create project via micornaut launch
  - either micronaut app
  - or serverless function
- add package azure-function or azure-function-http
- package provides gradle deploy task which allows direct deployment to azure


### Limitations

The main problem with building functions for aws/azure via micronaut is, that the workflow is a bit convoluted as i.e. the required deploy.sh script is not in any created project by default and that the default package versions can lead to compatibility issues across different versions.
While these can be easy to spot and fix for developers experienced in working with micronaut, graalvm and aws, for developers newly diving into serverless, these issues can be difficult and frustrating to spot/fix, and will make the workflow fail entirely. 
Also, the aws package does not provide a deploy task as the azure package does.


---
## Kotless
---
"Kotlin serverless framework"

Focus on simplifying serverless deployment creation workflow

consists of:
- DSL to define serverless applications
- also offers support for ktor or spring boot
- Gradle Plugin to deploy directly to AWS or test locally

Kotless also allows to work with either the ktor or the spring boot dsl, which is recommendet as kotless own dsl.

The framework ist still in a very early stage as the latest version ist 0.7-beta-5, and thus currently lacks functionalities such as serialization, and support for the latest kotlin version.
Also, as of writing this article, it only supports AWS lambda, though support for Google and Azure is planned for sometime in the future.


### Workflow
- add to gradle.build.kts
    ```yaml
    import io.kotless.plugin.gradle.dsl.kotless
    .
    .
    .
    plugins {
    kotlin("jvm") version "1.3.61" apply true
    id("io.kotless") version "0.1.3" apply true
    }
    .
    .
    .
    repositories {
    jcenter()
    }
    .
    .
    .
    dependencies {
    implementation("io.kotless", "lang", "0.1.3")
    ...
    }
    ```

- Write function with standard kotlin using kotless annotations for paths
    ```java
    @Post("/")
    fun execute(request: BreakEvenRequest): BreakEvenResponse {
        val breakEvenPoint = ceil(request.fixedCosts / (request.price - request.unitCosts)).toInt()
        return BreakEvenResponse(breakEvenPoint = breakEvenPoint)
    }
    ```
- also supports ktor dsl
    ```kotlin
    class Server : Kotless() {
        override fun prepare(app: Application) {
            app.routing {
                post("/") {
                    val breakEvenRequest = call.receive<BreakEvenRequest>()
                    val breakEvenPoint =
                            ceil(breakEvenRequest.fixedCosts / 
                                (breakEvenRequest.price - breakEvenRequest.unitCosts)).toInt()
                    call.respond(breakEvenPoint)
                }
            }
        }
    }
    ```
- testing locally:
  - execute the *gradle.kotless.local* task 
  - 
- Upload directly to aws using the kotless gradle task
  - add to *build.gradle.kts*
  ```yaml
  kotless {
    config { 
        bucket = "my.kotless.bucket"
  
        terraform {
            profile = "my.kotless.user"
            region = "eu-west-1"
        }
    }
    webapp {
        lambda {
            kotless {
                packages = setOf("com.example.kotless")
            }
        }
    }
  } 
  ```
  - run gradle *deploy* task

### Limitations
As Kotless is still in a very early stage we have encountered a lot of problems, mainly around compatibility with other libraries and with different gradle and kotlin version.
We have also encountered an issue with the deploy task leading to a malformed terraform file which lead made it impossible to deploy.

### Conclusion
While kotless in theory provides a simplifyed serverless coding and deployment creation workflow, the erros, incompatiblity, lacking features such as serialization and the slow development time are to be considered.
Therefore, our conclusion is that Kotless is not yet ready to be used in production.

---
# Deployment on FAAS vendors
Probably the most common approach to serverless is to deploy your code to one of the popular serverless function platform vendors such as AWS lambda, Azure Functions or Google Cloud Functions.

These vendors offer you a platform to which you, with a little deployment configuration, can directly deploy your code and the platform takes care of and hides all the required infrastructure configuration from the developer.
The configuration of your deployment usually contains vendor specific commands.

# AWS lambda
AWS lambda is among the most popular serverless function plattform vendors.

- upload code via CLI or link to github repo
- supports various different runtimes such as java, nodejs, python, Go ...
  - custom runtimes can be specified too
  - micronaut and quarkus provide packages for aws lambda with their own runtime for native executables

## workflow
- create functions either via the aws console or via the CLI called SAM
    - SAM provides commands for initialising, building and deploying functions as well as local testing.
- for using the web console
  - create a jar or zip file and upload it

### using Microframeworks
- Micronaut and Quarkus offer packages to build functions optimised for lambda
- Application can be deployed either using the lambda java runtime, or by bulding a native executable with a custom runtime provided by the corresponding package
  - easy native packaging and deployment
  - ```bash mn create-app info.novatec.break-even --lang=kotlin --features aws-lambda,graalvm ```
  - either create a jar file 
  - or let the aws lambda package create a zip folder to upload
    - project requires a bootstrap file
    - ONLY REQUIRED IN OLDER VERSIONS: edit bootsrap file to include
      - increase Xmxx size to at least 256 in bootstrap file to function properly
    - also set the memory usage on lambda accordingly, either via config file or in the web console
    - generate a native image preferably with a amazon-linux-docker-image
      - micronaut projects that include the aws and graalvm packages include a deploy.sh script and a dockerfile to build a suitable native image for lambda
  - use lambdas java runtime or custom runtime for native executables
  - both frameworks also provide scripts to test application localy via SAM
  
  

###  Contents of functions.zip
#### Using graalvm package
- contents of function.zip using graalvm to create a executable:
    - bootstrap
        ```bash 
        #!/bin/sh
        set -euo pipefail
        ./break-even-mn-lambda -Xmx512m
        ```
    - break-even-mn-lambda binary file

#### Generating a function.zip without graalvm
```  
  - io
    - quarkus 
      - ...
  - javax
    - ...
  - lib
    - com.amazonaws....
    - ...
  - META-INF
    - services
    - MANIFEST.MF
  - info\novatec\
    - BreakEvenRequestHandler.class
  - application.properties
```
### using SAM
  - test, build and deploy via SAM
    - local test:
        - initiate api
            ```bash
            sam local start-api
            ```
        - single invocations
            ```bash
            sam local invoke "break-even-kotlin" -e events/event.json
            ```
    - build: 
        ```bash
            sam build
        ```
    - deploy: 
        ```bash
            sam deploy --guided
        ```
   
- requires a yaml file
    ```yaml
    AWSTemplateFormatVersion: '2010-09-09'
    Transform: AWS::Serverless-2016-10-31
    Description: AWS Serverless Micronaut API - example.micronaut::prime-finder
    Globals:
    Api:
        EndpointConfiguration: REGIONAL
    Resources:
    BreakEvenKotlin:
        Type: AWS::Serverless::Function
        Properties:
        Handler: not.used.in.provided.runtime
        Runtime: provided
        CodeUri: build/function.zip
        MemorySize: 128
        Policies: AWSLambdaBasicExecutionRole
        Timeout: 15
        Events:
            GetResource:
            Type: Api
            Properties:
                Path: /{proxy+}
                Method: any
    Outputs:
        BreakEvenKotlin:
            Description: URL for application
            Value: !Sub 'https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/find-primes-below/{number}'
            Export:
            Name: BreakEvenKotlin
    ```

---
# Azure Functions


- micronaut package: micronaut-azure-function
  - provides azure functions for running localy, packaging and deploying directly to azure
  - deployment can be done either via the gradle/maven task provided by the package,
    - requires a small amount of configuration
  - or by using the visual studio code azure integration
    - vs code integration makes it really easy to deploy with just a few clicks and no configuration
    - currently only supports maven projects
- While Azure does support native images packaged by graalvm, creating and uploading one is not as straightforward as with the packages provided for aws by quarkus and micronaut
    ```kotlin 
    class Function : AzureFunction() {
        @FunctionName("breakeven")
        fun breakeven(
                @HttpTrigger(
                        name = "name",
                        methods = [HttpMethod.POST],
                        authLevel = AuthorizationLevel.ANONYMOUS)
                price: Double, unitCosts: Double, fixedCosts: Double): Int {
            return ceil(fixedCosts / (price - unitCosts)).toInt()
        }
    }
    ```
--- 
# Deployment Anywhere
- use language & infrastructure you`re familiar with
- one system to manage and operate for all applications
- only serverless from a user perspective  
- avoid vendor lock-in
- avoid limitations of cloud vendors 
  - i.e. timeout
- build functions and microservices in any languange with same deployment mechanism
  - lambda "only" supports java, node, python, c# and go

There is a number of plattforms that enable you to deploy and manage serverless functions.
Nameworthy examples are:
- AWS Lambda
- Microsoft Functions
- Google Cloud Functions
- Apache OpenWhisk
- Fission
- FN Project
- Knative
- Kubeless
- Nuclio
- OpenFaas

We will take a look into a few of those

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

```yml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
 name: helloworld-go
 namespace: default
spec:
 template:
  spec:
   containers:
    - image: gcr.io/knative-samples/helloworld-go
      env:
        - name: TARGET
          value: "Go Sample v1"
```

## stats
- Stars: 2700
- Forks: 563
- Commits: 3800
- Contributors: 165
- Issues: 274 


most active of the platforms

## Performance
![openfaas test](Images/monitoring_breakeven_kotlin_kubernetes.PNG) 


---

# OpenFaas
OpenFaaS is a framework for building Serverless functions on top of containers and deployment on any cloud or on-premise.
The goal is to enable developers to deploy event-driven functions and microservices to Kubernetes without repetitive, boiler-plate coding.

OpenFaas allows you to write functions in any language for Linux or Windows and package in Docker/OCI image format.
The faas-cli can build a container for your code using a yaml file configuration and language template either from its own template store, or any github repository specifying a template such as [this template for quarkus](https://github.com/pmlopes/openfaas-quarkus-native-template).
This workflow adds a watchdog component to the container and thus allows any process to become a serverless function with auto-scaling and metrics.
This simplifies the deployment of functions greatly so that deploying a function to OpenFaas is effortlessly easy through the ability to deploy functions via UI portal and one-click install.
This workflow and the configuration of a function through yaml is much simpler compared to kubernetes, which is the main strength of OpenFaas.

- typical kubernetes yaml
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
    name: nginx-deployment
    labels:
        app: nginx
    spec:
    replicas: 3
    selector:
        matchLabels:
        app: nginx
    template:
        metadata:
        labels:
            app: nginx
        spec:
        containers:
        - name: nginx
            image: nginx:1.7.9
            ports:
            - containerPort: 80
    ```
- compared to typical OpenFaas yaml
    ```yaml
    version: 1.0
    provider:
        name: openfaas
        gateway: http://127.0.0.1:8080
    functions:
        break-even-kotlin:
            lang: kotlin-maven-mn
            handler: ./break-even-kotlin
            image: straywonderland/break-even-kotlin:latest
    ```

However, the fact that you have to build your images from the ground up can be considered a major drawback.
You cant just ship and deploy your already existing images for functions that have been build for other vendors directly to openfaas. 
Youll have to specify the yaml configuration tailored for openfaas and let the faas-cli build it.

- Portable 
  - runs on existing hardware or public/private cloud 
  -  Kubernetes and Docker Swarm native
- Auto-scales as demand increases

OpenFaas also offers a function-store with some useful predefined functions such as sentiment analysis, face detection, text to speech and nsfw detection.
These functions can easily be deployed via the faas-cli directly from the store.
Developers can also contribute to the function store, which may lead to a great variety of ready to use functions in the future.

Auto-scaling in OpenFaas can be configured within the yaml file of a deployed function.
Per default it is set to always keep at least one replica, and scale the number of replicas up to a maximum of 20 if a large amount of requests come in.
This means, that per default, there is no scale-to-zero but that at all times one image is kept up and running for each function.
Keeping a replica up reduces the average response time, since there are no cold starts.
And since youre deploying OpenFaas on a cloud plattform, this does not produce any cost-overhead as it would with a pay-per-use model of serverless providers.
OpenFaas does however support scale from and to zero by editing the configuration for the minimum number of replicas or setting it via
```bash 
kubectl scale deployment --replicas=0 break-even-kotlin -n openfaas-fn 
```

## benefits
- run on any public or private cloud
- Run container based functions on own servers
- runs on docker swarm or kubernetes


## workflow
https://github.com/openfaas/workshop

- create kubernetes or docker swarm cluster
- install openfaas using either helm or arkade
- install faas-cli
- create a function scaffold using faas-cli and specifying desired language
    ```bash
        faas-cli new --lang java breakeven
    ```
    - or add a yaml file to the directory of an existing project
    ```yaml
    version: 1.0
    provider:
        name: openfaas
        gateway: http://127.0.0.1:8080
    functions:
        break-even-kotlin:
            lang: kotlin-maven-mn
            handler: ./break-even-kotlin
            image: straywonderland/break-even-kotlin:latest
    ```
- build image for your function and deploy it directly to openfaas via 
    ```bash faas-cli up```


## stats
- 18.1 stars
- 1.5k forks
- 1,912 regular commits ( mostly lass than a week between commits)
- 150 contributors

OpenFaas seems to be quite active and being continuesly developed.

## Performance
Load testing on micronaut break-even function
| Median | 90%ile | Min  | Max |
| :----: |:------:|:----:|:---:|
| 16     | 53     | 5    | 92  |

![openfaas test](/Images/monitoring_breakeven_kotlin_openfaas.PNG) 
![openfaas test](/Images/response_times_openfaas.PNG) 

---
---

# FN Project
The Fn project is, as the developers describe it on their [homepage](https://fnproject.io/), an open-source container-native functions-as-a-service platform that you can run anywhere.
So wether you want to deploy serverless functions on a cloud vendor architecture or on-premise, Fn project delivers easy to use deployment of functions written in any programming language.

## Benefits
- scaffolding
- function development kits for mapping in and output
- focus on ease of deployment on any cloud and on-premise
- load balancing
- hot containers for fast response time
- one system to manage and operate for all applications
- avoid vendor lock-in

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

- or add a configuration file to an existing repo
    ```yml
    schema_version: 20180708
    name: javafn
    version: 0.0.1
    runtime: java
    build_image: fnproject/fn-java-fdk-build:jdk11-1.0100
    run_image: fnproject/fn-java-fdk:jre11-1.0.100
    cmd: com.example.fn.breakeven::handleRequest
    ```
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

## stats
- Stars: 4700
- Forks: 348
- Commits: 3400
  - last in dec 2019
  - semi active
- Contributors: 86
- Issues: 121 


---
---

---

# Kubeless
Kubeless is a Kubernetes-native serverless framework that lets you deploy functions without having to worry about the underlying infrastructure. It is designed to be deployed on top of a Kubernetes cluster and take advantage of all the great Kubernetes primitives. If you are looking for an open source serverless solution that clones what you can find on AWS Lambda, Azure Functions, and Google Cloud Functions, Kubeless is for you!

Kubeless Includes:
- Support for Python, Node.js, Ruby, PHP, Golang, .NET, Ballerina
- supports custom runtimes
- CLI compliant with AWS Lambda CLI
- Event triggers using Kafka messaging system and HTTP events
- Prometheus monitoring of functions calls and function latency by default
- Serverless Framework plugin



---

# Serverless Framework
The serverless framework offers tools for the entire serverless application lifecycle, beyond "just" development and deployment
- simplifies configuration and deployment of functions to aws lambda, azure functions etc.
- allows scaffolding of projects
- streamlines deployment across different vendors
- offers monitoring and testing tools

## workflow
to deploy via serverless, a ```serverless.yml``` file is required.
This is automatically added when creating a scaffold through the serverless cli will, or can be added manually and a minimal example looks as follows

```yaml

    frameworkVersion: '2'

    provider:
    name: aws
    runtime: java8
    lambdaHashingVersion: 20201221

    # you can overwrite defaults here
    stage: dev
    region: us-east-1

    package:
    artifact: target/hello-dev.jar

    functions:
    hello:
        handler: com.serverless.Handler
```
creating a scaffold via the cli is done via the ```serverless create``` command and requires  chosing a  template for the desired provider and language.

For example creating a kotlin maven project for aws is done with the following command:
```bash
serverless create --template aws-kotlin-jvm-maven
```

run ```bash serverless create --help ``` to view the available templates

```bash
Available templates: 
"aws-clojure-gradle", "aws-clojurescript-gradle", "aws-nodejs","aws-nodejs-docker", "aws-nodejs-typescript", "aws-alexa-typescript","aws-nodejs-ecma-script", "aws-python", "aws-python3", "aws-python-docker", "aws-groovy-gradle", "aws-java-maven","aws-java-gradle", "aws-kotlin-jvm-maven", "aws-kotlin-jvm-gradle","aws-kotlin-jvm-gradle-kts","aws-kotlin-nodejs-gradle", "aws-scala-sbt", "aws-csharp", "aws-fsharp","aws-go", "aws-go-dep", "aws-go-mod", "aws-ruby","aws-provided"

"tencent-go", "tencent-nodejs", "tencent-python", "tencent-php"

"azure-csharp", "azure-nodejs", "azure-nodejs-typescript", "azure-python"

"cloudflare-workers", "cloudflare-workers-enterprise","cloudflare-workers-rust"

"fn-nodejs", "fn-go"
"google-nodejs", "google-python", "google-go"
"kubeless-python", "kubeless-nodejs"
"knative-docker"

"openwhisk-java-maven", "openwhisk-nodejs", "openwhisk-php","openwhisk-python", "openwhisk-ruby", "openwhisk-swift"

"spotinst-nodejs", "spotinst-python", "spotinst-ruby", "spotinst-java8"

"twilio-nodejs"
"aliyun-nodejs"
"plugin"
"hello-world"
```

---

# Conclusion about Serverless

