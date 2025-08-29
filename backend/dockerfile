FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN adduser --system --group appuser


WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . /app

USER appuser


ENV DJANGO_SETTINGS_MODULE=backend.settings
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000", "--config", "gunicorn.conf.py"]