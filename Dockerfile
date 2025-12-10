
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY whisper ./whisper

RUN useradd -m appuser && chown -R appuser /app
USER appuser

CMD ["python", "-m", "whisper"]