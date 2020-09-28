
# Load Testing

## microframework comparison

Comparing the run time of the break even function written in different Microframeworks.
Comparison is done by running them localy via minikube and load testing with locust.

|     | Micronaut | Quarkus | delta |
|:---:|:--------: |:------:|:----:|
| mean| 13        | 10     | 3  |
| min | 2         | 3      | -1  |
| max | 50        | 44     | 6  |

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

|     | Knative | OpenFaas | FN  | AWS | Azure |
|:---:|:-------:|:--------:|:---:|:---:|:---:  |
| mean|         | 20       | 0   | 0   | 0 |
| min |         | 7        | 0   | 0   | 0 |
| max |         | 9326     | 0   | 0   | 0 |
| avg |         | 260      | 0   | 0   | 0 |

#### single request
|     |  Knative | OpenFaas | FN | AWS | Azure |
|:---:| :---: |:------:|:----:|:---: | :---:  |
| exection time|   0   | 260     | 0  | 0 | 0 |

