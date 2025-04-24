ARG PYTHON_VERSION=3.13

FROM python:${PYTHON_VERSION_SHORT}-slim-bookworm AS builder

RUN wget -qO- https://astral.sh/uv/install.sh | sh

WORKDIR /app
ADD . .
RUN uv sync --locked
EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
