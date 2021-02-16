# EMBL_task
#EMBL CRUD API


This is a simple Python/FastAPI application intended to provide a working example of searching EMBL database <b>ensembl_website_97</b>. 


How To start the API service using docker-compose
---------------
Run the following commands 
1. docker-compose up

The service will start to listen on port <b>80</b> inside the Docker machine

Testing
-------

1. Login to the `embl` docker container 
2. Run the command `pytest`


Making Requests
---------------

Please go to `http://localhost:80/docs` to find more about the API documentation. 

Todo
---------------
 Since its a simple REST API. I have not included GraphQL. 
