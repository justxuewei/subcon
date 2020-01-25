FROM alpine:3.8

WORKDIR /app

COPY entrypoint.sh requirements.txt app.py wsgi.py wsgi.ini wsgi.conf ./

RUN apk add python3 nginx uwsgi uwsgi-python3 && \
    pip3 install -r requirements.txt && \
    mkdir -p /run/nginx

EXPOSE 8080

ENTRYPOINT ["./entrypoint.sh"]

