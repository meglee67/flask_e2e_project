# this is copied from https://github.com/hantswilliams/HHA_504_2023/blob/main/WK8/code/docker_example_1/Dockerfile

FROM python:3.7-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the content of the local src directory to the working directory
COPY . /app

# Update the system and install git
RUN apk update && apk add git

# Upgrade pip
RUN pip install --upgrade pip

# Install the dependencies
RUN pip install -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Command to run the application
CMD ["python", "flask10.py"]



# for line 8 you have to change the "flask10.py" to whatever file you're running when you run to launch a site page

# Docker build command: docker build -t docker_example_1 .
# Docker run command: docker run -d -p 5001:5000 docker_example_1