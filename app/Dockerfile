FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN python3 -m pip install -r requirements.txt

WORKDIR /
CMD [ "gunicorn", "-b", "0.0.0.0:5000" , "app:app" ]