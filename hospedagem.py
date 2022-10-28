import requests
import re
from credentials import keys

#hotels/get-details https://rapidapi.com/apidojo/api/travel-advisor
class Hospedagem:
    def get_hotels(location_id, passageiros, data_ida, noites):
        TOKEN = keys.get('token_travel_advisor')
        url = "https://travel-advisor.p.rapidapi.com/hotels/get-details"
        querystring = {
            "location_id": location_id,
            "checkin": data_ida,
            "adults": passageiros,
            "currency": "BRL",
            "lang": "pt_BR",
            "nights": noites
        }
        headers = {
            "X-RapidAPI-Key": TOKEN,
            "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
        }
        dados = []

        while len(dados) == 0:
            response = requests.request("GET", url, headers=headers, params=querystring)
            response = response.json()
            dados = response['data']
            
            #apenas para verificação
            if len(dados) == 0:
                print('VAZIO\n')
            else:
                print('CHEIO\n')

        _dict = []
        for i in dados:
            try:
                hotel = {
                    "nome_hotel": i['name'],
                    "preco" : i['price'],
                    "foto": i['photo']['images']['small']['url'],
                    "avaliacao": i['raw_ranking'],
                    "estrelas": i['hotel_class'],
                    "endereco": i['address']
                }
            
                hotel['avaliacao'] = float(hotel['avaliacao'])
                hotel['avaliacao'] = round(hotel['avaliacao'], 2)
                hotel['estrelas'] = float(hotel['estrelas'])
                hotel['preco'] = hotel['preco'][2:10]
                hotel['preco'] = re.sub('[^0-9,]', '', hotel['preco'])
                hotel['preco'] = re.sub(',', '.', hotel['preco'])
                hotel['preco'] = float(hotel['preco'])

                _dict.append(hotel)
            except:
                pass

        return _dict

# get_hotels(303631, 2, '2022-11-20', 2)