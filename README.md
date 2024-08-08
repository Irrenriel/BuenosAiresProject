# Delivery Service

Microservice for International Delivery Service.

## How to use:

1. Clone repository.
2. Install Docker & Docker Compose.
3. Run `docker-compose up` inside repository.
4. Server will be run on: `http://localhost:8080/`

## Entrypoints:
* `http://localhost:8080/docs` - documentation, all available entrypoints will be here
* `http://localhost:8080/packages` - get all available packages
* `http://localhost:8080/packages/types` - get all package types
* `http://localhost:8080/packages/create` - create package
* `http://localhost:8080/package/{package_id}` - get package by package_id
* `http://localhost:8080/exchange_rate/update` - manually update exchange rate