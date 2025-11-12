FROM alpine:3.18
RUN apk add --no-cache curl
WORKDIR /app
COPY loop.sh .
CMD ["./loop.sh"]