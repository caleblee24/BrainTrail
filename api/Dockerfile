FROM python:3.11-slim
WORKDIR /app
ENV PIP_NO_CACHE_DIR=1
COPY pyproject.toml /app/
RUN pip install --upgrade pip && pip install -e .
COPY app /app/app
CMD ["uvicorn", "app.main:create_app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
