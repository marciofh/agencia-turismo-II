import requests

#AIRPORTS/SEARCH https://rapidapi.com/apidojo/api/travel-advisor
class Cidade:
    def get_location(cidade):
        url = "https://travel-advisor.p.rapidapi.com/airports/search"
        querystring = {
            "query":cidade,
            "locale":"pt_BR"
            }
        headers = {
            "X-RapidAPI-Key": "12bb9c7718mshe8cbe79cbc0f70cp10b4c1jsnfb9d6a4ccc43",
            "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        response =  response.json()

        _dict = {
                "nome_cidade" : response[0]['display_title'],
                "location_id" : response[0]['location_id'],
                "aero_code" : '',
                "aero_nome": ''
            }

        if len(response) > 1:
            _dict['aero_code'] = response[1]['code']
            _dict['aero_nome'] = response[1]['name']
        else :
            _dict['aero_code'] = response[0]['code']
            _dict['aero_nome'] = response[0]['name']

        return _dict