FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PATH="/opt/venv/bin:/root/.local/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends ca-certificates curl tini \
    && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /tmp/uv-installer.sh

RUN sh /tmp/uv-installer.sh \
    && rm /tmp/uv-installer.sh

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv python install 3.14 --install-dir /opt/python \
    && PYTHON_BIN="$(find /opt/python -path '*/bin/python3.14' -print -quit)" \
    && uv venv /opt/venv --python "$PYTHON_BIN" \
    && . /opt/venv/bin/activate \
    && uv sync --frozen --no-dev --active

COPY app ./app
COPY config.py wsgi.py ./

RUN useradd --create-home --uid 10001 --shell /usr/sbin/nologin appuser \
    && mkdir -p /tmp/flask_session \
    && chown -R appuser:appuser /app /opt/python /opt/venv /tmp/flask_session

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS http://127.0.0.1:5000/login || exit 1

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/opt/venv/bin/python", "-c", "from waitress import serve; from wsgi import app; serve(app, listen='0.0.0.0:5000')"]
