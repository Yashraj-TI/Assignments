# Assignments
## Commands used to link and run 2 Containers
```
docker-compose up -d
docker run --name redis_test -p 6379:6379 -d redis 
docker ps
docker run --link redis_test:redis flask_project_web
```
 
