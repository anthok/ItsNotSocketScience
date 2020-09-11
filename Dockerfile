FROM ubuntu:18.04
RUN apt-get update -y && apt-get upgrade -y && apt-get install python3 -y
RUN mkdir /opt/socketscience/
WORKDIR /opt/socketscience/
COPY . /opt/socketscience/
ENTRYPOINT ["python3", "app.py", "-c", "cfg.json"]
