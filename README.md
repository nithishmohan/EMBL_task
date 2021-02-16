# EMBL_task
#EMBL CRUD API


How To start the API service using docker-compose
---------------
Run the following commands 
1. docker-compose up

The service will start to listen on port <b>80</b> inside the Docker machine

Testing
-------

1. Login to the `embl` docker container (`docker exec -it app_server /bin/bash`)
2. Run the command `pytest`


Making Requests
---------------

Please go to `http://localhost:80/docs` to find more about the API documentation. 
