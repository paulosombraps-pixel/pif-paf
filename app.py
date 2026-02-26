from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

jogadores = []

HTML = """
<!doctype html>
<html>
<head>
    <title>Jogo de Pontuação</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="font-family: Arial; text-align: center; background: #0b3d0b; color: white;">

<h2>Jogo de Pontuação</h2>

<form method="post" action="/add">
    <input name="nome" placeholder="Nome do jogador" required>
    <button type="submit">Adicionar</button>
</form>

<br>

{% for jogador in jogadores %}
    <div style="margin:10px; padding:10px; border:1px solid white;">
        <h3>{{ jogador.nome }} - {{ jogador.pontos }} pontos</h3>

        {% for v in range(1,6) %}
            <a href="/jogar/{{ jogador.nome }}/{{ v }}">
                <button>{{ v }}</button>
            </a>
        {% endfor %}
    </div>
{% endfor %}

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML, jogadores=jogadores)

@app.route("/add", methods=["POST"])
def add():
    nome = request.form["nome"]
    jogadores.append({"nome": nome, "pontos": 0})
    return redirect("/")

@app.route("/jogar/<nome>/<int:valor>")
def jogar(nome, valor):
    total_ganho = 0

    for jogador in jogadores:
        if jogador["nome"] != nome:
            jogador["pontos"] -= valor
            total_ganho += valor

    for jogador in jogadores:
        if jogador["nome"] == nome:
            jogador["pontos"] += total_ganho

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

