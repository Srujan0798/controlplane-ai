FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY controlplane ./controlplane
COPY policies ./policies
COPY examples ./examples
COPY docs ./docs

RUN pip install --no-cache-dir -e . \
 && useradd --create-home --uid 1000 --shell /usr/sbin/nologin cp \
 && mkdir -p /app/.data \
 && chown -R cp:cp /app

USER cp

EXPOSE 8080
ENV HOST=0.0.0.0 PORT=8080
CMD ["uvicorn", "controlplane.server.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8080"]
