# TODO

- [ ] knative skalierung testen
- [ ] knative scale to zero kommt zu kubernetes?
  
- [ ] Micronaut -> graalvm -> lambda
- [ ] micronaut and azure functions

- [ ] openFaas usw nutzen in der Industrie 

- [ ] performance vergleich; aws lambda vs knative 
- [ ] container overhead?
- [ ] delta zwischen lokalem start und plattform start
  - [ ] delta zwischen quarkus, spring usw.

- [ ] cold start:
  - [ ] viele anfragen auf einmal auf einen cold start
  - [ ] ein cold start
  - [ ] wie funktioniert der cold start setup?
      - knative via buffer erwähnen




# ISSUES

## AWS
### FAILED
- maven only deploy.sh version works somewhat

quarkus:
- mvnw package -Pnative failed => FIXED

- generates function zip

- lambda generates runtime exit error

  

gradle version:
- includes no deploy.sh or dockerfile
- gradlew nativeImage failed (FIXED to at least produce native executable -> no function.zip tough)
- gradlew dockerBuldNative failed
- gradlew assemble and then 
    ``` 
    native-image --no-server -cp buold/libs/break-even-mn-lambda-0.1-all-jar 
    ```
    failed


maven:
- sam-local.sh failed
- mvnw package -Dnative succesful for micronaut BUT
  - did not actually build a native image?
- mvn package then native-image failed

complete repo:
- for the "complete" sample repos: uploading jar does not work -> results in timeout 
- building example projects function.zip works (via deploy.sh)
  - default function (json) calls are successfull but return 405 code 
  - FIXED: use api-gateway test instead of simple function test since application sample uses api gateway for requests
  - RESULT: 800 ms warm start , 2140 ms cold start

packages
- aws-lambda + graalvm failed
- aws-lambda + aws-lambda-customruntime + graalvm failed
- aws-lambda-customruntime + graalvm failed
- example "complete" project includes aws + customruntime + graal (doc does not mention customruntime tough)
- custom runtime package failed -> use only aws + graalvm ?
  - building works but calling fails with runtime exiting without providing a reason

=> note:
    maybe runtime error caused by difference between amazon linux and system used to build native image

### ERROR CORRECTION
in complete:
increase Xmxx size to at least 256 in bootstrap file to function properly


## KOTLESS:

aws educate doesnt allow generating users; so uploading code via direct kotless deployment doesnt work or needs a workaround