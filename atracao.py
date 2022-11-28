import requests
from credentials import keys

#attraction/list https://rapidapi.com/apidojo/api/travel-advisor
class ApiAtracao:
    def get_atracao(location_id):
        TOKEN = keys.get('token')
        url = "https://travel-advisor.p.rapidapi.com/attractions/list"
        querystring = {
            "location_id": location_id,
            "currency": "BRL",
            "lang": "pt_BR",
            "lunit": "km",
            "sort": "recommended"
        }
        headers = {
            "X-RapidAPI-Key": TOKEN,
            "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        response = response.json()
        response = response['data']
        _dict = []

        for i in response:
            try:
                atracao = {
                    "nome_atracao": i['name'],
                    "foto": i['photo']['images']['small']['url'],
                    "categoria": i['subcategory'][0]['name'],
                    "endereco": i['address'],
                    "views": i['num_reviews'],
                    "avaliacao": i['rating'],
                    "cidade_id": i['ranking_geo_id']
                }  

                atracao['views'] = int(atracao['views'])
                atracao['avaliacao'] = float(atracao['avaliacao'])
                _dict.append(atracao)
            except:
                pass
        
        return _dict

# get_atracao(303631)