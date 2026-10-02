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
            <label>Identifiant de l'employé</label>
            <div class="attendu">Attendu : str (id_employee présent dans la base)</div>
            <input type="text" id="id_employee" required>
        </div>

        <button type="submit">PRÉDIRE</button>

    </form>

    <div id="resultat"></div>

    <script>
        document.getElementById("predictionForm").addEventListener(
            "submit",
            async function(event) {

                event.preventDefault();

                const id = document.getElementById("id_employee").value;
                const resultat = document.getElementById("resultat");

                resultat.style.color = "";
                resultat.textContent = "Prédiction en cours...";

                try {

                    const response = await fetch(
                        "/PredictionUser?id_employee=" + encodeURIComponent(id),
                        { method: "POST" }
                    );

                    if (response.status === 404 || response.status === 500) {
                        throw new Error(
                            "Employé introuvable : cet identifiant n'existe pas dans la base."
                        );
                    }

                    if (!response.ok) {
                        let detail = "";
                        try {
                            const err = await response.json();
                            detail = " - " + JSON.stringify(err.detail);
                        } catch (e) {}
                        throw new Error("Erreur " + response.status + detail);
                    }

                    const reponse = await response.json();
                    const prediction = Array.isArray(reponse) ? reponse[0] : reponse;

                    resultat.innerHTML = `
                        <p>Prédiction : ${prediction.prediction}</p>

                        <p>Probabilité de rester :
                        ${prediction.STAY}</p>

                        <p>Probabilité de partir :
                        ${prediction.LEAVE}</p>
                    `;

                } catch (error) {

                    resultat.style.color = "#c0392b";
                    resultat.textContent = error.message;

                }
            }
        );
    </script>

</body>
</html>
""")