import pytest
from Projet_5.TESTGitProject5 import PredictionUser, Features, app, engine
from sqlalchemy import create_engine, text
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
from fastapi.testclient import TestClient
import json

features = Features(
    age=35,
    genre="F",
    revenu_mensuel=19000,
    statut_marital="Célibataire",
    poste="Cadre Commercial",
    nombre_experiences_precedentes=4,
    annees_dans_l_entreprise=4,
    satisfaction_employee_environnement=3,
    satisfaction_employee_equipe=4,
    heure_supplementaires="Non",
    augementation_salaire_precedente=12,
    nombre_participation_pee=1,
    nb_formations_suivies=3,
    distance_domicile_travail=15,
    niveau_education=10,
    domaine_etude="Infra & Cloud",
    annees_depuis_la_derniere_promotion=2
)

def test_prediction():
    assert isinstance(features, Features)
    assert 18 <= features.age <= 70
    assert 1000 <= features.revenu_mensuel <= 20000
    dico, dico_database = PredictionUser(features)
    assert dico is not None
    assert dico_database['prediction'] in ['STAY', 'LEAVE']

def test_CLient():
    Client = TestClient(app)
    features_test = features.model_dump()
    request = Client.post("/PredictionUser",json=features_test)
    assert request.status_code == 200
