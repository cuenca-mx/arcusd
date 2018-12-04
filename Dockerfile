FROM python:3.7
LABEL maintainer="dev@cuenca.com"

# Install app
ADD Makefile requirements.txt /arcusd/
WORKDIR /arcusd
RUN make install

# Add project content to image
ADD . /arcusd/