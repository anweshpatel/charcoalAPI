FROM arm32v6/python:3.6-alpine

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8080

ENV NAME usn

CMD ["python","app.py"]