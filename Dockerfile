FROM python:3.8.12-alpine

RUN adduser -D powsybl
USER powsybl
WORKDIR /home/powsybl
COPY functions functions
COPY requirements.txt \
    constant.py \
    delete_computation_results.py \
    delete_indexed_equipments.py \
    ./
RUN pip3 install -r requirements.txt
CMD [ "python", "delete_indexed_equipments.py" ]
