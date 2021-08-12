FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
ENV FLASK_APP=flaskr
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN apk add gcc musl-dev linux-headers libffi-dev openssl-dev openssh
COPY . .
RUN pip install -r requirements.txt
