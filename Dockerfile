FROM python:3.15.0rc2 AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_PROJECT_ENVIRONMENT=/opt/venv

WORKDIR /app

# Слой зависимостей — кэшируется, пока не изменится pyproject.toml/uv.lock
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Слой кода — инвалидируется при каждом изменении исходников
COPY . .
RUN uv sync --frozen --no-dev

FROM python:3.15.0rc2

RUN useradd --create-home appuser
WORKDIR /home/appuser/app

COPY --from=builder /opt/venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]