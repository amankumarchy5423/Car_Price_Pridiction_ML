FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN apt update -y && \
    pip install uv && \
    uv venv && \
    uv pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["uv","run" ,"app.py"]

