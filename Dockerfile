FROM alpine:latest

RUN adduser -D -h /srv goserver

COPY goserver /srv/goserver

USER goserver

CMD ["/srv/goserver"]
