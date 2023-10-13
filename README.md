# Signal Controller: Trading Signal Management System

## Table of Contents

1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Getting Started](#getting-started)
   - [Standard Installation](#standard-installation)
   - [Docker Deployment](#docker-deployment)
4. [Technologies](#technologies)
5. [Codebase Summary](#codebase-summary)
6. [Key Functionalities](#key-functionalities)
   - [Crawl Assignment](#crawl-assignment)
7. [Contribution Guidelines](#contribution-guidelines)
8. [License](#license)

## Overview

Signal Controller is an enterprise-level trading signal management application. Developed on the Django framework, this system is designed to facilitate the effective management and control of trading signals in both development and testing environments.

## Requirements

- **Python**: v3.11
- **Django**: v4.1.7
- **Database**: PostgreSQL

## Getting Started

### Standard Installation

1. **Clone the Repository**
    ```bash
    git clone <repository_url>
    ```
2. **Install Required Packages**
    ```bash
    poetry install
    ```
3. **Database Migration**
    ```bash
    poetry run python manage.py migrate
    ```
4. **Launch Development Server**
    ```bash
    poetry run python manage.py runserver
    ```

### Docker Deployment

Navigate to the project's root directory:

1. **Build Docker Image**
    ```bash
    docker build -t signal_controller .
    ```
2. **Run Docker Container**
    ```bash
    docker run -p 8000:8000 signal_controller
    ```

## Technologies

- **Framework**: Django
- **API Toolkit**: Django REST Framework

## Codebase Summary

- **`pyproject.toml`**: Manages project metadata and dependencies, specifying Python version, Django, Django REST Framework, and other essential libraries.
- **`Dockerfile`**: Configures the Python environment, manages dependencies, and initiates the application using Gunicorn.
- **`nginx.conf`**: Establishes an Nginx reverse proxy and serves static and media files.
- **`docker-compose.yaml`**: Orchestrates a multi-container Docker application, managing database, web server, and Nginx instances.
- **`wsgi.py` & `asgi.py`**: Configure WSGI and ASGI servers for deployment.
- **`models.py`**: Defines data models, including the `MasterTrader` entity.

## Key Functionalities

### Crawl Assignment

#### Overview

The `balance_runner_assignment` function in `src/api/models.py` is responsible for balancing the distribution of `MasterTrader` instances among active `CrawlRunner` instances. This ensures that no single `CrawlRunner` is overwhelmed with too many `MasterTrader` instances.

#### Algorithm

The algorithm follows these steps:

1. **Retrieve Active Instances**: Lists all active `CrawlRunner` and `MasterTrader` instances.
2. **Calculate Instance Metrics**: Computes the total and average number of `MasterTrader` instances per `CrawlRunner`.
3. **Perform Early Exit Check**: If there are no active instances, the function exits early.
4. **Compute Averages**: Calculates the average number of `MasterTrader` instances per `CrawlRunner`.
5. **Determine Remaining Assignments**: Finds out how many more `MasterTrader` instances need to be allocated.


# Contribution Guidelines

For guidelines on how to contribute to this project, please refer to [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This software is licensed under the MIT License. For more information, see [LICENSE.md](LICENSE.md).
