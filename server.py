from flask import Flask, render_template, request, session
import plotly.express as px
import pandas as pd
import datetime
import plotly
import json

from cidade import ApiCidade
from atracao import ApiAtracao
from passagem import ApiPassagem
from hospedagem import ApiHospedagem
from models import Cidade, Passagem, Hospedagem, Atracao, Pacote

#CADASTRAR CIDADE ORIGEM E DESTINO
#TODA CIDADE TEM HOTEL E ATRAÇÃO
#NEM TODA CIDADE TEM PASSAGEM
#CONSULTAR DE PACOTE EXISTE ?

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

    #procura se a cidade de origem existe no banco de dados

    #if not cidade:
    #API CIDADE    
    print("########## EXECUTANDO API CIDADE ##########\n")
    dict_origem = ApiCidade.get_location(session["origem"])
    dict_destino = ApiCidade.get_location(session["destino"])
    session["origem"] = dict_origem
    session["destino"] = dict_destino
    
    #cidade de origem
    cidade = Cidade.criaCidade(dict_origem) 
    Cidade.cadastraCidade(cidade) #ARMAZENA NO BANCO

    #ciade de destino
    cidade = Cidade.criaCidade(dict_destino) 
    Cidade.cadastraCidade(cidade) #ARMAZENA NO BANCO

    #procura se tem passagem de ida e volta

    #if not passagem:
    #API VOO
    print("\n########## EXECUTANDO API VOO ##########\n")
    dict_ida = ApiPassagem.get_passagem(session['data_ida'], session['passageiros'], dict_origem['aero_code'], dict_destino['aero_code'])
    dict_volta = ApiPassagem.get_passagem(session['data_volta'], session['passageiros'], dict_destino['aero_code'], dict_origem['aero_code'])
    
    lista_passagens = []
    #passagem de ida
    for passagem in dict_ida:
         lista_passagens.append(Passagem.criaPassagem(passagem, dict_origem['location_id'], dict_destino['location_id'])) 
    Passagem.cadastraPassagens(lista_passagens) #ARMAZENA NO BANCO
    
    lista_passagens.clear() 
    #passagem de volta
    for passagem in dict_volta:
         lista_passagens.append(Passagem.criaPassagem(passagem, dict_destino['location_id'], dict_origem['location_id'])) 
    Passagem.cadastraPassagens(lista_passagens) #ARMAZENA NO BANCO

    dict_voos = {
        "ida": dict_ida,
        "volta": dict_volta,
        "origem": dict_origem,
        "destino": dict_destino,
    }
    
    return render_template('Passagem.html', content = dict_voos)

@app.route("/hospedagem", methods=["POST"])
def get_hotel():
    session["voo_ida"] = request.form.get('voo_ida')
    session["voo_volta"] = request.form.get('voo_volta')

    data_ida = datetime.datetime.strptime(session["data_ida"], "%Y-%m-%d").date()
    data_volta = datetime.datetime.strptime(session["data_volta"], "%Y-%m-%d").date()
    session['noites'] = (data_volta - data_ida).days
    
    #if not cidade:
    #API HOTEL
    print("########## EXECUTANDO API HOTEL ##########\n")
    dict_hoteis = ApiHospedagem.get_hotels(session["destino"]["location_id"], session["passageiros"], session["data_ida"], session['noites']) 
    
    lista_hospedagens = []
    for hospedagem in dict_hoteis:
        lista_hospedagens.append(Hospedagem.criaHospedagem(hospedagem))
    Hospedagem.cadastraHospedagens(lista_hospedagens) #ARMAZENA NO BANCO
    #cadastrar hospedagem de cidade origem
    
    return render_template('Hospedagem.html', content = dict_hoteis)

