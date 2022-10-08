from flask import Flask, render_template, request, session
from cidade import Cidade
from passagem import Passagem
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

    #API VOO
    print("\n########## EXECUTANDO API VOO ##########")
    dict_ida = Passagem.get_passagem(session['data_ida'], session['passageiros'], dict_origem['aero_code'], dict_destino['aero_code']) #ARMAZENAR NO BANCO
    dict_volta = Passagem.get_passagem(session['data_volta'], session['passageiros'], dict_destino['aero_code'], dict_origem['aero_code']) #ARMAZENAR NO BANCO

    voos = {
        "ida": dict_ida,
        "volta": dict_volta,
    }
    
    return render_template('Passagem.html', content = voos)

@app.route("/hospedagem", methods=["POST"])
def get_hotel():
    voo_ida = request.form.get('voo_ida')
    voo_volta = request.form.get('voo_volta')

    print(voo_ida, voo_volta)
    
    return 'oi'

if __name__ == "__main__":
    app.secret_key = 'key'
    app.run()