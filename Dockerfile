FROM python:3.5.1-alpine 
MAINTAINER Chris Smith <chris87@gmail.com> 

RUN \
  pip install \
    python-etcd

COPY *.py /

VOLUME ["/letsencrypt"]
ENTRYPOINT ["python", "/generate.py"]
