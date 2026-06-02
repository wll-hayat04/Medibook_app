FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8091

CMD ["gunicorn", "medibook_project.wsgi:application", "--bind", "0.0.0.0:8091"]