from flask import Flask, render_template, request, session
from cidade import Cidade
from passagem import Passagem
from hospedagem import Hospedagem
from atracao import Atracao
import datetime

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
    dict_origem = Cidade.get_location(session["origem"]) #ARMAZENAR NO BANCO
    dict_destino = Cidade.get_location(session["destino"]) #ARMAZENAR NO BANCO
    session["location_destino"] = dict_destino["location_id"]

    #API VOO
    print("########## EXECUTANDO API VOO ##########\n")
    dict_ida = Passagem.get_passagem(session['data_ida'], session['passageiros'], dict_origem['aero_code'], dict_destino['aero_code']) #ARMAZENAR NO BANCO
    dict_volta = Passagem.get_passagem(session['data_volta'], session['passageiros'], dict_destino['aero_code'], dict_origem['aero_code']) #ARMAZENAR NO BANCO

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

    print("########## EXECUTANDO API HOTEL ##########\n")
    dict_hoteis = Hospedagem.get_hotels(session["location_destino"], session["passageiros"], session["data_ida"], noites) #ARMAZENAR NO BANCO
    
    return render_template('Hospedagem.html', content = dict_hoteis)

@app.route("/pacote", methods=["POST"])
def fechando_pacote():
    hotel = request.form.get('hotel')
    hotel = eval(hotel)
    ida = eval(session['voo_ida'])
    volta = eval(session['voo_volta'])

    print("########## EXECUTANDO API ATRACAO ##########\n")
    dict_atracoes = Atracao.get_atracao(session['location_destino']) #ARMAZENAR NO BANCO
    print()
    print(dict_atracoes)
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

    print("########## FECHANDO PACOTE ##########\n") #ARMAZENAR NO BANCO
    return render_template('Pacote.html', content = dict_pacote)

if __name__ == "__main__":
    app.secret_key = 'key'
    app.run()