FROM python:3.12.5-slim-bullseye

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY . /app

WORKDIR /app
RUN uv pip install -r pyproject.toml --system --no-cache

ENTRYPOINT ["scripts/entrypoint.sh"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
