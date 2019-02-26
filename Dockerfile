FROM python:3.6
LABEL maintainer="dev@cuenca.com"

# Install latest security updates
RUN SECURITY_LIST=$(mktemp) \
 && grep security /etc/apt/sources.list > "$SECURITY_LIST" \
 && apt-get -o "Dir::Etc::SourceList=${SECURITY_LIST}" -o Acquire::http::AllowRedirect=false update \
 && apt-get -o "Dir::Etc::SourceList=${SECURITY_LIST}" -o Acquire::http::AllowRedirect=false upgrade -y \
 && rm -rf /var/lib/apt/lists/* \
 && rm "$SECURITY_LIST"

# Install app
ADD Makefile requirements.txt /arcusd/
WORKDIR /arcusd
RUN make install

# Add project content to image
ADD . /arcusd/

CMD celery worker -A arcusd.daemon.tasks --loglevel=info -c ${ARCUSD_WORKERS:-0}
