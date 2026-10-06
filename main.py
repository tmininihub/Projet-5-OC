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

model_trained = joblib.load("model_trained")
LE_HeureSup = joblib.load("LE_HeureSup")
EmployesBDD = joblib.load("EmployesBDD")

engine = create_engine(URLBDD)

EmployesBDD.to_sql(
    "employes",
    con=engine,
    if_exists="replace",
    index=False
)

@app.get("/", response_class=HTMLResponse)
def home():
    return accueil()

@app.post("/PredictionUser")
def PredictionUser(id_employee):
    dico = {}
    dico_database = {}

    with engine.connect() as conn:
        result = conn.execute(
            text('SELECT * FROM "employes" WHERE id_employee = :id'),
            {"id": id_employee}
        )
        row = result.fetchone()
    df_features = pd.DataFrame([row])
    df_features = df_features.drop(columns=["id_employee","niveau_hierarchique_poste","annee_experience_totale","annees_dans_l_entreprise"])
    print(df_features)
    row = df_features

    df_features.to_sql(
        "predictions_inputs",
        con=engine,
        if_exists="append",
        index=False
    )
    df_features["heure_supplementaires"] = LE_HeureSup.transform(df_features["heure_supplementaires"])
    prediction_proba = model_trained.predict_proba(df_features)
    proba = prediction_proba*100
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
    df_database = pd.DataFrame([dico_database])
    df_database.to_sql(
        "predictions_outputs",
        con=engine,
        if_exists="append",
        index=False
    )

    return dico_database, row.to_dict(orient="records")

