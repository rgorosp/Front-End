import json
import threading
import webbrowser
from pathlib import Path

from flask import Flask, jsonify, redirect, request, send_from_directory, url_for


app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_CARROS = BASE_DIR / "carros.json"
STATUS_VALIDOS = {"Disponível", "Reservado", "Vendido"}
CARROS_INICIAIS = [
	{"modelo": "Honda Civic EXL", "ano": 2020, "quilometragem": "48.000 km", "preco": "R$ 119.900", "status": "Disponível"},
	{"modelo": "Volkswagen T-Cross", "ano": 2021, "quilometragem": "37.500 km", "preco": "R$ 109.900", "status": "Disponível"},
	{"modelo": "Chevrolet Onix LT", "ano": 2022, "quilometragem": "29.000 km", "preco": "R$ 78.900", "status": "Reservado"},
	{"modelo": "Jeep Renegade Longitude", "ano": 2020, "quilometragem": "55.000 km", "preco": "R$ 104.900", "status": "Vendido"},
]


def carregar_carros():
	if not ARQUIVO_CARROS.exists():
		return CARROS_INICIAIS.copy()

	try:
		with ARQUIVO_CARROS.open("r", encoding="utf-8") as arquivo:
			dados = json.load(arquivo)
		return dados if isinstance(dados, list) else CARROS_INICIAIS.copy()
	except (json.JSONDecodeError, OSError):
		return CARROS_INICIAIS.copy()


def salvar_carros(carros):
	with ARQUIVO_CARROS.open("w", encoding="utf-8") as arquivo:
		json.dump(carros, arquivo, ensure_ascii=False, indent=2)


@app.get("/")
def index():
	return send_from_directory(BASE_DIR, "index.html")


@app.get("/api/carros")
def listar_carros():
	return jsonify(carregar_carros())


@app.post("/carros")
def cadastrar_carro():
	formulario = request.form
	modelo = formulario.get("modelo", "").strip()
	ano_texto = formulario.get("ano", "").strip()
	quilometragem = formulario.get("quilometragem", "").strip()
	preco = formulario.get("preco", "").strip()
	status = formulario.get("status", "").strip()

	try:
		ano = int(ano_texto)
	except ValueError:
		return "Ano inválido.", 400

	if not modelo or not quilometragem or not preco:
		return "Preencha todos os campos.", 400
	if not 1900 <= ano <= 2100:
		return "Ano inválido.", 400
	if status not in STATUS_VALIDOS:
		return "Status inválido.", 400

	carros = carregar_carros()
	carros.append({
		"modelo": modelo,
		"ano": ano,
		"quilometragem": quilometragem,
		"preco": preco,
		"status": status,
	})
	salvar_carros(carros)
	return redirect(url_for("index"))


if __name__ == "__main__":
	threading.Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000/")).start()
	app.run(debug=False, use_reloader=False)
