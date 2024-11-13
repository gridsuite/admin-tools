FROM python:3.8.12-alpine

RUN adduser -D powsybl
USER powsybl
WORKDIR /home/powsybl

COPY scripts/requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY scripts/ ./

# We call a script here, but it's overwritten at job execution by the way
# depending at which script should be applied
# it's a dry-run call by default to avoid unexpected impact with this image
CMD [ "python", "delete_indexed_equipments.py", "--dry-run" ]
