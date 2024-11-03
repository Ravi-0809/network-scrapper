# network-scrapper

Pending:
2. clean-up code
3. clean-up readme and create a simple bash script for starting
4. create video


Setup
1. brew install minikube
2. install docker
3. minikube start
4. switch docker env to minikube; `eval $(minikube docker-env)`
5. build docker image for svc `docker build -t network-scapper:latest -f app/Dockerfile .`
6. build image for job `docker build -t network-scapper-selenium-job:latest -f job/Dockerfile .`
7. apply deployment file `kubectl -n scrapper apply -f app/deployment-svc.yaml` 
8. start service tunnel `minikube service flask-gateway-server -n scrapper`
9. hit api and test


Connect to Mongo instance:
pre req - `brew install mongosh`

1. `ktemp port-forward service/mongo 27017:27017`
2. `mongosh -u admin -p password --authenticationDatabase admin`