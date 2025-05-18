from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Ruta al JSON relativa al archivo actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "videojuegos.json")

with open(json_path, encoding="utf-8") as f:
    videojuegos = json.load(f)

generos = sorted(set(j["genero"] for j in videojuegos))

@app.route('/')
def home():
    return render_template("inicio.html")

@app.route('/buscador')
def buscador():
    return render_template("buscador.html", generos=generos)

@app.route('/lista', methods=['POST'])
def lista():
    query = request.form.get('query', '').strip().lower()
    genero = request.form.get('genero', '').strip()

    # Filtrar por título si se introduce
    resultados = [
        juego for juego in videojuegos
        if (query == "" or juego["titulo"].lower().startswith(query)) and
           (genero == "" or juego["genero"] == genero)
    ]

    return render_template("lista.html", resultados=resultados)

@app.route('/detalles/<int:videojuego_id>')
def detalles(videojuego_id):
    juego = next((j for j in videojuegos if j["id"] == videojuego_id), None)
    if not juego:
        return "Juego no encontrado", 404
    return render_template("detalles.html", juego=juego)

if __name__ == '__main__':
    app.run(debug=True)
