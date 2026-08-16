# goserver

A simple Go HTTP server that serves an HTML page, designed to run in Docker.

## Requirements

- Go 1.26+
- Docker

## Running Locally

```bash
go build
./goserver
```

The server starts on port `8010`.

## Endpoints

| Method | Path | Description          |
|--------|------|----------------------|
| GET    | /    | Returns an HTML page |

## Docker

### Building the Binary

Build a statically linked binary for Linux:

```bash
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build
```

`CGO_ENABLED=0` is required for Alpine compatibility.

### Dockerfile

The Dockerfile uses Alpine Linux and runs as a non-root user:

```dockerfile
FROM alpine:latest

RUN adduser -D -h /srv goserver

COPY goserver /srv/goserver

USER goserver

CMD ["/srv/goserver"]
```

Running as a non-root user is a security best practice — it limits the impact if the container is compromised.

### Building and Running

```bash
docker build . -t goserver:latest
docker run -p 8010:8010 goserver
```

### Testing

```bash
curl localhost:8010
```

## Verification

Confirm the server is running inside a container:

```bash
$ docker ps
CONTAINER ID   IMAGE       COMMAND           PORTS                   STATUS       NAMES
60d56208be78   goserver    "/srv/goserver"   0.0.0.0:8010->8010/tcp   Up 2 minutes   hopeful_mclaren
```

Confirm the process runs as a non-root user:

```bash
$ docker exec -it 60d56208be78 sh
/ $ id
uid=1000(goserver) gid=1000(goserver) groups=1000(goserver)
```

Confirm the endpoint responds correctly:

```bash
$ curl localhost:8010
<html>
<head></head>
<body>
	<p> Hello from Docker! I'm a Go server. </p>
</body>
</html>
```
