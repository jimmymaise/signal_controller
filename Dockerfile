# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR  /src

# Copy the dependencies file to the working directory
COPY pyproject.toml poetry.lock /src/

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# Install the app dependencies with Poetry
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the app code to the working directory
COPY . .

# Expose port 8000 for the app
EXPOSE 8000

# Set environment variables for Django
ENV PYTHONUNBUFFERED=1
ENV DJANGO_ENVIRONMENT=production

# Collect static files
RUN poetry run python manage.py collectstatic --no-input

# Set the default command to run the app with Gunicorn
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]