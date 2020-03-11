FROM python:3.7
LABEL maintainer="dev@cuenca.com"

# Install app
ADD Makefile requirements.txt /arcusd/
WORKDIR /arcusd
RUN make install

# Add project content to image
ADD . /arcusd/
RUN pip install -e .

CMD NEW_RELIC_LICENSE_KEY=$NEW_RELIC_LICENSE_KEY NEW_RELIC_APP_NAME=arcusd newrelic-admin run-program celery worker -A arcusd.daemon.tasks --loglevel=info -c ${ARCUSD_WORKERS:-5}
