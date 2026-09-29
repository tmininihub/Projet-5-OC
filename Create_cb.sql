-- ============================================================
-- Création de la base et des tables - Projet 5 (Futurisys)
-- ============================================================

-- 1. Création de la base (à lancer depuis psql ou en étant connecté
--    à la base "postgres"), puis se connecter à cette base :
-- CREATE DATABASE projet_5_bdd;

-- ============================================================
-- Table du dataset complet (fusion des 3 CSV : SIRH, éval, sondage)
-- ============================================================
CREATE TABLE employes (
    id_employee                                INTEGER PRIMARY KEY,
    age                                        INTEGER NOT NULL,
    genre                                      VARCHAR(1) NOT NULL CHECK (genre IN ('F', 'M')),
    revenu_mensuel                             INTEGER NOT NULL,
    statut_marital                             VARCHAR(20) NOT NULL,
    departement                                VARCHAR(30) NOT NULL,
    poste                                      VARCHAR(40) NOT NULL,
    nombre_experiences_precedentes             INTEGER NOT NULL,
    nombre_heures_travailless                  INTEGER NOT NULL,
    annee_experience_totale                    INTEGER NOT NULL,
    annees_dans_l_entreprise                   INTEGER NOT NULL,
    annees_dans_le_poste_actuel                INTEGER NOT NULL,
    satisfaction_employee_environnement        INTEGER NOT NULL,
    note_evaluation_precedente                 INTEGER NOT NULL,
    niveau_hierarchique_poste                  INTEGER NOT NULL,
    satisfaction_employee_nature_travail       INTEGER NOT NULL,
    satisfaction_employee_equipe               INTEGER NOT NULL,
    satisfaction_employee_equilibre_pro_perso  INTEGER NOT NULL,
    eval_number                                INTEGER NOT NULL,
    note_evaluation_actuelle                   INTEGER NOT NULL,
    heure_supplementaires                      VARCHAR(3) NOT NULL CHECK (heure_supplementaires IN ('Oui', 'Non')),
    augementation_salaire_precedente           VARCHAR(10) NOT NULL,
    a_quitte_l_entreprise                      VARCHAR(3) NOT NULL CHECK (a_quitte_l_entreprise IN ('Oui', 'Non')),
    nombre_participation_pee                   INTEGER NOT NULL,
    nb_formations_suivies                      INTEGER NOT NULL,
    nombre_employee_sous_responsabilite        INTEGER NOT NULL,
    code_sondage                               INTEGER NOT NULL,
    distance_domicile_travail                  INTEGER NOT NULL,
    niveau_education                           INTEGER NOT NULL,
    domaine_etude                              VARCHAR(40) NOT NULL,
    ayant_enfants                              VARCHAR(1) NOT NULL,
    frequence_deplacement                      VARCHAR(20) NOT NULL,
    annees_depuis_la_derniere_promotion        INTEGER NOT NULL,
    annes_sous_responsable_actuel              INTEGER NOT NULL
);

-- ============================================================
-- Table des inputs envoyés au modèle (une ligne par requête)
-- ============================================================
CREATE TABLE predictions_inputs (
    id                                         SERIAL PRIMARY KEY,
    created_at                                 TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    age                                        INTEGER NOT NULL,
    genre                                      VARCHAR(1) NOT NULL,
    revenu_mensuel                             INTEGER NOT NULL,
    statut_marital                             VARCHAR(20) NOT NULL,
    departement                                VARCHAR(30) NOT NULL,
    poste                                      VARCHAR(40) NOT NULL,
    nombre_experiences_precedentes             INTEGER NOT NULL,
    nombre_heures_travailless                  INTEGER NOT NULL,
    annees_dans_l_entreprise                   INTEGER NOT NULL,
    annees_dans_le_poste_actuel                INTEGER NOT NULL,
    satisfaction_employee_environnement        INTEGER NOT NULL,
    satisfaction_employee_nature_travail       INTEGER NOT NULL,
    satisfaction_employee_equipe               INTEGER NOT NULL,
    satisfaction_employee_equilibre_pro_perso  INTEGER NOT NULL,
    note_evaluation_precedente                 INTEGER NOT NULL,
    note_evaluation_actuelle                   INTEGER NOT NULL,
    heure_supplementaires                      VARCHAR(3) NOT NULL,
    augementation_salaire_precedente           INTEGER NOT NULL,
    nombre_participation_pee                   INTEGER NOT NULL,
    nb_formations_suivies                      INTEGER NOT NULL,
    nombre_employee_sous_responsabilite        INTEGER NOT NULL,
    distance_domicile_travail                  INTEGER NOT NULL,
    niveau_education                           INTEGER NOT NULL,
    domaine_etude                              VARCHAR(40) NOT NULL,
    ayant_enfants                              VARCHAR(1) NOT NULL,
    frequence_deplacement                      VARCHAR(20) NOT NULL,
    annees_depuis_la_derniere_promotion        INTEGER NOT NULL,
    annes_sous_responsable_actuel              INTEGER NOT NULL,
    "Frequence_changement_emploi"              REAL NOT NULL,
    "Satisfaction_totale"                      REAL NOT NULL
);

-- ============================================================
-- Table des outputs du modèle
-- ============================================================
CREATE TABLE predictions_outputs (
    id                SERIAL PRIMARY KEY,
    prediction        VARCHAR(5) NOT NULL CHECK (prediction IN ('STAY', 'LEAVE')),
    "STAY"            VARCHAR(10) NOT NULL,
    "LEAVE"           VARCHAR(10) NOT NULL,
    created_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);