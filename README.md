# network-scrapper

Pending:
1. test the username+password auth

Questions:
1. Do we only need to capture network calls or request/response data as well?
2. 


Setup
1. brew install minikube
2. install docker
3. minikube start
4. switch docker env to minikube; `eval $(minikube docker-env)`
5. build docker image for svc `docker build -t network-scapper:latest -f Dockerfile .`
6. apply deployment file `kubectl -n scrapper apply -f deployment-svc.yaml` 
7. start service tunnel `minikube service flask-gateway-server -n scrapper`
8. hit api and test


Connect to Mongo instance:
pre req - `brew install mongosh`

1. `ktemp port-forward service/mongo 27017:27017`
2. `mongosh -u admin -p password --authenticationDatabase admin`