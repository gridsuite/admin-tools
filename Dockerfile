FROM python:3.8.12-alpine

RUN adduser -D powsybl
USER powsybl
WORKDIR /home/powsybl
COPY scripts/ ./

RUN apk add --no-cache curl jq && pip3 install -r requirements.txt
