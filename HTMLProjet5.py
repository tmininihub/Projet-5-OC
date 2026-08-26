from fastapi.responses import HTMLResponse


def accueil():
    return HTMLResponse("""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Prédiction de départ</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 850px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }

        h1 {
            text-align: center;
            margin-bottom: 35px;
        }

        .form-group {
            background: white;
            padding: 15px;
            margin-bottom: 12px;
            border-radius: 8px;
        }

        label {
            display: block;
            font-weight: bold;
            margin-bottom: 8px;
        }

        .attendu {
            font-size: 13px;
            color: #666;
            margin-bottom: 8px;
        }

        input {
            width: 100%;
            padding: 10px;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        button {
            width: 100%;
            padding: 14px;
            margin-top: 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }

        #resultat {
            background: white;
            margin-top: 25px;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
        }
    </style>
</head>

<body>

    <h1>Prédiction de départ d'un employé</h1>

    <form id="predictionForm">

        <div class="form-group">
            <label>Âge</label>
            <div class="attendu">Attendu : int (entre 18 et 100)</div>
            <input type="number" id="age" required>
        </div>

        <div class="form-group">
            <label>Genre</label>
            <div class="attendu">Attendu : str (F ou M)</div>
            <input type="text" id="genre" required>
        </div>

        <div class="form-group">
            <label>Revenu mensuel</label>
            <div class="attendu">Attendu : int (entre 2000 et 20000)</div>
            <input type="number" id="revenu_mensuel" required>
        </div>

        <div class="form-group">
            <label>Statut marital</label>
            <div class="attendu">
                Attendu : str (Célibataire, Marié(e), Divorcé(e))
            </div>
            <input type="text" id="statut_marital" required>
        </div>

        <div class="form-group">
            <label>Poste</label>
            <div class="attendu">
                Attendu : str (Cadre Commercial, Assistant de Direction,
                Consultant, Tech Lead, Manager, Senior Manager,
                Représentant Commercial, Directeur Technique,
                Ressources Humaines)
            </div>
            <input type="text" id="poste" required>
        </div>

        <div class="form-group">
            <label>Nombre d'expériences précédentes</label>
            <div class="attendu">Attendu : int</div>
            <input type="number" id="nombre_experiences_precedentes" required>
        </div>

        <div class="form-group">
            <label>Années dans l'entreprise</label>
            <div class="attendu">Attendu : int</div>
            <input type="number" id="annees_dans_l_entreprise" required>
        </div>

        <div class="form-group">
            <label>Satisfaction environnement</label>
            <div class="attendu">Attendu : int</div>
            <input type="number" id="satisfaction_employee_environnement" required>
        </div>

        <div class="form-group">
            <label>Satisfaction équipe</label>
            <div class="attendu">Attendu : int</div>
            <input type="number" id="satisfaction_employee_equipe" required>
        </div>

        <div class="form-group">
            <label>Heures supplémentaires</label>
            <div class="attendu">Attendu : str (Oui ou Non)</div>
            <input type="text" id="heure_supplementaires" required>
        </div>

        <div class="form-group">
            <label>Augmentation de salaire précédente</label>
            <div class="attendu">Attendu : int (en %)</div>
            <input type="number" id="augementation_salaire_precedente" required>
        </div>

        <div class="form-group">
            <label>Nombre de participations au PEE (Plan d'Épargne Entreprise)</label>
            <div class="attendu">Attendu : int</div>
            <input type="number" id="nombre_participation_pee" required>
        </div>

        <div class="form-group">
            <label>Nombre de formations suivies</label>
            <div class="attendu">Attendu : int</div>
            <input type="number" id="nb_formations_suivies" required>
        </div>

        <div class="form-group">
            <label>Distance domicile-travail</label>
            <div class="attendu">Attendu : int (en km)</div>
            <input type="number" id="distance_domicile_travail" required>
        </div>

        <div class="form-group">
            <label>Niveau d'éducation</label>
            <div class="attendu">Attendu : int</div>
            <input type="number" id="niveau_education" required>
        </div>

        <div class="form-group">
            <label>Domaine d'étude</label>
            <div class="attendu">
                Attendu : str (Infra & Cloud, Autre, Transformation Digitale,
                Marketing, Entrepreunariat, Ressources Humaines)
            </div>
            <input type="text" id="domaine_etude" required>
        </div>

        <div class="form-group">
            <label>Années depuis la dernière promotion</label>
            <div class="attendu">Attendu : int</div>
            <input type="number" id="annees_depuis_la_derniere_promotion" required>
        </div>

        <button type="submit">PRÉDIRE</button>

    </form>

    <div id="resultat"></div>

    <script>
        document.getElementById("predictionForm").addEventListener(
            "submit",
            async function(event) {

                event.preventDefault();

                const data = {
                    age: Number(document.getElementById("age").value),
                    genre: document.getElementById("genre").value,
                    revenu_mensuel: Number(
                        document.getElementById("revenu_mensuel").value
                    ),
                    statut_marital:
                        document.getElementById("statut_marital").value,
                    poste:
                        document.getElementById("poste").value,
                    nombre_experiences_precedentes: Number(
                        document.getElementById(
                            "nombre_experiences_precedentes"
                        ).value
                    ),
                    annees_dans_l_entreprise: Number(
                        document.getElementById(
                            "annees_dans_l_entreprise"
                        ).value
                    ),
                    satisfaction_employee_environnement: Number(
                        document.getElementById(
                            "satisfaction_employee_environnement"
                        ).value
                    ),
                    satisfaction_employee_equipe: Number(
                        document.getElementById(
                            "satisfaction_employee_equipe"
                        ).value
                    ),
                    heure_supplementaires:
                        document.getElementById(
                            "heure_supplementaires"
                        ).value,
                    augementation_salaire_precedente: Number(
                        document.getElementById(
                            "augementation_salaire_precedente"
                        ).value
                    ),
                    nombre_participation_pee: Number(
                        document.getElementById(
                            "nombre_participation_pee"
                        ).value
                    ),
                    nb_formations_suivies: Number(
                        document.getElementById(
                            "nb_formations_suivies"
                        ).value
                    ),
                    distance_domicile_travail: Number(
                        document.getElementById(
                            "distance_domicile_travail"
                        ).value
                    ),
                    niveau_education: Number(
                        document.getElementById(
                            "niveau_education"
                        ).value
                    ),
                    domaine_etude:
                        document.getElementById(
                            "domaine_etude"
                        ).value,
                    annees_depuis_la_derniere_promotion: Number(
                        document.getElementById(
                            "annees_depuis_la_derniere_promotion"
                        ).value
                    )
                };

                const resultat = document.getElementById("resultat");

                resultat.textContent = "Prédiction en cours...";

                try {

                    const response = await fetch(
                        "/PredictionUser",
                        {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify(data)
                        }
                    );

                    if (!response.ok) {
                        throw new Error("Erreur " + response.status);
                    }

                    const prediction = await response.json();

                    resultat.innerHTML = `
                        <p>Probabilité de rester :
                        ${prediction[0].STAY}</p>

                        <p>Probabilité de partir :
                        ${prediction[0].LEAVE}</p>
                    `;

                } catch (error) {

                    resultat.textContent =
                        "Une erreur est survenue : " + error.message;

                }
            }
        );
    </script>

</body>
</html>
""")