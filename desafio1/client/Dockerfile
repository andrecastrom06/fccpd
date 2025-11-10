FROM alpine:3.18
RUN apk add --no-cache curl
WORKDIR /app
COPY loop.sh /app/loop.sh
RUN chmod +x /app/loop.sh
CMD ["/app/loop.sh"]