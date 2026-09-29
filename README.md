# Projet 5 - Déploiement d'un modèle de Machine Learning (Futurisys)

API FastAPI qui expose le modèle du projet 4 : à partir des caractéristiques d'un employé, il prédit s'il va **rester (`STAY`) ou quitter (`LEAVE`)** l'entreprise. Chaque requête et chaque prédiction sont enregistrées dans une base PostgreSQL.

Dépôt : https://github.com/tmininihub/Projet-5-OC

## Fonctionnement

```
Client ──► API FastAPI ──► Modèle (pipeline scikit-learn + LightGBM)
               └──► PostgreSQL (inputs et outputs enregistrés)
```

Fichiers principaux : `main.py` (API), `model_trained` (pipeline entraîné, chargé avec `joblib`), `create_db.sql` (création des tables), `requirements.txt`, `.github/workflows/CICD.yml` (pipeline), fichiers `test_*.py` (tests).

## Installation

Prérequis : Python 3.11+, PostgreSQL, Git.

```bash
git clone https://github.com/tmininihub/Projet-5-OC.git
cd Projet-5-OC
python -m venv .venv          # puis l'activer
pip install -r requirements.txt
```

## Configuration

L'URL de la base est lue dans la variable d'environnement `URLBDD`. En local, crée un fichier `.env` à la racine (à ne pas commiter) :

```dotenv
URLBDD=postgresql+psycopg://utilisateur:motdepasse@localhost:5432/nom_de_la_base
```

## Utilisation

```bash
uvicorn main:app --reload
```

| Méthode | Route | Description |
|---|---|---|
| GET | `/` | Vérifie que l'API répond |
| POST | `/PredictionUser` | Reçoit un employé en JSON, renvoie la prédiction |
| GET | `/docs` | Documentation Swagger (schéma des données et exemples d'appel) |

Le JSON d'entrée est validé par Pydantic (classe `Features`, 30 champs : profil, poste, satisfaction, évaluations, etc.). Une donnée manquante ou hors des valeurs autorisées renvoie une erreur 422. Le détail des champs est dans `/docs`.

Les noms de champs sont ceux de l'entraînement du modèle, fautes comprises (`augementation_salaire_precedente`, `annes_sous_responsable_actuel`, `Entrepreunariat`) : ne pas les corriger sans réentraîner.

Exemple de sortie enregistrée en base :

```python
{'prediction': 'STAY', 'STAY': '92.8%', 'LEAVE': '7.2%'}
```

## Modèle

- Classification binaire sur `a_quitte_l_entreprise`.
- Pipeline scikit-learn (prétraitement `ColumnTransformer` + LightGBM) qui reçoit les données brutes et sauvegardé avec `joblib` **après** l'entraînement (`joblib.dump(pipeline, "model_trained")`), sinon l'API lève `NotFittedError`.
- Données : 3 CSV (SIRH, évaluations, sondage) fusionnés sur l'identifiant employé, soit 1470 employés.

### Performances

Classe `OUI` = l'employé quitte l'entreprise.

| Jeu | Accuracy | Précision (OUI) | Recall (OUI) | F1 (OUI) |
|---|---|---|---|---|
| Train (1176) | 0.93 | 0.71 | 1.00 | 0.83 |
| Test (294) | 0.76 | 0.35 | 0.60 | 0.44 |

Matrice de confusion sur le jeu de test :

| | Prédit NON | Prédit OUI |
|---|---|---|
| Réel NON | 195 | 52 |
| Réel OUI | 19 | 28 |

## Base de données

Exécuter `create_db.sql` dans une base PostgreSQL existante (par exemple via le Query Tool de pgAdmin) crée trois tables :

| Table | Contenu |
|---|---|
| `employes` | Dataset complet (fusion des 3 CSV) |
| `predictions_inputs` | Une ligne par requête : les caractéristiques envoyées au modèle |
| `predictions_outputs` | Une ligne par prédiction : `prediction`, `"STAY"`, `"LEAVE"` |

## Tests

```bash
pytest
pytest --cov=. --cov-report=term-missing   # avec couverture (pip install pytest-cov)
```

Les tests appellent la route `/PredictionUser` avec le `TestClient` de FastAPI et utilisent la base définie par `URLBDD`.

## CI/CD

À chaque `push`, le pipeline GitHub Actions lance le job `test` (installation des dépendances, `pytest`). Si les tests passent, le job `deploy` lance l'API avec uvicorn (port 8000).

Les jobs tournent sur un **runner auto-hébergé** (ton PC), le déploiement est donc local, ce que la mission accepte. Le secret GitHub `URLBDD` (Settings → Secrets and variables → Actions) fournit l'URL de la base.

Pour installer le runner : Settings → Actions → Runners → New self-hosted runner, suivre les commandes affichées, puis lancer `./run.cmd` et laisser la fenêtre ouverte. Sans runner actif, les jobs restent en attente.

## Sécurité

- Le mot de passe de la base n'est jamais dans le code : fichier `.env` (ignoré par Git) en local, secret GitHub dans le pipeline.
- Pydantic rejette les entrées invalides avant d'appeler le modèle ou la base.
- Authentification : les clés sont stockées dans les secrets GitHub (Settings → Secrets and variables → Actions).
