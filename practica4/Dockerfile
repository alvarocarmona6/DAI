FROM python:2.7

RUN mkdir -p /home/project/practica4
WORKDIR /home/project/practica4
COPY requirements.txt /home/project/practica4
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/project/practica3
