# network-scrapper

Pending:
2. clean-up readme
3. create video

## Description

### Gateway Service
TODO
### Scraping
TODO
### Data Storage
TODO

## Architecture and Design
TODO

## APIs and Usage
Interaction with the project is through the flask gateway server which have the below two APIs exposed:

1. API to trigger selenium scrapers
    - The body requires a list of json objects. Username and password can be blank or omitted.
    - If body contains a list of "n" objects, "n" kubernetes jobs will be parallely spawned to capture the respective HAR data
    ```
    curl --location 'http://127.0.0.1:<minikube_tunnel_port>/scrape/network' \
    --header 'Content-Type: application/json' \
    --data '[
        {
            "url": "https://google.com",
            "username": "",
            "password": ""
        }
    ]'
    ```
2. API to get the stored HAR data:
    - returns the HAR for the mentioned url as a json
    - If not present, returns null
    ```
    curl --location 'http://127.0.0.1:<minikube_tunnel_port>/get/full' \
    --header 'Content-Type: application/json' \
    --data '{
        "url": "https://google.com"
    }'
    ```

## Local Setup
1. Kubernetes setup (ignore if kubernetes cluster already exists)
    - Minikube was used for this project but the same can be deployed on any kubernetes cluster once the docker images are pushed to a remote repository
    - install minikube - `brew install minikube`
    - install docker desktop and cli
    - start the kubernetes cluster - `minikube start`
    - switch to using docker of the minikube env so that local docker images can be used directly without pushing to a remote repository - `eval $(minikube docker-env)`
    - setup kubectl and create a namespace `scrapper` (used for all the project related deployments)

2. build docker image for flask gateway server
    ```
    docker build -t network-scapper:latest -f app/Dockerfile .
    ```

3. build docker image for selenium job
    ```
    docker build -t network-scapper-selenium-job:latest -f job/Dockerfile .
    ```

4. apply deployment file for flask gateway server
    ```
    kubectl -n scrapper apply -f app/deployment-svc.yaml
    ```

5. apply role bindings to allow flask gateway server to create jobs in the same kube namespace
    ```
    kubectl -n scrapper apply -f role.yaml
    kubectl -n scrapper apply -f role-binding.yaml
    ```
6. setup standalone mongo instance
    ```
    kubectl -n scrapper apply -f mongo/deployment.yaml
    ```
7. start service tunnel on minikube to access flask gateway server (if using minikube)
    ```
    minikube service flask-gateway-server -n scrapper
    ```


## Connect to Mongo instance:
pre req - `brew install mongosh`

1. `kubectl -n scrapper port-forward service/mongo 27017:27017`
2. `mongosh -u admin -p password --authenticationDatabase admin`