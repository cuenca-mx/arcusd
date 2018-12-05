FROM python:3.6
LABEL maintainer="dev@cuenca.com"

# Install app
ADD Makefile requirements.txt /arcusd/
WORKDIR /arcusd
RUN pip install --quiet --upgrade pip
RUN make install

# Add project content to image
ADD . /arcusd/

#
#ENTRYPOINT ['celery', '-A', 'tasks', '--loglevel=info']

CMD celery worker -A arcusd.daemon.tasks --loglevel=info

## Start celery
#COPY arcusd/daemon/config/celeryd-daemon /etc/init.d/celeryd
#COPY arcusd/daemon/config/celeryd-conf /etc/default/celeryd
#RUN mkdir -p /etc/default
#RUN chmod +x /etc/init.d/celeryd
#RUN chmod -R a+rw /arcusd
#RUN adduser celery --disabled-password
#RUN mkdir -p /var/log/celery/ && chown celery:celery /var/log/celery/
#RUN mkdir -p /var/run/celery/ && chown celery:celery /var/run/celery/
#RUN pip install --quiet celery

#CMD chmod -R a+rxw /etc/hosts && /etc/init.d/celeryd start