from datetime import date, datetime
import requests 
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
api_base_url = "http://localhost:8000"


def converter_data(data_str):
    return datetime.strptime(data_str, "%Y-%m-%d").date().strftime("%d/%m/%Y")

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/listar')
def listar():
    viajantes = requests.get(f"{api_base_url}/viajantes").json()
    viagens = requests.get(f"{api_base_url}/viagens").json()
    pedidos = requests.get(f"{api_base_url}/pedidos").json()
    
    for viagem in viagens:
        viagem['data_partida'] = converter_data(viagem['data_partida'])

    for pedido in pedidos:
        viajante = requests.get(f"{api_base_url}/viajantes/{pedido['id_viajante']}").json()
        pedido['viajante'] = viajante
    return render_template('listar.html', viajantes=viajantes, viagens=viagens, pedidos=pedidos)

@app.route('/viajante/<int:id>')
def viajante(id):
    viajante = requests.get(f"{api_base_url}/viajantes/{id}").json()
    marcacoes = requests.get(f"{api_base_url}/marcacoes?viajante_id={id}").json()
    marcacoes_viagens = []
    for marcacao in marcacoes:
        viagem = requests.get(f"{api_base_url}/viagens/{marcacao['id_viagem']}").json()
        marcacoes_viagens.append(viagem)
    # converter data para formato mais legível
    viajante['data_nasc'] = converter_data(viajante['data_nasc'])
    return render_template('viajante.html', viajante=viajante, marcacoes=marcacoes_viagens)

@app.route('/viagem/<int:id>')
def viagem(id):
    viagem = requests.get(f"{api_base_url}/viagens/{id}").json()
    restricoes = requests.get(f"{api_base_url}/viagens/{id}/restricoes").json()
    marcacoes = requests.get(f"{api_base_url}/marcacoes?viagem_id={id}").json()

    marcacoes_viajantes = []
    for marcacao in marcacoes:
        viajante = requests.get(f"{api_base_url}/viajantes/{marcacao['id_viajante']}").json()
        marcacoes_viajantes.append(viajante)

    # converter data para formato mais legível
    viagem['data_partida'] = converter_data(viagem['data_partida'])
    return render_template("viagem.html", viagem=viagem, restricoes=restricoes, viajantes=marcacoes_viajantes)

@app.route('/pedido/<int:id>')
def pedido(id):
    pedido = requests.get(f"{api_base_url}/pedidos/{id}").json()
    pedido["viajante"] = requests.get(f"{api_base_url}/viajantes/{pedido['id_viajante']}").json()
    pedido["data_pedido"] = converter_data(pedido["data_pedido"])
    return render_template("pedido.html", pedido=pedido)

@app.route('/gerir', methods=['GET', 'POST'])
def gerir():

    if request.method == 'POST':
        acao = request.form.get('acao')
        id_viajante = request.form.get('id')


        if acao == 'apagar':
            requests.delete(f"{api_base_url}/viajantes/{id_viajante}")

        elif acao == 'editar':
            dados = {
                "nome": request.form.get('nome'),
                "email": request.form.get('email'),
                "data_nasc": request.form.get('data_nasc')
            }
            requests.put(f"{api_base_url}/viajantes/{id_viajante}", json=dados)
        return redirect(url_for('gerir'))

 
    req = requests.get(f"{api_base_url}/viajantes")
    viajantes = req.json()
    for v in viajantes:
        v['data_nasc2'] = v['data_nasc'] # manter data original para envio à API
        v['data_nasc'] = converter_data(v['data_nasc'])
    return render_template("gerir.html", viajantes=viajantes)



@app.route('/marcar', methods=['GET', 'POST'])
def marcar():
    if request.method == 'POST':
        id_viajante = request.form.get('viajante')
        id_viagem = request.form.get('viagem')
        data_marcacao = datetime.now().date().strftime("%Y-%m-%d")  
    

        nova_marcacao = {
            "id_viajante": id_viajante,
            "id_viagem": id_viagem,
            "data_marcacao": data_marcacao
        }
        requests.post(f"{api_base_url}/marcacoes", json=nova_marcacao)
        
        return redirect(url_for('marcar'))

    req2 = requests.get(f"{api_base_url}/viajantes")
    viajantes = req2.json()

    req_v = requests.get(f"{api_base_url}/viajantes")
    viajantes = req_v.json()

    req_vi = requests.get(f"{api_base_url}/viagens")
    viagens = req_vi.json()

    for viagem in viagens:
        viagem['data_partida'] = converter_data(viagem['data_partida'])

    return render_template('marcar.html', viajantes=viajantes, viagens=viagens)
@app.route('/pedir_viagem', methods=['POST'])
def pedir_viagem():
    id_viajante = request.form.get('viajante')
    destino = request.form.get('destino')

    pedido = {
        "id_viajante": id_viajante,
        "destino_temporal": destino
    }
    requests.post(f"{api_base_url}/pedidos", json=pedido)

    return redirect(url_for('marcar'))


@app.route('/registar', methods=['GET', 'POST'])
def registar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        data_nasc = request.form['data_nasc']

        novo_viajante = {
            "nome": nome,
            "email": email,
            "data_nasc": data_nasc
        }
        req = requests.post(f"{api_base_url}/viajantes", json=novo_viajante)
        
        
        return redirect(url_for('viajante', id=req.json()['id']))
    return render_template('registar.html')

if __name__ == '__main__':
    app.run(debug=True)