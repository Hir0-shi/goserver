FROM alpine:latest
ENV PORT=8991

RUN adduser -D -h /srv goserver

COPY goserver /srv/goserver

USER goserver

CMD ["/srv/goserver"]
