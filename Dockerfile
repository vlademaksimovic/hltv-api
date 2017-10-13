FROM gliderlabs/alpine:3.6
MAINTAINER Simon Egersand "s.egersand@gmail.com"

RUN apk add --update --no-cache \
    bash \
    py-pip \
    python3 \
    python2-dev \
    python3-dev \
    build-base \
    linux-headers \
    curl

# TODO: Just add what's necessary, also do this:
# ADD ./requirements.txt /tmp/requirements.txt
# RUN pip install --no-cache-dir -q -r /tmp/requirements.txt

# TODO: Set workdir
# WORKDIR /opt/webapp

ADD . /

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

# Expose is not supported by Heroku
# EXPOSE 8000

# TODO: Look into this
# Run the image as a non-root user
# RUN adduser -D myuser
# USER myuser

# $PORT is set by Heroku
CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT app:app
