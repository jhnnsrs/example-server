# Example-Server 

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/arkitektio/example-server/)
![Maintainer](https://img.shields.io/badge/maintainer-jhnnsrs-blue)

Example server implementation following the design principles of the [Arkitekt](https://arkitekt.live) framework. 

> [!NOTE]  
> This is an example server to demonstrate the patterns and practices used in Arkitekt servers. It is not intended for production use and is just a reference implementation. It additionality serves as a starting point for developers looking to build their own Arkitekt-based servers and as a central github repository to discuss server-related issues and improvements.


## Features

- Built with Django and Strawberry GraphQL
- Dockerized for easy deployment
- Template CI/CD workflows for automated builds and deployments
- Example models, queries, and mutations to get started quickly
- Fits the Arkitekt spec for multi-tenancy ("Organizations")
- Includes tests and linting configurations for code quality

## Getting Started

Cloning the repository and running the server locally:

```bash
git clone https://github.com/arkitektio/example-server.git
cd example-server
docker-compose up --build
```

This starts the server in a Docker container. You can access the GraphQL playground at `http://localhost:8000/graphql/`.



## Integration with Arkitekt

To test integrate with the Arkitekt framework, you can use the Arkitekt CLI to connect to the running server, run this projects on the same directory as your Arkitekt deployment:

```bash
arkitekt-server service connect --url http://localhost:8000 --identifier arkitekt.io.example-server 
```

This will register the service in the arkitekt platform and will allow you to request access to it in any
arkitekt application. 

## Accessing the authenticated inside the app

You can now access and register this requirement inside your Arkitekt applications.

```python
from arkitekt_next import easy
from arkitekt_next.service.builder import GraphQLServiceBuilder


app = easy("my-app")
app.require_service("example", service="arkitekt.io.example-server", optional=False, builder=GraphQLServiceBuilder)
# We require to have the example service available inside our app, and we use the GraphQLServiceBuilder to build the service (when publishing this, you best handle this in a dedicated client sdk module)


with app:

    service = app.get_service("example")
    response = service.query(
        """
        query {
            testModels {
                id
                name
            }
        }
        """
    )
    print(response.data)

```
### 


