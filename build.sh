#bin/sh
docker stop pythonblog [containerid]
docker container rm pythonblog
docker image rm pythonblog 
docker build -t pythonblog .
docker run -d -p 5000:5000 --name pythonblog pythonblog
docker exec -it pythonblog bash
