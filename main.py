import joblib
import uvicorn
import fastapi
import numpy as np
import dotenv
import os
import sqlalchemy
import pandas as pd
import pytest
from sqlalchemy import create_engine, engine, text
import uuid

from sqlalchemy import create_engine
from dotenv import load_dotenv
from typing import Literal
from sklearn.preprocessing import LabelEncoder, StandardScaler
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from HTMLProjet5 import accueil
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
load_dotenv()

URLBDD = os.getenv("URLBDD")

app = FastAPI()
LE = LabelEncoder()

class Features(BaseModel):
    age: int
    genre: Literal['F', 'M']
    revenu_mensuel: int
    statut_marital: Literal['Célibataire', 'Marié(e)', 'Divorcé(e)']
    departement: Literal['Commercial', 'Consulting', 'Ressources Humaines']
    poste: Literal['Cadre Commercial', 'Assistant de Direction', 'Consultant', 'Tech Lead', 'Manager', 'Senior Manager', 'Représentant Commercial', 'Directeur Technique', 'Ressources Humaines']
    nombre_experiences_precedentes: int
    nombre_heures_travailless: int
    annees_dans_l_entreprise: int
    annees_dans_le_poste_actuel: int
    satisfaction_employee_environnement: int
    satisfaction_employee_nature_travail: int
    satisfaction_employee_equipe: int
    satisfaction_employee_equilibre_pro_perso: int
    note_evaluation_precedente: int
    note_evaluation_actuelle: int
    heure_supplementaires: Literal['Oui', 'Non']
    augementation_salaire_precedente: int
    nombre_participation_pee: int
    nb_formations_suivies: int
    nombre_employee_sous_responsabilite: int
    distance_domicile_travail: int
    niveau_education: int
    domaine_etude: Literal['Infra & Cloud', 'Autre', 'Transformation Digitale', 'Marketing', 'Entrepreunariat', 'Ressources Humaines']
    ayant_enfants: Literal['Y']
    frequence_deplacement: Literal['Aucun', 'Occasionnel', 'Frequent']
    annees_depuis_la_derniere_promotion: int
    annes_sous_responsable_actuel: int
    Frequence_changement_emploi: float
    Satisfaction_totale: float

model_trained = joblib.load("model_trained")
LE_HeureSup = joblib.load("LE_HeureSup")

@app.get("/", response_class=HTMLResponse)
def home():
    return accueil()

@app.post("/PredictionUser")
def PredictionUser(features:Features):
    dico = {}
    dico_database = {}

    features = features.model_dump()
    df_features = pd.DataFrame([features])

    engine = create_engine(URLBDD)

    df_features.to_sql(
        "Project5_Features",
        con=engine,
        if_exists="append",
        index=False
    )
    df_features["heure_supplementaires"] = LE_HeureSup.transform(df_features["heure_supplementaires"])
    prediction = model_trained.predict(df_features)
    prediction_proba = model_trained.predict_proba(df_features)
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

    return dico, dico_database

features = {
  "age": 41,
  "genre": "F",
  "revenu_mensuel": 5993,
  "statut_marital": "Célibataire",
  "departement": "Commercial",
  "poste": "Cadre Commercial",
  "nombre_experiences_precedentes": 8,
  "nombre_heures_travailless": 80,
  "annees_dans_l_entreprise": 6,
  "annees_dans_le_poste_actuel": 4,
  "satisfaction_employee_environnement": 2,
  "satisfaction_employee_nature_travail": 4,
  "satisfaction_employee_equipe": 1,
  "satisfaction_employee_equilibre_pro_perso": 1,
  "note_evaluation_precedente": 3,
  "note_evaluation_actuelle": 3,
  "heure_supplementaires": "Oui",
  "augementation_salaire_precedente": 11,
  "nombre_participation_pee": 0,
  "nb_formations_suivies": 0,
  "nombre_employee_sous_responsabilite": 1,
  "distance_domicile_travail": 1,
  "niveau_education": 2,
  "domaine_etude": "Infra & Cloud",
  "ayant_enfants": "Y",
  "frequence_deplacement": "Occasionnel",
  "annees_depuis_la_derniere_promotion": 0,
  "annes_sous_responsable_actuel": 5,
  "Satisfaction_totale" : 4,
  "Frequence_changement_emploi": 0.5
}

# PredictionUser(Features(**features))
