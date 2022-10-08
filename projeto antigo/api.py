import requests
from datetime import datetime
import pandas as pd
import re
import json
from credentials import keys

TOKEN = keys.get('TOKEN')

class Api:
    def get_locationId(location):
        url = "https://travel-advisor.p.rapidapi.com/locations/search"

        querystring = {
            "query": location,
            "limit":"1",
            "offset":"0",
            "units":"km",
            "location_id":"1",
            "currency":"BRL",
            "sort":"relevance",
            "lang":"pt_BR"
        }
        headers = {
            "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com",
            "X-RapidAPI-Key": TOKEN
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        response = response.json()
        location_id = response['data'][0]['result_object']['location_id']
        
        return location_id

    def get_hotels(location_id, passageiros, data_ida, data_volta):
        url = "https://travel-advisor.p.rapidapi.com/hotels/get-details"
        data_ida = datetime.strptime(data_ida, "%Y-%m-%d").date()
        data_volta = datetime.strptime(data_volta, "%Y-%m-%d").date()
        noites = (data_volta - data_ida).days

        querystring = {
            "location_id": location_id,
            "checkin": data_ida,
            "adults": passageiros,
            "lang":"pt_BR",
            "currency":"BRL",
            "nights": noites
        }   
        headers = {
            "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com",
            "X-RapidAPI-Key": TOKEN
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        response = response.json()
        dados = (response['data'])

        lista_hotel = []
        for i in range(5):
            dados[i]['raw_ranking'] = float(dados[i]['raw_ranking'])
            dados[i]['raw_ranking'] = round(dados[i]['raw_ranking'], 2)
            hotel = {
                "nome" : dados[i]['name'],
                "preco" : dados[i]['price'],
                "foto" : dados[i]['photo']['images']['small']['url'],
                "ranking_site" : dados[i]['raw_ranking'],
                "stars": dados[i]['hotel_class'],
                "url_site" : dados[i]['web_url'],
                "endereco" : dados[i]['address'],
                "data": data_ida
            }
            lista_hotel.append(hotel)
        df = pd.DataFrame(lista_hotel)
        df['preco'] = df['preco'].map(lambda x: x[3:10])
        df['preco'] = df['preco'].map(lambda x: re.sub('[^0-9,]', '', x))
        print(df)
        print()
        js = df.to_json(orient = 'records')
        js = json.loads(js)
        
        return js