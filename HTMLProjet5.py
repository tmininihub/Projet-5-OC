from fastapi.responses import HTMLResponse

def accueil():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Prédiction de départ</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 40px auto;
                padding: 20px;
            }

            h1 {
                text-align: center;
            }

            .form-group {
                margin-bottom: 15px;
            }

            label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }

            input, select {
                width: 100%;
                padding: 10px;
                box-sizing: border-box;
            }

            button {
                width: 100%;
                padding: 12px;
                margin-top: 20px;
                cursor: pointer;
                font-size: 16px;
            }

            #resultat {
                margin-top: 25px;
                padding: 20px;
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
                <input type="number" id="age" required>
            </div>

            <div class="form-group">
                <label>Genre</label>
                <select id="genre" required>
                    <option value="F">F</option>
                    <option value="M">M</option>
                </select>
            </div>

            <div class="form-group">
                <label>Revenu mensuel</label>
                <input type="number" id="revenu_mensuel" required>
            </div>

            <div class="form-group">
                <label>Statut marital</label>
                <select id="statut_marital" required>
                    <option value="Célibataire">Célibataire</option>
                    <option value="Marié(e)">Marié(e)</option>
                    <option value="Divorcé(e)">Divorcé(e)</option>
                </select>
            </div>

            <div class="form-group">
                <label>Poste</label>
                <select id="poste" required>
                    <option value="Cadre Commercial">Cadre Commercial</option>
                    <option value="Assistant de Direction">Assistant de Direction</option>
                    <option value="Consultant">Consultant</option>
                    <option value="Tech Lead">Tech Lead</option>
                    <option value="Manager">Manager</option>
                    <option value="Senior Manager">Senior Manager</option>
                    <option value="Représentant Commercial">Représentant Commercial</option>
                    <option value="Directeur Technique">Directeur Technique</option>
                    <option value="Ressources Humaines">Ressources Humaines</option>
                </select>
            </div>

            <div class="form-group">
                <label>Nombre d'expériences précédentes</label>
                <input type="number" id="nombre_experiences_precedentes" required>
            </div>

            <div class="form-group">
                <label>Années dans l'entreprise</label>
                <input type="number" id="annees_dans_l_entreprise" required>
            </div>

            <div class="form-group">
                <label>Satisfaction environnement</label>
                <input type="number" id="satisfaction_employee_environnement" required>
            </div>

            <div class="form-group">
                <label>Satisfaction équipe</label>
                <input type="number" id="satisfaction_employee_equipe" required>
            </div>

            <div class="form-group">
                <label>Heures supplémentaires</label>
                <select id="heure_supplementaires" required>
                    <option value="Oui">Oui</option>
                    <option value="Non">Non</option>
                </select>
            </div>

            <div class="form-group">
                <label>Augmentation de salaire précédente</label>
                <input type="number" id="augementation_salaire_precedente" required>
            </div>

            <div class="form-group">
                <label>Nombre de participations au PEE</label>
                <input type="number" id="nombre_participation_pee" required>
            </div>

            <div class="form-group">
                <label>Nombre de formations suivies</label>
                <input type="number" id="nb_formations_suivies" required>
            </div>

            <div class="form-group">
                <label>Distance domicile-travail</label>
                <input type="number" id="distance_domicile_travail" required>
            </div>

            <div class="form-group">
                <label>Niveau d'éducation</label>
                <input type="number" id="niveau_education" required>
            </div>

            <div class="form-group">
                <label>Domaine d'étude</label>
                <select id="domaine_etude" required>
                    <option value="Infra & Cloud">Infra & Cloud</option>
                    <option value="Autre">Autre</option>
                    <option value="Transformation Digitale">Transformation Digitale</option>
                    <option value="Marketing">Marketing</option>
                    <option value="Entrepreunariat">Entrepreunariat</option>
                    <option value="Ressources Humaines">Ressources Humaines</option>
                </select>
            </div>

            <div class="form-group">
                <label>Années depuis la dernière promotion</label>
                <input type="number" id="annees_depuis_la_derniere_promotion" required>
            </div>

            <button type="submit">PRÉDIRE</button>

        </form>

        <div id="resultat"></div>

        <script>
            document.getElementById("predictionForm").addEventListener("submit", async function(event) {

                event.preventDefault();

                const data = {
                    age: Number(document.getElementById("age").value),
                    genre: document.getElementById("genre").value,
                    revenu_mensuel: Number(document.getElementById("revenu_mensuel").value),
                    statut_marital: document.getElementById("statut_marital").value,
                    poste: document.getElementById("poste").value,
                    nombre_experiences_precedentes: Number(document.getElementById("nombre_experiences_precedentes").value),
                    annees_dans_l_entreprise: Number(document.getElementById("annees_dans_l_entreprise").value),
                    satisfaction_employee_environnement: Number(document.getElementById("satisfaction_employee_environnement").value),
                    satisfaction_employee_equipe: Number(document.getElementById("satisfaction_employee_equipe").value),
                    heure_supplementaires: document.getElementById("heure_supplementaires").value,
                    augementation_salaire_precedente: Number(document.getElementById("augementation_salaire_precedente").value),
                    nombre_participation_pee: Number(document.getElementById("nombre_participation_pee").value),
                    nb_formations_suivies: Number(document.getElementById("nb_formations_suivies").value),
                    distance_domicile_travail: Number(document.getElementById("distance_domicile_travail").value),
                    niveau_education: Number(document.getElementById("niveau_education").value),
                    domaine_etude: document.getElementById("domaine_etude").value,
                    annees_depuis_la_derniere_promotion: Number(document.getElementById("annees_depuis_la_derniere_promotion").value)
                };

                const resultat = document.getElementById("resultat");
                resultat.textContent = "Prédiction en cours...";

                try {
                    const response = await fetch("/PredictionUser", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify(data)
                    });

                    if (!response.ok) {
                        throw new Error("Erreur " + response.status);
                    }

                    const prediction = await response.json();

                    resultat.innerHTML = `
                        <p>Probabilité de rester : ${prediction[0].STAY}</p>
                        <p>Probabilité de partir : ${prediction[0].LEAVE}</p>
                    `;

                } catch (error) {
                    resultat.textContent = "Une erreur est survenue : " + error.message;
                }
            });
        </script>

    </body>
    </html>
    """