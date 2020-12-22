FROM python:3.9-alpine

RUN \
    wget https://releases.hashicorp.com/consul/1.9.0/consul_1.9.0_linux_amd64.zip -O temp.zip \
    && unzip -d /usr/local/bin temp.zip \
    && rm temp.zip \
    && wget https://releases.hashicorp.com/consul-template/0.25.1/consul-template_0.25.1_linux_amd64.zip -O temp.zip \
    && unzip -d /usr/local/bin temp.zip \
    && rm temp.zip

RUN \
    apk update \
    && apk add bind-tools curl jq supervisor

RUN echo 'alias sc=supervisorctl' >> ~/.bash_profile

WORKDIR /var
COPY app ./

RUN \
    mkdir -p /consul/data \
    && mkdir -p /consul/config
COPY consul/config /consul/config
COPY supervisor /etc

# Application
EXPOSE 80

# Server RPC is used for communication between Consul clients and servers for internal
# request forwarding.
EXPOSE 8300

# Serf LAN and WAN (WAN is used only by Consul servers) are used for gossip between
# Consul agents. LAN is within the datacenter and WAN is between just the Consul
# servers in all datacenters.
EXPOSE 8301 8301/udp 8302 8302/udp

# HTTP and DNS (both TCP and UDP) are the primary interfaces that applications
# use to interact with Consul.
EXPOSE 8500 8600 8600/udp

RUN alias
CMD [ "supervisord" ]
