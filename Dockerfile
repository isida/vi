FROM python:2-alpine

COPY . /isida
WORKDIR /isida

RUN pip2 install -r requirements.txt

CMD ["python2", "./isida.py"]
