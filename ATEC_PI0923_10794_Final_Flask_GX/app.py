from datetime import date, datetime
import requests 
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
api_base_url = "http://localhost:8000"



@app.route('/')
def home():
    return render_template('base.html')

@app.route('/listar')
def listar():
    resp = requests.get(f"{api_base_url}/viajantes")
    viajantes_api = resp.json()

    
    lista = []
    for v in viajantes_api:
        lista.append({
            "nome": v["nome"],
            "email": v["email"]
        })

    resp_viagens = requests.get(f"{api_base_url}/viagens")
    viagens = resp_viagens.json()

    resp_reservas = requests.get(f"{api_base_url}/marcacoes")
    reservas = resp_reservas.json()

    restricoes = []
    for viagem in viagens:
        resp_r = requests.get(f"{api_base_url}/viagens/{viagem['id']}/restricoes")
        if resp_r.ok:
            restricoes.extend(resp_r.json())

    return render_template('listar.html', viajantes=lista, viagens=viagens, reservas=reservas, restricoes=restricoes)

@app.route('/consultar')
def consultar():
    resp1 = requests.get(f"{api_base_url}/viajantes")
    viajantes_api = resp1.json()
    viajantes_display = []
    for v in viajantes_api:
        viajantes_display.append({
            "nome": v["nome"],
            "email": v["email"]
        })

    resp2 = requests.get(f"{api_base_url}/viagens")
    viagens = resp2.json()

    resp3 = requests.get(f"{api_base_url}/marcacoes")
    reservas = resp3.json()

    return render_template('consultar.html', reservas=reservas, viajantes=viajantes_api, viagens=viagens, viajantes_display=viajantes_display)

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

 
    req = requests.get(f"{api_base_url}/viajantes")
    viajantes = req.json()

    return render_template("gerir.html", viajantes=viajantes)



@app.route('/marcar', methods=['GET', 'POST'])
def marcar():
    id_viajante = request.form.get('viajante')
    id_viagem = request.form.get('viagem')
    data_marcacao = datetime.now().date().strftime("%Y-%m-%d")  
    

    nova_marcacao = {
        "id_viajante": id_viajante,
        "id_viagem": id_viagem,
        "data_marcacao": data_marcacao
    }
    print(nova_marcacao)
    req = requests.post(f"{api_base_url}/marcacoes", json=nova_marcacao)
    
    req2 = requests.get(f"{api_base_url}/viajantes")
    viajantes = req2.json()

    req_v = requests.get(f"{api_base_url}/viajantes")
    viajantes = req_v.json()

    req_vi = requests.get(f"{api_base_url}/viagens")
    viagens = req_vi.json()
    return render_template('marcar.html', viajantes=viajantes, viagens=viagens)



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
        
        
        return redirect(url_for('listar'))
    return render_template('registar.html')

if __name__ == '__main__':
    app.run(debug=True)