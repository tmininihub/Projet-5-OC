# Projet 5 - Prédire le départ d'un employé (Futurisys)

## C'est quoi ce projet ?

Une entreprise veut savoir quels employés risquent de la quitter. Ce projet met à disposition un **modèle de Machine Learning** (entraîné au projet 4) sous la forme d'une **API** : un petit service web auquel on envoie l'identifiant d'un employé et qui répond **`STAY`** (il reste) ou **`LEAVE`** (il part), avec une probabilité.

Dépôt : https://github.com/tmininihub/Projet-5-OC

## Comment ça marche

1. L'utilisateur saisit l'identifiant d'un employé sur une page web.
2. L'API retrouve les informations de cet employé dans une base de données PostgreSQL.
3. Le modèle calcule la prédiction à partir de ces informations.
4. La prédiction s'affiche, et la requête avec son résultat est enregistrée dans la base.

## Installation

Il faut Python 3.11 ou plus, PostgreSQL et Git.

```bash
git clone https://github.com/tmininihub/Projet-5-OC.git
cd Projet-5-OC
python -m venv .venv          # puis activer cet environnement
pip install -r requirements.txt
```

**Créer la base** : créer une base vide dans PostgreSQL (par exemple avec pgAdmin), puis y exécuter le fichier `create_db.sql`, qui crée les tables.

**Indiquer où se trouve la base** : créer un fichier `.env` à la racine du projet avec l'adresse de la base :

```dotenv
URLBDD=postgresql+psycopg://utilisateur:motdepasse@localhost:5432/nom_de_la_base
```

## Utilisation

```bash
uvicorn main:app --reload
```

Ouvrir ensuite http://127.0.0.1:8000, saisir un identifiant d'employé et cliquer sur **PRÉDIRE**.

La documentation interactive de l'API (routes, exemples d'appel) est sur http://127.0.0.1:8000/docs.

## Le modèle

Le modèle classe chaque employé en `STAY` ou `LEAVE`. Il a été entraîné sur les données de 1470 employés (profil, poste, satisfaction, évaluations, etc.).

| | Accuracy | Précision (OUI) | Recall (OUI) | F1 (OUI) |
|---|---|---|---|---|
| Entraînement | 0.93 | 0.71 | 1.00 | 0.83 |
| Test | 0.76 | 0.35 | 0.60 | 0.44 |

« OUI » = l'employé quitte l'entreprise. Matrice de confusion sur le jeu de test :

| | Prédit NON | Prédit OUI |
|---|---|---|
| Réel NON | 195 | 52 |
| Réel OUI | 19 | 28 |

## La base de données

Trois tables, créées par `create_db.sql` :

- `employes` : les données de chaque employé.
- `predictions_inputs` : les données envoyées au modèle à chaque requête.
- `predictions_outputs` : les prédictions rendues par le modèle.

Les deux dernières gardent une trace de toutes les utilisations de l'API.

## Les tests

Les tests vérifient automatiquement que l'API et la validation des données fonctionnent. Pour les lancer :

```bash
pytest --cov=main --cov-report=term-missing
```

Le rapport indique le pourcentage du code couvert par les tests (actuellement 97 %).

## Déploiement automatique (CI/CD)

À chaque `git push`, GitHub lance automatiquement deux étapes, définies dans `.github/workflows/CICD.yml` :

1. **Test** : le code est testé.
2. **Déploiement** : si les tests réussissent, l'API est démarrée sur l'ordinateur local.

Pour que GitHub puisse exécuter ces étapes sur ton ordinateur, il faut y lancer un petit programme appelé **runner**.

**Installation du runner (une seule fois)** : sur GitHub, aller dans **Settings → Actions → Runners → New self-hosted runner**, choisir Windows et exécuter dans PowerShell les commandes affichées.

**Lancement du runner (à chaque session)** : dans un terminal où l'environnement Python du projet est activé :

```
cd C:\actions-runner
run.cmd
```

Laisser la fenêtre ouverte. Si le runner est éteint, GitHub reste en attente (« Waiting for a runner ») et rien ne démarre.

## Sécurité

- Le mot de passe de la base n'est jamais écrit dans le code : il est dans le fichier `.env` (non envoyé sur GitHub) en local, et dans les secrets GitHub (Settings → Secrets and variables → Actions) pour le déploiement automatique.
- Les données reçues par l'API sont vérifiées avant d'être utilisées.
