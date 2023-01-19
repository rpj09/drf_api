

FROM python:3.10.6-slim-buster

RUN pip3 install --upgrade pip

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

COPY entrypoint.sh .

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]