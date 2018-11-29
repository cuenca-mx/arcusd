FROM python:3.6
LABEL maintainer="dev@cuenca.com"

ADD Makefile requirements.txt /arcusd/
WORKDIR /arcusd

RUN pip install --quiet --upgrade pip
RUN make install

