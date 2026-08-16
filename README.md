# goserver

A simple Go HTTP server that serves an HTML page, designed to run in Docker.

## Related Projects

| Branch     | Project                           | Description                                                    |
|------------|-----------------------------------|----------------------------------------------------------------|
| `main`     | `goserver`                        | This Go HTTP server                                            |
| `pyserver` | [`pyserver/`](pyserver/README.md) | Python script that analyzes character/word frequency in a book |

## Requirements

- Go 1.26+
- Docker

## Configuration

The server port is configurable via the `PORT` environment variable.

## Running Locally

```bash
export PORT="8999"
go build
./goserver
```

Expected output:

```
server started on 8999
```

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

The Dockerfile uses Alpine Linux, sets the port via `ENV`, and runs as a non-root user:

```dockerfile
FROM alpine:latest
ENV PORT=8991

RUN adduser -D -h /srv goserver

COPY goserver /srv/goserver

USER goserver

CMD ["/srv/goserver"]
```

`ENV PORT=8991` sets the port inside the container. Running as a non-root user is a security best practice — it limits the impact if the container is compromised.

### Building and Running

```bash
docker build . -t goserver:latest
docker run -p 8991:8991 goserver
```

Expected output:

```
server started on 8991
```

### Testing

```bash
curl localhost:8991
```

Expected response:

```html
<html>
<head></head>
<body>
	<p> Hello from Docker! I'm a Go server. </p>
</body>
</html>
```

## Full Workflow

### Local run

```bash
$ export PORT="8999"
$ go build
$ ./goserver
server started on 8999

$ curl localhost:8999
<html>
<head></head>
<body>
	<p> Hello from Docker! I'm a Go server. </p>
</body>
</html>
```

### Docker run

```bash
$ CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build
$ docker build . -t goserver:latest
[+] Building 1.5s (8/8) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 172B
 => [internal] load metadata for docker.io/library/alpine:latest
 => [internal] load .dockerignore
 => => transferring context: 2B
 => CACHED [1/3] FROM docker.io/library/alpine:latest@sha256:28bd5fe8b56d
 => [internal] load build context
 => => transferring context: 8.57MB
 => [2/3] RUN adduser -D -h /srv goserver
 => [3/3] COPY goserver /srv/goserver
 => exporting to image
 => => exporting layers
 => => exporting manifest sha256:1881eca3ac6a
 => => exporting config sha256:96e13639ecc2
 => => naming to docker.io/library/goserver:latest

$ docker run -p 8991:8991 goserver
server started on 8991

$ curl localhost:8991
<html>
<head></head>
<body>
	<p> Hello from Docker! I'm a Go server. </p>
</body>
</html>
```

### Verify non-root user

```bash
$ docker exec -it <container_id> sh
/ $ id
uid=1000(goserver) gid=1000(goserver) groups=1000(goserver)
```
