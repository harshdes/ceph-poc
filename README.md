# Pre-requisites
* [Docker](https://www.docker.com/products/overview#/install_the_platform)
* [JDK 8](http://www.oracle.com/technetwork/java/index.html)

# Installing

The spring boot application is packaged inside a docker container. 
To build and run the container:
```sh
./build.sh
```
The script will

* Compile & package the java application into a jar
* Create a docker container with all dependencies including the above created application
* Starts the docker container which internally
 * Starts cassandra daemon and initializes the database
 * Starts the java web application

The output of the build script will contain the location/URL of the application.
This is typically `http://<docker-machine-ip` ( For e.g http://192.168.99.100 )

### Swagger

To browse and invoke the REST endpoints, go to the `<application_url>/swagger-ui.html` ( For e.g http://192.168.99.100/swagger-ui.html )

# Technologies

* [**Cassandra**](http://cassandra.apache.org/) for clustered database
* [**Spring Boot**](https://projects.spring.io/spring-boot/) for web framework
 * [**spring-data-cassandra**](http://projects.spring.io/spring-data-cassandra/) to interface with cassandra
 * [**spring-statemachine**](https://projects.spring.io/spring-statemachine/) to describe and execute statemachine-based tasks
* [**Docker**](https://www.docker.com/) for containerizing the application