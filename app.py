
import os
from flask import Flask, jsonify, render_template_string
import psycopg

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GC Manager</title>
<style>
body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f1f5f9;
    color: #172554;
}
header {
    background: #12345a;
    color: white;
    padding: 25px;
}
main { padding: 30px; }
.card {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 3px 12px #0001;
}
h1 { margin: 0; }
</style>
</head>
<body>
<header>
<h1>GC MANAGER</h1>
<p>Gestion de sous-traitance en génie civil</p>
</header>
<main>
<div class="card">
<h2>Tableau de bord</h2>
<p>Bienvenue dans votre plateforme de gestion.</p>
<p>Activités : Terrassement, Assainissement, Chaussée.</p>
<p id="status">Vérification du serveur...</p>
</div>
</main>
<script>
fetch('/health')
.then(r => r.json())
.then(d => {
document.getElementById('status').textContent =
d.database ? 'Serveur et base de données connectés' :
'Serveur actif - base de données à configurer';
})
.catch(() => {
document.getElementById('status').textContent =
'Serveur actif';
});
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/health")
def health():
    if not DATABASE_URL:
        return jsonify(database=False), 200

    try:
        with psycopg.connect(DATABASE_URL, connect_timeout=5) as conn:
            conn.execute("SELECT 1")
        return jsonify(database=True), 200
    except Exception:
        return jsonify(database=False), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
