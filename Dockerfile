FROM python:3-alpine

COPY . /isida
WORKDIR /isida

RUN pip3 install -r requirements.txt

CMD ["python3", "./isida.py"]
