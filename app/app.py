from flask import Flask, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, template_folder="templates")
CORS(app)

# Correction du chemin vers la base de données
DB_PATH = os.getenv("DB_PATH", "metrics.db")

def fetch_metrics():
    """Récupère les métriques de la base de données SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, cpu_usage, ram_usage FROM metrics ORDER BY timestamp DESC LIMIT 100")
        rows = cursor.fetchall()
        conn.close()

        # Correction des indices pour retourner les bonnes colonnes
        return [{"timestamp": row[0], "cpu": row[1], "ram": row[2]} for row in rows]
    except Exception as e:
        print(f"Erreur lors de la récupération des métriques : {e}")
        return []

@app.route('/')
def index():
    """Route principale : affiche le tableau de bord."""
    return render_template('index.html')

@app.route('/api/metrics', methods=['GET'])
def metrics():
    """Route pour récupérer les métriques."""
    data = fetch_metrics()
    return jsonify({
        "timestamps": [row["timestamp"] for row in data],
        "cpu": {"values": [row["cpu"] for row in data]},
        "ram": {"values": [row["ram"] for row in data]}
    })

if __name__ == '__main__':
    # Correction pour s'assurer que l'application Flask utilise le bon port
    port = int(os.getenv("FLASK_PORT", 5001))
    app.run(debug=True, host='0.0.0.0', port=port)

