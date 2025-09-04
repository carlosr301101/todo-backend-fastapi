FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install uv

CMD [ "uv","sync" ]


