#bin/sh
docker stop flaskdocker-ctn
docker container rm flaskdocker-ctn
docker image rm falskdocker-img 
docker build -t flaskdocker-img .
docker run -d -p 5000:5000 --name flaskdocker-ctn flaskdocker-img
docker exec -it falskdocker bash
