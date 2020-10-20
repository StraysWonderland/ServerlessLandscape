
# Load Testing

## microframework comparison

Comparing the run time of the break even function written in different Microframeworks.
Comparison is done by running them localy via minikube and load testing with locust.

|     | Micronaut | Quarkus | delta |
|:---:|:--------: |:------:|:----:|
| mean| 13        | 10     | 3    |
| min | 2         | 3      | -1   |
| max | 50        | 44     | 6    |

Since both frameworks use graalVM to create a native executable, the execution time is quite similar with no significant difference betweend them

### comparison to spring 
|     | Micronaut | SPRING | delta |
|:---:|:--------: |:------:|:----:|
| mean| 13        | 0     | 0   |
| min | 2         | 0     | 0   |
| max | 50        | 0     | 0   |

## platform comparison

Comparing the break even function written with Micronaut on different Serverless Platforms.
Load Testing done via locust framework.

|     | local | Knative| OpenFaas | FN | AWS | Azure |
|:---:|:--------:  |:---:|:------:|:----:|:---: | :---:  |
| mean| 13         | 6  | 16     | 0  | 0 | 0 |
| min | 2          | 3  | 5      | 0  | 0 | 0 |
| max | 50         | 23 |92     | 0  | 0 | 0 |

- significant difference between knative and OpenFaas

### cold start

Each platforms required execution time for a cold start, i.e. when there are no active replicas.

#### Exectution time for a single request

|     |  Knative | OpenFaas | FN | AWS | Azure |
|:---:| :---: |:------:|:----:|:---: | :---:  |
| execution time|   0   | 260     | 0  | 0 | 0 |

#### Starting a lot of requests on cold start

|     | Knative | OpenFaas | FN  | AWS | Azure |
|:---:|:-------:|:--------:|:---:|:---:|:---:  |
| mean|         | 20       | 0   | 0   | 0 |
| min |         | 7        | 0   | 0   | 0 |
| max |         | 9326     | 0   | 0   | 0 |
| avg |         | 260      | 0   | 0   | 0 |

OpenFaas has a very high max execution time if a lot of requests come in at the same time on a cold start.
Explanation?


## AWS

FAT JAR
cold start: 27.22 ms | 30.36 | 
warm start 1.31 ms | 1.29

NATIVE EXECUTABLE

---

![openfaas test](Images/monitoring_breakeven_kotlin_lambda_dashboard.PNG) 



API Gateway

max 1024ms
avg 22ms
min 17ms