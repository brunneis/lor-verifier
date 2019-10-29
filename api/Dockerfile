FROM brunneis/python:3.7
LABEL maintainer "Rodrigo Martínez <rodrigo@martinez.gal>"
COPY api.py /
RUN \
    apt-get update \
    && apt-get -y install build-essential \
    && pip install \
    fastapi \
    uvicorn
ENTRYPOINT uvicorn api:app --host 0.0.0.0 --port 8080