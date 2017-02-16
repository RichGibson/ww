FROM python:2.7
 RUN apt-get update && apt-get install -y \
        python-dev python-pip python-setuptools \
        libffi-dev libxml2-dev libxslt1-dev \
        liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install -r requirements.txt
 #RUN pop install Pillow
 ADD . /code/
