import pytest
from main import app, engine
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

def test_prediction():
    Client = TestClient(app)
    request = Client.post("/PredictionUser",params={"id_employee": "1"})
    assert request.status_code == 200
    request = request.json()
    row = request[1]
    dico_database = request[0]
    assert 18 <= row[0]["age"] <= 70
    assert 1000 <= row[0]["revenu_mensuel"] <= 20000
    assert row[0]["genre"] in ["F", "M"]
    assert dico_database['prediction'] in ['STAY', 'LEAVE']