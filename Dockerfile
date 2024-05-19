# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app inside the container
WORKDIR /app

# Copy the app directory contents into the container at /app
COPY ./app /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable
ENV NAME World

# Command to run the app
CMD ["streamlit", "run", "app.py"]
