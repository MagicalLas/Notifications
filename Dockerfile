FROM python:3.7

RUN pip install sanic

COPY . .

CMD [ "python", "main.py" ]