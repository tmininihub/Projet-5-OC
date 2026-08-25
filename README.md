# Projet 5 – Développez une API Python pour un modèle de Machine Learning

Ce projet correspond au **Projet 5 du parcours OpenClassrooms**. Il reprend le modèle de Machine Learning développé lors du **Projet 4** et le rend accessible via une API web.

## Fonctionnalités

- API développée avec **FastAPI** et **Pydantic**.
- Endpoint `/PredictionUser` pour effectuer une prédiction à partir des caractéristiques d'un salarié.
- Utilisation du modèle entraîné lors du Projet 4.
- Encodage et normalisation des données avant prédiction.
- Enregistrement des prédictions et de leur historique dans **PostgreSQL**.
- Tests automatisés avec **Pytest**.
- Intégration continue avec **GitHub Actions**.
- Conteneurisation avec **Docker**.

## Installation

```bash
pip install -r requirements.txt
```

Configurer la variable d'environnement `URLBDD` pour la connexion PostgreSQL.

## Lancer l'API

```bash
uvicorn GitProject5:app --host 0.0.0.0 --port 8000
```

La documentation interactive de l'API est ensuite disponible sur `/docs`.

## Tests

```bash
pytest
```

## Docker

Construire et lancer l'application avec Docker à partir du `Dockerfile` fourni.

## Projet 4

Le modèle et les artefacts de préparation des données utilisés par cette API proviennent du travail réalisé dans le **Projet 4**. Le Projet 5 se concentre sur leur intégration dans une API, la persistance des prédictions, les tests et le déploiement.
