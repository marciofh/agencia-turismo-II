import requests

#attraction/list https://rapidapi.com/apidojo/api/travel-advisor
class Atracao:
    def get_atracao(location_id):
        url = "https://travel-advisor.p.rapidapi.com/attractions/list"

        querystring = {
            "location_id": location_id,
            "currency":"BRL",
            "lang":"pt_BR",
            "lunit":"km",
            "sort":"recommended"}

        headers = {
            "X-RapidAPI-Key": "15f96871b7msh35361c8ec15be36p13678ajsn0a39df238716",
            "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        response =  response.json()
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
                "avaliacao": i['rating']
                }  

                atracao['views'] = int(atracao['views'])
                atracao['avaliacao'] = float(atracao['avaliacao'])
                _dict.append(atracao)

            except:
                pass
        
        return _dict

# get_atracao(303631)