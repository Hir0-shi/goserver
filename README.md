# goserver

A simple Go HTTP server that serves an HTML page.

## Requirements

- Go 1.26+

## Usage

```bash
go mod tidy
go build
./goserver
```

The server starts on port `8010`.

## Endpoints

| Method | Path | Description          |
|--------|------|----------------------|
| GET    | /    | Returns an HTML page |

## Example

```bash
curl localhost:8010
```
