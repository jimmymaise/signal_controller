# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.2.2  \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/code" \
    VENV_PATH="/code/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Set the working directory to /app
WORKDIR  /src

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential


# Copy the dependencies file to the working directory
COPY pyproject.toml poetry.lock /src/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -


# Install the app dependencies with Poetry
RUN poetry install

# Copy the rest of the app code to the working directory
COPY ./src ./

# Expose port 8000 for the app
EXPOSE 8000

# Set environment variables for Django
ENV PYTHONUNBUFFERED=1
ENV DJANGO_ENVIRONMENT=production



# Collect static files
RUN poetry run python manage.py collectstatic --no-input

RUN echo $VIRTUAL_ENV


# Set the default command to run the app with Gunicorn
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]