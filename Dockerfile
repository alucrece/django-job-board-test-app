FROM python:3.14

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn job_board.wsgi:application --bind 0.0.0.0:8000 --workers 2"]