FROM python:3.11-bullseye
MAINTAINER Vizzuality info@vizzuality.com

ENV NAME adapterearthengine
ENV USER adapterearthengine

RUN apt-get -y update && apt-get -y upgrade && \
   apt-get install -y bash git openssl \
   libffi-dev gcc musl-dev libgeos-dev python3-pip python3-dev

RUN addgroup $USER && adduser --shell /bin/bash --disabled-login --ingroup $USER $USER

RUN pip install --upgrade pip
RUN pip install virtualenv gunicorn gevent

RUN mkdir -p /opt/$NAME
WORKDIR /opt/$NAME

COPY requirements.txt /opt/$NAME/requirements.txt
COPY requirements_dev.txt /opt/$NAME/requirements_dev.txt
RUN pip install -r requirements.txt
RUN pip install -r requirements_dev.txt

COPY entrypoint.sh /opt/$NAME/entrypoint.sh
COPY main.py /opt/$NAME/main.py
COPY gunicorn.py /opt/$NAME/gunicorn.py

# Copy the application folder inside the container

COPY ./adapterearthengine /opt/$NAME/adapterearthengine
COPY tests /opt/$NAME/tests
RUN chown -R $USER:$USER /opt/$NAME

# Tell Docker we are going to use this ports
EXPOSE 5700
USER $USER

# Launch script
ENTRYPOINT ["./entrypoint.sh"]
