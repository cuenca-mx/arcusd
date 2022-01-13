FROM python:3.8
LABEL maintainer="dev@cuenca.com"

# Install app
ADD Makefile requirements.txt /arcusd/
WORKDIR /arcusd
RUN apt-get update -y
RUN pip install -q --upgrade pip
RUN make install

# Add project content to image
ADD . /arcusd/
RUN pip install -e .

CMD newrelic-admin run-program celery worker -A arcusd.daemon.tasks --loglevel=info -c ${ARCUSD_WORKERS:-5}
