#FROM alpine:3.6
FROM gliderlabs/alpine:3.6

MAINTAINER Simon Egersand "s.egersand@gmail.com"

RUN apk add --update --no-cache \
    py-pip \
    python3 \
    python2-dev \
    python3-dev \
    build-base \
    linux-headers \
    curl

ADD . /

RUN pip3 install --upgrade pip

RUN pip3 install uwsgi
RUN pip3 install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["uwsgi", "--http", "0.0.0.0:8000", "--module", "app:app", "--processes", "1", "--threads", "8"]
