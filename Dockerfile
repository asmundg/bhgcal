FROM ubuntu:trusty
RUN apt-get update
RUN apt-get install --yes --no-install-recommends \
    python-pip
ADD . /src
RUN pip install -r /src/requirements.txt
RUN (cd /src && python setup.py develop)

ENTRYPOINT ["bhgcal"]
