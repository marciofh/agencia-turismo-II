from flask import Flask, render_template, request, session
from cidade import Cidade
from passagem import Passagem
from hospedagem import Hospedagem
import ast

app = Flask(__name__)

@app.route("/")
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
    print("########## EXECUTANDO API CIDADE ##########")
    dict_origem = Cidade.get_location(session["origem"]) #ARMAZENAR NO BANCO
    dict_destino = Cidade.get_location(session["destino"]) #ARMAZENAR NO BANCO
    session["location_destino"] = dict_destino["location_id"]

    #API VOO
    print("\n########## EXECUTANDO API VOO ##########")
    dict_ida = Passagem.get_passagem(session['data_ida'], session['passageiros'], dict_origem['aero_code'], dict_destino['aero_code']) #ARMAZENAR NO BANCO
    dict_volta = Passagem.get_passagem(session['data_volta'], session['passageiros'], dict_destino['aero_code'], dict_origem['aero_code']) #ARMAZENAR NO BANCO

    dict_voos = {
        "ida": dict_ida,
        "volta": dict_volta,
    }
    
    return render_template('Passagem.html', content = dict_voos)

@app.route("/hospedagem", methods=["POST"])
def get_hotel():
    voo_ida = request.form.get('voo_ida')
    voo_volta = request.form.get('voo_volta')
    
    session["voos"] = {
        "ida": voo_ida,
        "volta": voo_volta
    }

    dict_hoteis = Hospedagem.get_hotels(session["location_destino"], session["passageiros"], session["data_ida"], session["data_volta"]) #ARMAZENAR NO BANCO
    
    return render_template('Hospedagem.html', content = dict_hoteis)

@app.route("/pacote", methods=["POST"])
def fechando_pacote():
    hotel = request.form.get('hotel')

    dict_pacote = {
        "hotel": hotel,
        "voos": session['voos']
    }
    return render_template('Pacote.html', content = dict_pacote)


if __name__ == "__main__":
    app.secret_key = 'key'
    app.run()