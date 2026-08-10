FROM python:3.12-slim

WORKDIR /code

# Install build tools required by torch/transformers wheels resolution
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl sqlite3\
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Install dependencies first so this layer is cached unless requirements change
COPY requirements.in .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip compile requirements.in -o requirements.txt \
    && uv pip sync requirements.txt --system

COPY app ./app/

EXPOSE 8000

CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000"]
