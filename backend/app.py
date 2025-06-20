from flask import Flask
from backend.controlador.rutas import rutas
import os

app = Flask(__name__, template_folder='../frontend/plantillas', static_folder='../frontend/estaticos')
app.register_blueprint(rutas)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 