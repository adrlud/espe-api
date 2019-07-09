FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /tmp/app
WORKDIR /tmp/app
COPY app/requirements.txt /tmp/app
RUN pip install -r requirements.txt
COPY app /tmp/app
