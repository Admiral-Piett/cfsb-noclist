FROM python:3.9.1-alpine

WORKDIR /opt/svc

COPY src/ ./
COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
