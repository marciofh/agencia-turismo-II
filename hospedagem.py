import requests
import re
from datetime import datetime

#hotels/get-details https://rapidapi.com/apidojo/api/travel-advisor
class Hospedagem:
    def get_hotels(location_id, passageiros, data_ida, data_volta):
        data_ida = datetime.strptime(data_ida, "%Y-%m-%d").date()
        data_volta = datetime.strptime(data_volta, "%Y-%m-%d").date()
        noites = (data_volta - data_ida).days

        url = "https://travel-advisor.p.rapidapi.com/hotels/get-details"
        querystring = {
            "location_id":location_id,
            "checkin":data_ida,
            "adults":passageiros,
            "currency":"BRL",
            "lang": 'pt_BR',
            "nights": noites
            }
        headers = {
            "X-RapidAPI-Key": "88eb6d5222mshc661135cc2ca447p15dd6djsn6c51ff9ca44c", #2º token
            "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
        }

        dados = []
        print(dados)
        print()

        while len(dados) == 0:
            response = requests.request("GET", url, headers=headers, params=querystring)
            response =  response.json()
            dados = response['data']
            
            #apenas para verificação
            if len(dados) == 0:
                print('[]\n')
            else:
                print('CHEIO\n')

        _dict = []

        for i in range(5):
            hotel = {
                "nome_hotel": dados[i]['name'],
                "preco" : dados[i]['price'],
                "foto": dados[i]['photo']['images']['small']['url'],
                "avaliacao": dados[i]['raw_ranking'],
                "estrelas": dados[i]['hotel_class'],
                "endereco": dados[i]['address']
            }
            
            hotel['avaliacao'] = float(hotel['avaliacao'])
            hotel['avaliacao'] = round(hotel['avaliacao'], 2)
            hotel['estrelas'] = float(hotel['estrelas'])
            hotel['preco'] = hotel['preco'][2:10]
            hotel['preco'] = re.sub('[^0-9,]', '', hotel['preco'])
            hotel['preco'] = re.sub(',', '.', hotel['preco'])
            hotel['preco'] = float(hotel['preco'])

            _dict.append(hotel)

        return _dict

# get_hotels(303631, 2, '2022-10-20', '2022-10-21')