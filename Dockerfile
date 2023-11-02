FROM python:3.11.6-slim-bullseye
RUN apt update -y && apt install -y ffmpeg aria2
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . /app
CMD ["python3","run.py"]