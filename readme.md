# Projet Koann - Application Web et Mobile
## Présentation

Ce projet est une application web développée avec Django et PostgreSQL.
L’objectif est de migrer vers une architecture sécurisée et performante sur AWS (ECS/EKS, RDS, S3, CloudFront, etc.) en suivant les bonnes pratiques de cybersécurité.

## Stack technique
- **Backend** : Django 5.4.2 (Python 3.13)
- **Base de données** : PostgreSQL
- **Serveur d’application** : Gunicorn
- **Proxy / Serveur web** : Nginx
- **Gestion des tâches asynchrones** *(prévu)* : Celery + Redis / RabbitMQ
- **Stockage statique/média** : S3 en production, dossier local en dev
- **Conteneurisation** : Docker & Docker Compose
- **CI/CD** : GitHub Actions (ou GitLab CI selon le repo)

---

## Installation et démarrage

### 1. Prérequis
- Docker & Docker Compose installés      

### 2. Cloner le projet
```bash
git clone git@github.com:organisation/koann_aws.git
cd koann_aws
```

### 3. Variables d’environnement

Créer un fichier .env à la racine du projet à partir du fichier .env.sample :


### 4. Lancer en local (Docker)

```bash
docker compose up --build
```

L’application sera disponible sur http://localhost:8000

### 5. Exécuter les migrations

```bash
docker compose run --rm koann-web python manage.py migrate
```

### 6. Créer un superutilisateur

```bash
docker compose run --rm koann-web python manage.py createsuperuser
```

## Structure du projet

```
koann_aws/
├── core/ # Code Django
│ ├── settings/ # Settings Django (base, dev, prod)
│ ├── users/ 
│ ├── common/ # App common
│ ├── jobs/ # Business app
│ ├── ...
├── docker/ # Dockerfiles & config nginx
├── compose.yml # Docker Compose (dev)
├── requirements.txt # Dépendances Python
├── manage.py
```

⚙️ Commandes utiles

Lancer les tests :
```bash
docker compose run --rm koann-web pytest
```

Collecter les fichiers statiques :
```bash
docker compose run --rm koann-web python manage.py collectstatic
```

Ouvrir un shell Django :
```bash
docker compose run --rm koann-web python manage.py shell
```

## Workflow Dev

1. Créer une branche feature/ avant de développer
2. Lancer l’app avec Docker pour s’assurer de la compatibilité.
3. Écrire des tests unitaires (pytest / Django test framework).
4. Faire un commit clair et une pull request.
5. La CI vérifiera linting, migrations, tests.

## Bonnes pratiques sécurité

- Ne jamais commiter .env ni secrets dans le repo.
- Les clés et credentials sensibles sont stockés dans AWS Secrets Manager en prod.
- Les fichiers statiques/médias sont servis via S3 + CloudFront.
- Les migrations doivent être validées avant tout déploiement.

## Roadmap
- Intégration Celery + Redis pour les tâches asynchrones
- Déploiement AWS avec Terraform + ECS
- Mise en place CI/CD (GitHub Actions)
- Monitoring (Prometheus / CloudWatch)
