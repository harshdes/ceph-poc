# Pre-requisites
* [Docker](https://www.docker.com/products/overview#/install_the_platform)
* [JDK 8](http://www.oracle.com/technetwork/java/index.html)

# Installing

The spring boot application is packaged inside a docker container. 
To build and run the container:
```sh
./build.sh
```

The output of the build script will contain the location/URL of the application.
This is typically `http://<docker-machine-ip` ( For e.g http://192.168.99.100 )

### Swagger

To browse and invoke the REST endpoints, go to the `<application_url>/swagger-ui.html`
