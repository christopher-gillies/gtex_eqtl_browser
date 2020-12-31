FROM python:3.6-slim

RUN apt-get update
RUN apt-get install -y apt-utils build-essential
RUN apt-get install -y gcc

RUN apt-get update; apt-get -y install libopenblas-base liblapack3 vim samtools sqlite3

RUN pip install numpy pandas pyarrow pysam jupyterlab flask

EXPOSE 5000

CMD bash