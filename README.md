## Instructions

This section will start 2 Python apps: backend and frontend services. We want the frontend service to access the backend service via a human-readable hostname: http://backend.service.consul. Take a look at `frontend-service/server.py` to that hostname's usage.

Start all the things:

```
$ docker-compose up -d
```

Prove the human-readable hostname works by running:

```
$ curl localhost:9200
```

Browse to http://localhost:8500 to see Consul's UI. Alternatively, you can run commands inside a container, like this:

```
$ docker exec consul-server-1 consul members
Node             Address          Status  Type    Build  Protocol  DC   Segment
server-1         172.20.0.3:8301  alive   server  1.9.1  2         dc1  <all>
backend-client   172.20.0.2:8301  alive   client  1.9.0  2         dc1  <default>
frontend-client  172.20.0.4:8301  alive   client  1.9.0  2         dc1  <default>
```

Stop all the things:

```
$ docker-compose down
```
