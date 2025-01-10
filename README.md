# Project Name




## Overview

This project is a simple chat assistant and web search tool designed to run using Docker Compose, with a Makefile to simplify common tasks. Below are instructions on how to set up, run, and manage the application.

## Prerequisites

- Docker: Ensure Docker is installed on your machine. You can download it from [here](https://www.docker.com/products/docker-desktop).
- Docker Compose: This is typically included with Docker Desktop, but you can verify its installation by running `docker-compose --version`.

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/JosefButts/SampleChatAssistant.git
  
   ```

2. **Environment Variables**

   Copy the `.env.example` to `.env` and fill in the necessary environment variables.

   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file to include your API keys and other configuration settings.

## LangChain Setup and Tracing

The project uses LangChain for AI capabilities and includes tracing functionality for debugging and monitoring. Configure the following environment variables in your `.env` file:

1. **LangChain Configuration**
   ```bash
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
   LANGCHAIN_API_KEY=<your_langchain_api_key>
   LANGCHAIN_PROJECT=<your_project_name>
   LANGCHAIN_VERBOSE=true
   LANGCHAIN_TRACING=true
   ```

These settings enable:
- Tracing of all LangChain operations
- Integration with LangSmith for visualization and debugging
- Verbose logging for development purposes

Visit the [LangSmith dashboard](https://smith.langchain.com) to view traces and debug your application.

## Running the Application


### Using Docker Compose

1. **Start Services**

   To start all services in detached mode (production):

   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

   For development mode with logs:

   ```bash
   docker-compose -f docker-compose.dev.yml up
   ```

2. **Stop Services**

   To stop and remove all services:

   ```bash
   docker-compose down
   ```

   For development mode:

   ```bash
   docker-compose -f docker-compose.dev.yml down
   ```

3. **Build Images**

   To build the Docker images:

   ```bash
   docker-compose build
   ```

   For development mode:

   ```bash
   docker-compose -f docker-compose.dev.yml build
   ```

4. **Run Tests**

   To run tests:

   ```bash
   docker-compose -f docker-compose.dev.yml exec backend pytest
   ```

### Using the Makefile

1. **Start Services**

   To start all services in detached mode (production):

   ```bash
   make up
   ```

   For development mode with logs:

   ```bash
   make up-dev
   ```

2. **Stop Services**

   To stop and remove all services:

   ```bash
   make down
   ```

3. **Build Images**

   To build the Docker images:

   ```bash
   make build
   ```

   For development mode:

   ```bash
   make build-dev
   ```

4. **Run Tests**

   To run tests:

   ```bash
   make test
   ```

5. **Help**

   To see a list of available commands:

   ```bash
   make help
   ```

## Additional Information

- Ensure that your Docker daemon is running before executing any Docker or Makefile commands.
- If `make` is not available on your system, you can directly use the equivalent `docker-compose` commands listed in the "Using Docker Compose" section above.
- For any issues or contributions, please refer to the project's issue tracker or contact the maintainers. 