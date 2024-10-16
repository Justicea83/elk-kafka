FROM python:3
LABEL maintainer="justicea83"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    librdkafka-dev \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /tmp/requirements.txt
RUN mkdir "app"
COPY ./stream.py /app
COPY ./check_kafka.py /app

WORKDIR /app

RUN python -m venv /py && \
    . /py/bin/activate && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt

ENV PATH="/py/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:/app"


ENTRYPOINT ["python", "/app/check_kafka.py"]