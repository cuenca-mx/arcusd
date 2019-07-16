FROM cuenca/python:latest
LABEL maintainer="dev@cuenca.com"

# Install app
ADD Makefile requirements.txt /arcusd/
WORKDIR /arcusd
RUN make install

# Add project content to image
ADD . /arcusd/
RUN pip install -e .

CMD celery worker -A arcusd.daemon.tasks --loglevel=info -c ${ARCUSD_WORKERS:-0}
