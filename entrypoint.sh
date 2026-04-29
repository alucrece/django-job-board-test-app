#!/bin/sh

# On s'arrête si une commande échoue
set -e

echo "--- Étape 1 : Envoi des assets vers Azure Blob Storage ---"

python backend/backend/initialize_azure.py

echo "--- Étape 2 : Exécution des migrations de la base de données ---"
python manage.py migrate --noinput

echo "--- Étape 3 : Lancement de l'application avec Gunicorn ---"

exec gunicorn job_board.wsgi:application --bind 0.0.0.0:8000 --workers 2