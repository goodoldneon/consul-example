# Consul Example

## Background

This repo shows how Consul can be used without sidecar containers. It demonstrates:

- Resolution of human-readable hostnames (e.g. `backend-service.service.consul`) using Consul's DNS.
- mTLS using a Consul proxy.
- Authentication using Consul intentions.

## Instructions

This section will start 2 Python apps: backend and frontend services. We want the frontend service to access the backend service via a human-readable hostname: backend-service.service.consul. Take a look at `frontend-service/server.py` to that hostname's usage.

Start all the things:

```
$ docker-compose up -d --build
```

Prove the human-readable hostname works by running:

```
$ curl localhost:8080/hostname
```

Prove the proxy works by running:

```
$ curl localhost:8080/proxy
```

Browse to http://localhost:8500 to see Consul's UI. Alternatively, you can run commands inside a container, like this:

```
$ docker exec consul-server-1 consul members
Node             Address          Status  Type    Build  Protocol  DC   Segment
server-1         172.20.0.3:8301  alive   server  1.9.1  2         dc1  <all>
backend-client   172.20.0.2:8301  alive   client  1.9.0  2         dc1  <default>
frontend-client  172.20.0.4:8301  alive   client  1.9.0  2         dc1  <default>
```

In the UI, create an intention that blocks traffic from the frontend service to the backend service. Running the following should no longer have output:

```
$ curl localhost:8080/proxy
```

If you want to shell into a container, run something like this:

```
$ docker exec -it frontend-service sh
```

When in a container, you can see the processes managed by supervisord by running:

```
$ supervisorctl -c /etc/supervisor/supervisord.conf status
app                              RUNNING   pid 8, uptime 0:04:57
consul-agent                     RUNNING   pid 9, uptime 0:04:57
consul-connect                   RUNNING   pid 37, uptime 0:04:56
dnsmasq                          FATAL     Exited too quickly (process log may have details)
```

In the above output:

- `app` is the Python serv.
- `consul-agent` is the Consul agent.
- `consul-connect` is the Consul proxy.
- `dnsmasq` is a DNS used to forward `*.consul` hostnames to Consul's DNS. Without this, http://backend.service.consul wouldn't resolve.

Stop all the things:

```
$ docker-compose down
```
