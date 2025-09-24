# Extend the Spark Python template:
    FROM bde2020/spark-python-template:3.3.0-hadoop3.3

    # Your name / email
    MAINTAINER Ilya iatashdowda@gmail.com
    
    # Copy your application's code into /app
    COPY . /app
    
    # Install your dependencies:
    # The template image automatically runs "pip install -r /app/requirements.txt"
    # if you haven't overridden the CMD, but if you need to customize, you can:
    # RUN pip install -r /app/requirements.txt
    
    # Set environment variables for the script to run
    ENV SPARK_APPLICATION_PYTHON_LOCATION=/app/FederatedAveraging.py
    