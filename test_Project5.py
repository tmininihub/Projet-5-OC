import pytest
from main import Features, app, engine
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
    age=41,
    genre="F",
    revenu_mensuel=5993,
    statut_marital="Célibataire",
    departement="Commercial",
    poste="Cadre Commercial",
    nombre_experiences_precedentes=8,
    nombre_heures_travailless=80,
    annees_dans_l_entreprise=6,
    annees_dans_le_poste_actuel=4,
    satisfaction_employee_environnement=2,
    satisfaction_employee_nature_travail=4,
    satisfaction_employee_equipe=1,
    satisfaction_employee_equilibre_pro_perso=1,
    note_evaluation_precedente=3,
    note_evaluation_actuelle=3,
    heure_supplementaires="Oui",
    augementation_salaire_precedente=11,
    nombre_participation_pee=0,
    nb_formations_suivies=0,
    nombre_employee_sous_responsabilite=1,
    distance_domicile_travail=1,
    niveau_education=2,
    domaine_etude="Infra & Cloud",
    ayant_enfants="Y",
    frequence_deplacement="Occasionnel",
    annees_depuis_la_derniere_promotion=0,
    annes_sous_responsable_actuel=5,
    Frequence_changement_emploi=2.0,
    Satisfaction_totale=2.0,
)

def test_prediction():
    # assert isinstance(features, Features)
    Client = TestClient(app)
    features_test = features.model_dump()
    request = Client.post("/PredictionUser",json=features_test)
    assert request.status_code == 200
    request = request.json()
    dico = request[0]
    dico_database = request[1]
    assert dico is not None
    assert dico_database['prediction'] in ['STAY', 'LEAVE']
