FROM consul

COPY consul/config /consul/config

EXPOSE 8500 8600/udp

CMD [ "consul", "agent", "-server", "-ui", "-node", "server-1", "-bootstrap-expect", "1", "-client", "0.0.0.0", "-data-dir", "/consul/data", "-config-dir", "/consul/config"]
