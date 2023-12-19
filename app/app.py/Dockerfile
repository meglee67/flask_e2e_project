# this is copied from https://github.com/hantswilliams/HHA_504_2023/blob/main/WK8/code/docker_example_1/Dockerfile

FROM python:3.7-alpine
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "flask8.py"]

# Docker build command: docker build -t docker_example_1 .
# Docker run command: docker run -d -p 5001:5000 docker_example_1