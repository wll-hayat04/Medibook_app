FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8091

CMD ["sh", "-c", "python manage.py migrate && python manage.py loaddata fixtures/initial_data.json && python manage.py collectstatic --noinput && gunicorn medibook_project.wsgi:application --bind 0.0.0.0:${PORT:-8091}"]