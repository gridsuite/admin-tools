FROM python:3.8.12-alpine

RUN adduser -D powsybl
USER powsybl
WORKDIR /home/powsybl
COPY functions functions
COPY requirements.txt \
    constant.py \
    delete_computation_results.py \
    delete_indexed_equipments.py \
    delete_stashed_elements.py \
    invalidate_nodes_builds.py \
    reset_indexed_elements.py \
    ./
RUN pip3 install -r requirements.txt
# We call a script here, but it's overwritten at job execution by the way
# depending at which script should be applied
# it's a dry-run call by default to avoid unexpected impact with this image
CMD [ "python", "delete_indexed_equipments.py", "--dry-run" ]
