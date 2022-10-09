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
    voo_ida = request.form.get('voo_ida')
    voo_volta = request.form.get('voo_volta')
    
    session["voo_ida"] = voo_ida
    session["voo_volta"] = voo_volta

    print("########## EXECUTANDO API HOTEL ##########\n")
    dict_hoteis = Hospedagem.get_hotels(session["location_destino"], session["passageiros"], session["data_ida"], session["data_volta"]) #ARMAZENAR NO BANCO
    
    return render_template('Hospedagem.html', content = dict_hoteis)

@app.route("/pacote", methods=["POST"])
def fechando_pacote():
    hotel = request.form.get('hotel')
    hotel = ast.literal_eval(hotel)
    ida = ast.literal_eval(session['voo_ida'])
    volta = ast.literal_eval(session['voo_volta'])

    dict_pacote = {
        "hotel": hotel,
        "ida": ida,
        "volta": volta
    }
    print(dict_pacote)
    return render_template('Pacote.html', content = dict_pacote)

if __name__ == "__main__":
    app.secret_key = 'key'
    app.run()


{'hotel': "{'nome': 'Hotel Deville Prime Porto Alegre', 'preco': 'R$428 - R$595', 'foto': 'https://media-cdn.tripadvisor.com/media/photo-l/1c/4e/00/61/hotel-deville-prime-porto.jpg', 'avaliacao': '4.5527544021606445', 'estrelas': '4.0', 'endereco': 'Avenida dos Estados 1909 Anchieta, Porto Alegre, State of Rio Grande do Sul 90200-001 Brazil'}",
 'ida': "{'origem': 'Belo Horizonte', 'destino': 'Porto Alegre', 'aero_origem': 'CNF', 'aero_destino': 'POA', 'preco': 1004.02, 'duracao': '00:03:55', 'qtde_conn': 1, 'empresa': 'LATAM Airlines', 'dt_partida': '2022-10-14T05:15:00', 'dt_chegada': '2022-10-14T09:10:00'}",
 'volta': "{'origem': 'Porto Alegre', 'destino': 'Belo Horizonte', 'aero_origem': 'POA', 'aero_destino': 'CNF', 'preco': 640.16, 'duracao': '00:07:20', 'qtde_conn': 1, 'empresa': 'LATAM Airlines', 'dt_partida': '2022-10-19T06:15:00', 'dt_chegada': '2022-10-19T13:35:00'}"}