@app.route("/pacote", methods=["POST"])
def fechando_pacote():
    hotel = request.form.get('hotel')
    hotel = eval(hotel)
    ida = eval(session['voo_ida'])
    volta = eval(session['voo_volta'])
    origem = session['origem']
    destino = session['destino']

    #API ATRAÇÃO 
    print("########## EXECUTANDO API ATRACAO ##########\n")
    dict_atracoes = ApiAtracao.get_atracao(destino['location_id'])
    
    lista_atracoes = []
    for atracao in dict_atracoes:
        lista_atracoes.append(Atracao.criaAtracao(atracao))
    Atracao.cadastraAtracoes(lista_atracoes) #ARMAZENA NO BANCO

    #PACOTE TURISTICO
    print("\n########## FECHANDO PACOTE ##########\n")
    valor_pacote = round((float(ida['preco']) + float(volta['preco'])) * float(session['passageiros']) + float(hotel['preco'] * float(session['noites']))) #calcula valor pacote

    dict_pacote = {
        'hotel': hotel,
        'ida': ida,
        'volta': volta,
        'passageiros': session["passageiros"],
        'noites': session['noites'],
        'atracoes': dict_atracoes,
        'valor_pacote': valor_pacote,
        'origem': origem,
        'destino': destino
    }
    
    passagem_id_ida = Passagem.passagemSelecionada(ida) #busca id da passagem de ida
    if passagem_id_ida != 'error':
        passagem_id_ida = passagem_id_ida[0][0]

    passagem_id_volta = Passagem.passagemSelecionada(volta) #busca id da passagem de volta
    if passagem_id_volta != 'error':
        passagem_id_volta = passagem_id_volta[0][0]

    hospedagem_id = Hospedagem.hospedagemSelecionada(hotel) #busca id da hospedagem
    if hospedagem_id != 'error':
        hospedagem_id = hospedagem_id[0][0]

        pacote = Pacote.criaPacote(passagem_id_ida, passagem_id_volta, hospedagem_id, valor_pacote, session['passageiros'])
        Pacote.cadastraPacote(pacote) #ARMAZENA NO BANCO

    return render_template('Pacote.html', content = dict_pacote)

@app.route("/filtros", methods=["GET"])
def get_filtro():
    _dict = {
        "cidade":["São Paulo", "Porto Alegre", "Belo Horizonte", "Manaus", "Rio de Janeiro"]
    }
    
    #SELECIONAR FILTROS
    print("########## SELECIONANDO FILTROS ##########\n")
    return render_template('Filtros.html', content = _dict)

@app.route("/relatorio", methods=["POST"])
def gerar_relatorio():
    # tabela = request.form.get('tabela') #opção que escolhe tabela pra filtrar
    
    # if tabela == 'cidade':
    #     request.form.get('estado')
    
    # elif tabela == 'passagem':
    #     request.form.get('preco')
    #     request.form.get('duracao')
    #     request.form.get('qtde_conn')
    #     request.form.get('empresa')
    #     request.form.get('data_partida')
    #     request.form.get('data_chegada')
    #     request.form.get('origem')
    #     request.form.get('destino')
    
    # elif tabela == 'hospedagem':
    #     request.form.get('preco')
    #     request.form.get('avaliacao')
    #     request.form.get('estrelas')
    #     request.form.get('cidade')
    
    # elif tabela == 'atracao':
    #     request.form.get('categoria')
    #     request.form.get('views')
    #     request.form.get('estrelas')
    #     request.form.get('cidade')

    #     'select * from turismo_schema. where  '

    dados_banco = [{
        # 'cidade': [cidade1, cidade2],
        # 'Amount': [4, 5],
        # 'City': [cidade1, cidade2]
    }]
    df = pd.DataFrame(dados_banco[0])

    #GERAR RELATORIO
    print("########## GERANDO RELATORIO ##########\n")
    fig = px.bar(df, x='cidade', y='Amount', color='City', barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('Relatorio.html', graphJSON=graphJSON, content = dados_banco)

if __name__ == "__main__":
    app.secret_key = 'key'
    app.run()