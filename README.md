# Trading Signal Controller: An Enterprise Solution for Managing Trading Signals

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
   - [Conventional Installation](#conventional-installation)
   - [Docker Setup](#docker-setup)
4. [Built With](#built-with)
5. [Project Structure](#project-structure)
6. [Core Features](#core-features)
   - [Balancer for Assignment](#balancer-for-assignment)
7. [How to Contribute](#how-to-contribute)
8. [Licensing](#licensing)

## Introduction

Trading Signal Controller is a professional-grade application for managing trading signals. Built on Django, the system aims to streamline the handling of trading signals across both development and production settings.

## Prerequisites

- **Python**: Version 3.11
- **Django**: Version 4.1.7
- **Database**: PostgreSQL

## Quick Start

### Conventional Installation

1. **Clone the Git Repo**
    ```bash
    git clone <repository_link>
    ```
2. **Install Dependencies**
    ```bash
    poetry install
    ```
3. **Migrate the Database**
    ```bash
    poetry run python manage.py migrate
    ```
4. **Start the Dev Server**
    ```bash
    poetry run python manage.py runserver
    ```

### Docker Setup

Navigate to the root folder of the project:

1. **Create Docker Image**
    ```bash
    docker build -t trading_signal_controller .
    ```
2. **Initiate Docker Container**
    ```bash
    docker run -p 8000:8000 trading_signal_controller
    ```

## Built With

- **Web Framework**: Django
- **RESTful API**: Django REST Framework

## Project Structure

- **`pyproject.toml`**: Manages package metadata and dependencies.
- **`Dockerfile`**: Sets up the Python runtime, handles dependencies, and starts the app with Gunicorn.
- **`nginx.conf`**: Configures Nginx as a reverse proxy and serves static files.
- **`docker-compose.yaml`**: Manages multi-container Docker applications.
- **`wsgi.py` & `asgi.py`**: Set up WSGI and ASGI servers for deployment.
- **`models.py`**: Houses data models like `MasterTrader`.

## Core Features

### Balancer for Assignment

#### Introduction

The function `balance_runner_assignment` in `src/api/models.py` balances the allocation of `MasterTrader` instances across active `CrawlRunner` instances to prevent any one from being overloaded.

#### Implementation Steps

1. **Fetch Active Instances**: Enumerates all active `CrawlRunner` and `MasterTrader` instances.
2. **Calculate Metrics**: Finds total and average `MasterTrader` instances for each `CrawlRunner`.
3. **Early Exit Check**: Exits the function if no active instances are found.
4. **Average Computation**: Evaluates the average `MasterTrader` instances for each `CrawlRunner`.
5. **Identify Pending Assignments**: Determines any remaining `MasterTrader` instances that need to be assigned.

## How to Contribute

For a detailed guide on contributing to this project, please see [CONTRIBUTING.md](CONTRIBUTING.md).

## Licensing

The software is distributed under the MIT License. For additional details, refer to [LICENSE.md](LICENSE.md).
