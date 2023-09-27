FROM python:3.7-alpine3.9
ARG CACHEBUST=1

RUN apk update \
        && apk add --no-cache \
        bash
WORKDIR /home/httpd/qa

RUN mkdir -p /home/httpd/qa

COPY src/ /home/httpd/qa/src
COPY tests/ /home/httpd/qa/tests
ADD requirements.txt /home/httpd/qa/requirements.txt
ADD run_tests.sh /home/httpd/qa/run_tests.sh


RUN pip install -r requirements.txt

CMD bash run_tests.sh