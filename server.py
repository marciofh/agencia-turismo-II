from flask import Flask, render_template, request, session
from database import Cidade, Passagem, Hotel
from crawler import Crawler
from api import Api
import ast

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('Home.html')

@app.route("/passagem", methods=["POST"])
def passagem():
    session["origem"] = request.form.get('origem')
    session["destino"] = request.form.get('destino')
    session["passageiros"] = request.form.get('passageiros')
    session["data_ida"] = request.form.get('data_ida')
    session["data_volta"] = request.form.get('data_volta')

    #CONSULTAR CIDADE (DESTINO)   consultar se a cidade ja foi procurada antes
    print("\n########## CONSULTANDO CIDADE ##########")
    cidade = Cidade.consultaCidade(Cidade, session["destino"])

    #NÃO TEM CIDADE     quer dizer que o destino não foi pesquisando, nao tem passagem nem hotel
    if not cidade:
        print("nao tem cidade\n")
        session["city"] = False
        #CHAMAR CRAWLER
        print("########## EXECUTANDO CRAWLER ##########")
        crawler = Crawler()
        list_html = crawler.send_dados(session["origem"], session["destino"], session["passageiros"], session["data_ida"], session["data_volta"])
        session["url_gol"] = crawler.url_compra
        passagens = crawler.get_dados(list_html)

        #CADASTRAR PASSAGENS
        print("########## CADASTRANDO PASSAGEM ##########")
        for i in passagens['idas']:
            passagem = Passagem(i['origem'], i['destino'], i['hora_emb'], i['hora_desemb'], i['duracao'], i['conexao'], i['preco'], i['data'])
            passagem.cadastraPassagem()
        for i in passagens['voltas']:
            passagem = Passagem(i['origem'], i['destino'], i['hora_emb'], i['hora_desemb'], i['duracao'], i['conexao'], i['preco'], i['data'])
            passagem.cadastraPassagem()

    #TEM CIDADE     #quer dizer que destino ja foi pesquisado, pode ter passagem e hotel (depende da data)
    else:
        print("tem cidade\n")
        session["city"] = True
        #CONSULTAR PASSAGEM (ORIGEM, DESTINO, DATA)
        print("########## CONSULTANDO PASSAGEM ##########")
        ida = Passagem.consultaPassagem(Passagem, session["origem"], session["destino"], session["data_ida"])
        volta = Passagem.consultaPassagem(Passagem, session["destino"], session["origem"], session["data_volta"])

        #NÃO TEM PASSAGEM
        if not ida or not volta:
            print("nao tem passagem\n")
            #CHAMAR CRAWLER
            print("########## EXECUTANDO CRAWLER ##########")
            crawler = Crawler()
            list_html = crawler.send_dados(session["origem"], session["destino"], session["passageiros"], session["data_ida"], session["data_volta"])
            session["url_gol"] = crawler.url_compra
            passagens = crawler.get_dados(list_html)

            #CADASTRAR PASSAGENS
            print("########## CADASTRANDO PASSAGEM ##########")
            for i in passagens['idas']:
                passagem = Passagem(i['origem'], i['destino'], i['hora_emb'], i['hora_desemb'], i['duracao'], i['conexao'], i['preco'], i['data'])
                passagem.cadastraPassagem()
            for i in passagens['voltas']:
                passagem = Passagem(i['origem'], i['destino'], i['hora_emb'], i['hora_desemb'], i['duracao'], i['conexao'], i['preco'], i['data'])
                passagem.cadastraPassagem()
        
        #TEM PASSAGEM
        else:
            print("tem passgem\n")
            passagens = {
            "idas" : ida,
            "voltas" : volta
            }
            
    return render_template('Passagem.html', content = passagens)
    
@app.route("/hospedagem", methods=["POST"])
def hospedagem():
    voo_ida = request.form.get('voo_ida')
    voo_volta = request.form.get('voo_volta')
    session["voo_ida"] = voo_ida
    session["voo_volta"] = voo_volta
    destino = session["destino"]
    data_ida = session["data_ida"]
    data_volta = session["data_volta"]
    passageiros = session["passageiros"]
    city = session["city"]

    #TEM CIDADE             quer dizer que pode ter hotel
    if city:
        #CONSULTAR HOTEL (LOCATION_ID)
        print("\n########## CONSULTANDO HOTEL ##########")
        hotel = Hotel.consultaHotel(Hotel, session["destino"])
        print(hotel)

        #NÃO TEM HOTEL
        if not hotel:
            print("nao tem hotel\n")
            #CHAMAR API
            print("\n########## EXECUTANDO API ##########")
            location_id = Api.get_locationId(destino)
            hoteis = Api.get_hotels(location_id, passageiros, data_ida, data_volta)

        #TEM HOTEL
        else:
            print("tem hotel\n")
            hoteis = hotel
    
    #NÃO TEM CIDADE     quer dizer que não tem hotel
    else:
        #CHAMAR API
        print("\n########## EXECUTANDO API ##########")
        location_id = Api.get_locationId(destino)
        hoteis = Api.get_hotels(location_id, passageiros, data_ida, data_volta)
        
        #CADASTRAR CIDADE
        print("########## CADASTRANDO CIDADE ##########")
        cidade = Cidade(location_id, destino)
        cidade.cadastraCidade()

        #CADASTRAR HOTEIS
        print("\n########## CADASTRANDO HOTEL ##########")
        for i in hoteis:
            hotel = Hotel(i['nome'], i['preco'], i['foto'], i['ranking_site'], i['stars'], i['url_site'], i['endereco'], data_ida, session['destino'])
            hotel.cadastraHotel()

    return render_template('Hotel.html', content = hoteis)

@app.route("/pacote", methods=["POST"])
def pacote():
    hotel = request.form.get('hotel')
    ida = session["voo_ida"]
    volta = session["voo_volta"]
    hotel = ast.literal_eval(hotel)
    ida = ast.literal_eval(ida)
    volta = ast.literal_eval(volta)

    pacote = {
        "hotel": hotel,
        "ida": ida,
        "volta": volta,
        "url_gol": session['url_gol'],
        "passageiros": session['passageiros']
    }
    
    return render_template('Pacote.html', content = pacote)

if __name__ == "__main__":
    app.secret_key = 'key'
    app.run()