# Use the official Python 3.10.13 Alpine image as the base image
FROM python:3.10.13-alpine

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements.txt file from the local directory to the container
COPY requirements.txt ./

# Install the Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Copy the entire local directory contents to the working directory in the container
COPY . .

# Specify the command to run the application when the container starts
CMD [ "python", "./main.py" ]
