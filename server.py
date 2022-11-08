from flask import Flask, render_template, request, session
from cidade import ApiCidade
from passagem import ApiPassagem
from hospedagem import ApiHospedagem
from atracao import ApiAtracao
from models import Cidade, Passagem, Hospedagem, Atracao
import datetime

import pandas as pd
import json
import plotly
import plotly.express as px

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template('Home.html')

@app.route("/passagem", methods=["POST"])
def get_response():
    session["origem"] = request.form.get('origem')
    session["destino"] = request.form.get('destino')
    session["passageiros"] = request.form.get('passageiros')
    session["data_ida"] = request.form.get('data_ida')
    session["data_volta"] = request.form.get('data_volta')

    #API CIDADE    
    print("########## EXECUTANDO API CIDADE ##########\n")
    dict_origem = ApiCidade.get_location(session["origem"])
    dict_destino = ApiCidade.get_location(session["destino"])
    session["location_destino"] = dict_destino["location_id"]

    cidade = Cidade.criaCidade(dict_origem) #ARMAZENA NO BANCO

    #API VOO
    print("########## EXECUTANDO API VOO ##########\n")
    dict_ida = ApiPassagem.get_passagem(session['data_ida'], session['passageiros'], dict_origem['aero_code'], dict_destino['aero_code'])
    dict_volta = ApiPassagem.get_passagem(session['data_volta'], session['passageiros'], dict_destino['aero_code'], dict_origem['aero_code'])
    
    for i in dict_ida: #ESSE É O JEITO CERTO???
        passagem = Passagem.criaPassagem(i) #ARMAZENA NO BANCO

    dict_voos = {
        "ida": dict_ida,
        "volta": dict_volta,
    }
    
    return render_template('Passagem.html', content = dict_voos)

@app.route("/hospedagem", methods=["POST"])
def get_hotel():
    session["voo_ida"] = request.form.get('voo_ida')
    session["voo_volta"] = request.form.get('voo_volta')

    data_ida = datetime.datetime.strptime(session["data_ida"], "%Y-%m-%d").date()
    data_volta = datetime.datetime.strptime(session["data_volta"], "%Y-%m-%d").date()
    noites = (data_volta - data_ida).days

    #API HOTEL
    print("########## EXECUTANDO API HOTEL ##########\n")
    dict_hoteis = ApiHospedagem.get_hotels(session["location_destino"], session["passageiros"], session["data_ida"], noites) 
    for i in dict_hoteis: #ESSE É O JEITO CERTO???
        hospedagem = Hospedagem.criaHospedagem(i) #ARMAZENAR NO BANCO
    
    return render_template('Hospedagem.html', content = dict_hoteis)

@app.route("/pacote", methods=["POST"])
def fechando_pacote():
    hotel = request.form.get('hotel')
    hotel = eval(hotel)
    ida = eval(session['voo_ida'])
    volta = eval(session['voo_volta'])

    #API ATRAÇÃO 
    print("########## EXECUTANDO API ATRACAO ##########\n")
    dict_atracoes = ApiAtracao.get_atracao(session['location_destino'])
    for i in dict_atracoes: #ESSE É O JEITO CERTO???
        atracao = Atracao.criaAtracao(i)#ARMAZENAR NO BANCO
     
    data_ida = datetime.datetime.strptime(session["data_ida"], "%Y-%m-%d").date()
    data_volta = datetime.datetime.strptime(session["data_volta"], "%Y-%m-%d").date()
    noites = (data_volta - data_ida).days

    dict_pacote = {
        'hotel': hotel,
        'ida': ida,
        'volta': volta,
        'passageiros': session["passageiros"],
        'noites': noites,
        'atracoes': dict_atracoes
    }

    #PACOTE TURISTICO
    print("########## FECHANDO PACOTE ##########\n") #ARMAZENAR NO BANCO
    return render_template('Pacote.html', content = dict_pacote)

@app.route("/filtros", methods=["GET"])
def get_filtro():
    _dict = {
        "cidade":["São Paulo", "Porto Alegre", "Belo Horizonte", "Manaus", "Rio de Janeiro"],
    }

    return render_template('Filtros.html', content =_dict)

@app.route("/relatorio", methods=["POST"])
def gerar_relatorio():
    cidade1 = request.form.get('cidade1')
    cidade2 = request.form.get('cidade2')
    
    df = pd.DataFrame({
        'cidade': [cidade1, cidade2],
        'Amount': [4, 5],
        'City': [cidade1, cidade2]
    })

    #GERAR RELATORIO
    print("########## GERANDO RELATORIO ##########\n")
    fig = px.bar(df, x='cidade', y='Amount', color='City', barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('Relatorio.html', graphJSON=graphJSON)

if __name__ == "__main__":
    app.secret_key = 'key'
    app.run()