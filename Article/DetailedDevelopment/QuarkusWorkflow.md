
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
-   add to pom.xml
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

#### References

- [Red Hat: Quarkus introduction](https://developers.redhat.com/blog/2019/03/07/quarkus-next-generation-kubernetes-native-java-framework/)

- [Red Hat: what is quarkus](https://www.redhat.com/en/topics/cloud-native-apps/what-is-quarkus)

