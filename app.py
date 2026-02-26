from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

nomes = []
pontos = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/jogar", methods=["POST"])
def jogar():
    data = request.get_json()
    jogador = data["jogador"]
    valor = data["valor"]

    if jogador >= 0:
        total_ganho = valor * (len(pontos)-1)
        for i in range(len(pontos)):
            if i != jogador:
                pontos[i] = max(0, pontos[i]-valor)  # não deixa negativo
        pontos[jogador] += total_ganho

    return jsonify({"nomes": nomes, "pontos": pontos})

@app.route("/add_jogador", methods=["POST"])
def add_jogador():
    data = request.get_json()
    nome = data["nome"].strip()
    if any(n.lower() == nome.lower() for n in nomes):
        return jsonify({"nomes": nomes, "pontos": pontos})
    nomes.append(nome)
    pontos.append(0)
    return jsonify({"nomes": nomes, "pontos": pontos})

@app.route("/remover_jogador", methods=["POST"])
def remover_jogador():
    data = request.get_json()
    index = data["index"]
    nomes.pop(index)
    pontos.pop(index)
    return jsonify({"nomes": nomes, "pontos": pontos})

@app.route("/reset", methods=["POST"])
def reset():
    global pontos
    pontos = [0]*len(pontos)
    return jsonify({"nomes": nomes, "pontos": pontos})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
