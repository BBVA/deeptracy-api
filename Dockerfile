FROM python:3.6

RUN mkdir /tmp/install
RUN mkdir /opt/deeptracy

WORKDIR /tmp/install

# add dependencies
ADD requirements* /tmp/install/
RUN pip install -r /tmp/install/requirements.txt
RUN rm -rf /tmp/install

# add sources
ADD deeptracy_api /opt/deeptracy/deeptracy_api

# add run script
ADD wait-for-it.sh /opt/deeptracy
ADD run.sh /opt/deeptracy
RUN chmod +x /opt/deeptracy/run.sh

WORKDIR /opt/deeptracy
CMD ["/opt/deeptracy/run.sh"]
