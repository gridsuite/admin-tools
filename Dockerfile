FROM python:3.8.12-alpine

RUN apk add --no-cache curl jq && adduser -D powsybl
USER powsybl
WORKDIR /home/powsybl

COPY scripts/requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY scripts/ ./