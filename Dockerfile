FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential gcc g++ python3-dev libffi-dev libssl-dev libjpeg-dev zlib1g-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

RUN pip install torch==2.9.1+cpu --extra-index-url https://download.pytorch.org/whl/cpu

COPY requirements_docker.txt .
RUN pip install -r requirements_docker.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py loaddata fixtures/initial_data.json || true && python manage.py runserver 0.0.0.0:8000"]
