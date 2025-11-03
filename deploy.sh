#!/bin/bash

# Script de déploiement Django

set -e  # Arrête le script en cas d'erreur

echo "Début du déploiement Django..."

# Variables
APP_DIR="/var/www/koann"
VENV_DIR="$APP_DIR/venv"

# Aller dans le dossier de l'application
cd $APP_DIR || exit 1

# Pull les dernières modifications
echo "Récupération des modifications Git..."
git pull origin main || exit 1

# Activation du virtualenv
echo "Activation du virtualenv..."
source $VENV_DIR/bin/activate || exit 1

# Installation des dépendances
echo "Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt || exit 1

# Migrations de la base de données
echo "Application des migrations..."
python manage.py migrate --noinput || exit 1

# Collecte des fichiers statiques
echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput || exit 1

# Redémarrage de Supervisor
echo "Redémarrage de l'application..."
sudo supervisorctl restart all || exit 1

echo "Déploiement terminé avec succès!"

# Afficher le statut
sudo supervisorctl status