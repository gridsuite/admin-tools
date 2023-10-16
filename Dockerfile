FROM python:3.8.12-alpine
RUN mkdir -p /app
COPY functions /app/functions
COPY requirements.txt \
    constant.py \
    delete_computation_results.py \
    delete_indexed_equipments.py \
    /app/
RUN pip3 install -r /app/requirements.txt
CMD [ "python", "./app/delete_indexed_equipments.py" ]