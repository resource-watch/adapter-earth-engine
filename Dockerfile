FROM python:3.6-alpine
MAINTAINER Vizzuality info@vizzuality.com

ENV NAME adapterearthengine
ENV USER adapterearthengine

RUN apk update && apk upgrade && \
   apk add --no-cache --update bash git openssl-dev build-base alpine-sdk \
   libffi-dev gcc python3-dev musl-dev

RUN addgroup $USER && adduser -s /bin/bash -D -G $USER $USER

RUN easy_install pip && pip install --upgrade pip
RUN pip install virtualenv gunicorn gevent --use-feature=2020-resolver

RUN mkdir -p /opt/$NAME
RUN cd /opt/$NAME && virtualenv venv && source venv/bin/activate
COPY tox.ini /opt/$NAME/tox.ini
COPY requirements.txt /opt/$NAME/requirements.txt
COPY requirements_dev.txt /opt/$NAME/requirements_dev.txt
RUN cd /opt/$NAME && pip install -r requirements.txt --use-feature=2020-resolver
RUN cd /opt/$NAME && pip install -r requirements_dev.txt --use-feature=2020-resolver

COPY entrypoint.sh /opt/$NAME/entrypoint.sh
COPY main.py /opt/$NAME/main.py
COPY gunicorn.py /opt/$NAME/gunicorn.py

# Copy the application folder inside the container
WORKDIR /opt/$NAME

COPY ./adapterearthengine /opt/$NAME/adapterearthengine
COPY ./microservice /opt/$NAME/microservice
COPY tests /opt/$NAME/tests
RUN chown -R $USER:$USER /opt/$NAME

# Tell Docker we are going to use this ports
EXPOSE 5700
USER $USER

# Launch script
ENTRYPOINT ["./entrypoint.sh"]
