import joblib
import uvicorn
import fastapi
import numpy as np
import dotenv
import os
import sqlalchemy
import pandas as pd
import pytest

from sqlalchemy import create_engine
from dotenv import load_dotenv
from typing import Literal
from sklearn.preprocessing import LabelEncoder, StandardScaler
from pydantic import BaseModel
from fastapi import FastAPI

load_dotenv()
URLBDD = os.getenv("URLBDD")

app = FastAPI()
LE = LabelEncoder()

model_trained = joblib.load("trained_grid_model")
print(model_trained.best_params_)

class Features(BaseModel):
    age : int
    genre : Literal['F', 'M']
    revenu_mensuel : int
    statut_marital : Literal['Célibataire', 'Marié(e)', 'Divorcé(e)']
    poste : Literal['Cadre Commercial', 'Assistant de Direction', 'Consultant', 'Tech Lead', 'Manager', 'Senior Manager', 'Représentant Commercial', 'Directeur Technique', 'Ressources Humaines']
    nombre_experiences_precedentes : int
    annees_dans_l_entreprise : int
    satisfaction_employee_environnement : int
    satisfaction_employee_equipe : int
    heure_supplementaires : Literal['Oui', 'Non']
    augementation_salaire_precedente : int
    nombre_participation_pee : int
    nb_formations_suivies : int
    distance_domicile_travail : int
    niveau_education : int
    domaine_etude : Literal['Infra & Cloud', 'Autre', 'Transformation Digitale', 'Marketing', 'Entrepreunariat', 'Ressources Humaines']
    annees_depuis_la_derniere_promotion : int

BDD = joblib.load("BDD")

engine = create_engine(URLBDD)

BDD.to_sql(
    "MyBDD",
    con=engine,
    if_exists="replace",
    index=False
)

LE_genre = joblib.load("LE_genre.pkl")
LE_status_martial = joblib.load("LE_statut_marital.pkl")
LE_poste = joblib.load("LE_poste.pkl")
LE_heure_supplementaires = joblib.load("LE_heure_supplementaires.pkl")
LE_domaine_etude = joblib.load("LE_domaine_etude.pkl")
Scaler = joblib.load("Scaler")

list_LE = [LE_genre, LE_status_martial, LE_poste, LE_heure_supplementaires, LE_domaine_etude]

@app.post("/PredictionUser")
def PredictionUser(features:Features):
    list_features = []
    dico = {}
    dico_database = {}

    index = 0
    features = features.model_dump()
    keys = features.keys()
    for i,key in zip(features,keys):
        list_features.append(features[i])

    for key,feature in zip(keys, list_features):
        dico_database[key] = feature

    for j,i in enumerate(list_features):
        if i == str(i):
            list_features[j] = list_LE[index].transform([list_features[j]])[0]
            index+=1

    tableau_features = np.array(list_features).reshape(1, -1)
    tableau_features = Scaler.transform(tableau_features)
    prediction = model_trained.predict(tableau_features)
    prediction_proba = model_trained.predict_proba(tableau_features)
    proba = prediction_proba*100
    print(proba)
    print(prediction)
    stay = f"{proba[0][0]:.1f}%"
    leave = f"{proba[0][1]:.1f}%"
    dico["STAY"] = stay
    dico["LEAVE"] = leave
    if proba[0][0] > proba[0][1]:
        dico_database["prediction"] = "STAY"
    else:
        dico_database["prediction"] = "LEAVE"

    dico_database["STAY"] = stay
    dico_database["LEAVE"] = leave
    print(dico_database)

    df = pd.DataFrame([dico_database])

    df.to_sql(
        "HistoryPredictions",
        con=engine,
        if_exists="append",
        index=False
    )

    return dico, dico_database
