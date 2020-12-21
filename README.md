# Consul Example

## Background

This repo shows how Consul can be used without sidecar containers. It demonstrates:

- Easy service discovery, using Consul DNS or a Consul proxy.
- mTLS using a Consul proxy.
- Authentication using Consul intentions.

## Instructions

This section will start 2 Python apps: backend and frontend services. We want the frontend service to access the backend service via `localhost`.

Start all the things:

```
$ docker-compose up -d --build
```

Browse to http://localhost:8500 to see Consul's UI. Alternatively, you can run commands inside a container, like this:

```
$ docker exec consul-server-1 consul members
Node             Address          Status  Type    Build  Protocol  DC   Segment
server-1         172.20.0.3:8301  alive   server  1.9.1  2         dc1  <all>
backend-client   172.20.0.2:8301  alive   client  1.9.0  2         dc1  <default>
frontend-client  172.20.0.4:8301  alive   client  1.9.0  2         dc1  <default>
```

Prove the frontend service can communicate with the backend service via `localhost` by running:

```
$ curl localhost:8080
The backend says: "b'Hello from the backend'"%
```

Consul's DNS can resolve human-readable hostnames. See this by running the following command. In this example, the backend service's IP address is `192.168.160.3`:

```
$ docker exec frontend-service dig @localhost -p 8600 backend-service.service.consul

; <<>> DiG 9.16.6 <<>> @localhost -p 8600 backend-service.service.consul
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 64218
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;backend-service.service.consul.	IN	A

;; ANSWER SECTION:
backend-service.service.consul.	0 IN	A	192.168.160.3

;; Query time: 4 msec
;; SERVER: 127.0.0.1#8600(127.0.0.1)
;; WHEN: Mon Dec 21 15:09:49 UTC 2020
;; MSG SIZE  rcvd: 75
```

In Consul's UI, create an intention that blocks traffic from the frontend service to the backend service. Running the following should no longer have output:

```
$ curl localhost:8080
```

If you want to shell into a container, run something like this:

```
$ docker exec -it frontend-service sh
```

When in a container, you can see the processes managed by supervisord by running:

```
$ supervisorctl status
app                              RUNNING   pid 8, uptime 0:00:55
consul-agent                     RUNNING   pid 9, uptime 0:00:55
consul-connect                   RUNNING   pid 32, uptime 0:00:54
```

In the above output:

- `app` is the Python serv.
- `consul-agent` is the Consul agent.
- `consul-connect` is the Consul proxy.

Stop all the things:

```
$ docker-compose down
```
