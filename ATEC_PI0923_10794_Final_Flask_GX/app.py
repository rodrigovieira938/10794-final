from datetime import date, datetime

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


viajantes = [
    {
        "id": 1,
        "nome": "Ana Silva",
        "email": "ana@example.com",
        "data_nasc": date(1990, 5, 14)
    },
    {
        "id": 2,
        "nome": "Bruno Costa",
        "email": "bruno@example.com",
        "data_nasc": date(1985, 8, 22)
    },
    {
        "id": 3,
        "nome": "Carla Mendes",
        "email": "carla@example.com",
        "data_nasc": date(2000, 1, 10)
    },
    {
        "id": 4,
        "nome": "Diogo Rocha",
        "email": "diogo@example.com",
        "data_nasc": date(1978, 12, 3)
    },
]

viagens = [
    {
        "id": 1,
        "destino_temporal": "Roma Antiga - 50 a.C.",
        "data_partida": date(2026, 6, 1),
        "duracao_dias": 7,
        "max_viajantes": 10
    },
    {
        "id": 2,
        "destino_temporal": "Egito - Construção das Pirâmides",
        "data_partida": date(2026, 7, 15),
        "duracao_dias": 10,
        "max_viajantes": 8
    },
    {
        "id": 3,
        "destino_temporal": "Futuro - Marte 2150",
        "data_partida": date(2026, 9, 10),
        "duracao_dias": 5,
        "max_viajantes": 5
    },
]

reservas = [
    {
        "id": 1,
        "id_viajante": 1,
        "id_viagem": 1,
        "data_marcacao": date(2026, 1, 10)
    },
    {
        "id": 2,
        "id_viajante": 2,
        "id_viagem": 1,
        "data_marcacao": date(2026, 1, 12)
    },
    {
        "id": 3,
        "id_viajante": 3,
        "id_viagem": 2,
        "data_marcacao": date(2026, 2, 5)
    },
    {
        "id": 4,
        "id_viajante": 1,
        "id_viagem": 3,
        "data_marcacao": date(2026, 3, 1)
    },
]

restricoes = [
    {
        "id_viagem": 1,
        "idade_minima": 18,
        "idade_maxima": 60,
        "proibicao_interac_eventos": True,
        "requisitos": "Não alterar eventos históricos"
    },
    {
        "id_viagem": 2,
        "idade_minima": 21,
        "idade_maxima": None,
        "proibicao_interac_eventos": True,
        "requisitos": "Uso obrigatório de traje adequado"
    },
    {
        "id_viagem": 3,
        "idade_minima": 25,
        "idade_maxima": 55,
        "proibicao_interac_eventos": False,
        "requisitos": "Treino físico obrigatório"
    },
]



@app.route('/')
def home():
    return render_template('base.html')

@app.route('/listar')
def listar():
    return render_template('listar.html', viajantes=viajantes, viagens=viagens, reservas=reservas, restricoes=restricoes)

@app.route('/consultar')
def consultar():
    return render_template('consultar.html', reservas=reservas, viajantes=viajantes, viagens=viagens)

@app.route('/gerir',methods=['GET', 'POST'])
def gerir():
    return render_template('gerir.html', viajantes = viajantes, viagens = viagens, reservas = reservas, restricoes = restricoes)

pedidos = []

@app.route('/marcar', methods=['GET', 'POST'])
def marcar():
    if request.method == 'POST':
        tipo = request.form['tipo']
        id_viajante = int(request.form['viajante'])

        if tipo == "existente":
            id_viagem = int(request.form['viagem'])

            nova_reserva = {
                "id": len(reservas) + 1,
                "id_viajante": id_viajante,
                "id_viagem": id_viagem,
                "data_marcacao": date.today()
            }
            reservas.append(nova_reserva)

        elif tipo == "pedido":
            destino = request.form['destino_pedido']
            data_p = request.form['data_pedido']

            novo_pedido = {
                "id": len(pedidos) + 1,
                "id_viajante": id_viajante,
                "destino": destino,
                "data_desejada": date.fromisoformat(data_p),
                "data_pedido": date.today()
            }
            pedidos.append(novo_pedido)

        return redirect(url_for('consultar'))

    return render_template('marcar.html', viajantes=viajantes, viagens=viagens)



@app.route('/registar', methods=['GET', 'POST'])
def registar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        data_nasc = request.form['data_nasc']
        
        return redirect(url_for('listar'))
    return render_template('registar.html')

if __name__ == '__main__':
    app.run(debug=True)
