FROM python:3.8.12-alpine

RUN adduser -D powsybl
USER powsybl
WORKDIR /home/powsybl
COPY scripts/ ./

RUN pip3 install -r requirements.txt

# We call a dummy code by default to avoid unexpected impact with this image
# It's overwritten at job execution by the way depending at which script should be applied
CMD [ "python", "-c", "print('Please specify the script to run in the container CMD.')"]
