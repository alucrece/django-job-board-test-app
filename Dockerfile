FROM node:20-alpine AS tailwind-builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build:css

FROM python:3.14

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . .

COPY --from=tailwind-builder /app/static /app/static
RUN python manage.py collectstatic --noinput
RUN chmod +x /app/entrypoint.sh
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn job_board.wsgi:application --bind 0.0.0.0:8000 --workers 2"]

ENTRYPOINT ["/app/entrypoint.sh"]