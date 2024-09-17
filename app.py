from flask import Flask
from flask_cors import CORS
import os
from project.routes.routes import register_routes
from flask import send_from_directory

app = Flask(__name__)
CORS(app)  # Isso habilita o CORS para permitir requisições de outros domínios

app.secret_key = os.urandom(24)  # Gera uma chave secreta aleatória

@app.route('/assets/<path:filename>')
def custom_static(filename):
    return send_from_directory('assets', filename)

# Registra as rotas a partir do arquivo routes.py
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
