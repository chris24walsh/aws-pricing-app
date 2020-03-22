FROM python:latest

WORKDIR /usr/app
COPY * ./
RUN pip install -r requirements.txt

EXPOSE 8000
CMD python api-server.py
