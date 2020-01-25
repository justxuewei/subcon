#!/bin/sh

mv wsgi.conf /etc/nginx/conf.d
nginx -g "daemon on;" && uwsgi --ini /app/wsgi.ini
