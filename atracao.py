import requests

#attraction/list https://rapidapi.com/apidojo/api/travel-advisor
# class Atracao:
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

    for i in range(len(response)):
        try:
            atracao = {
            "nome_atracao": response[i]['name'],
            "foto": response[i]['photo']['images']['small']['url'],
            "categoria": response[i]['subcategory'][0]['name'],
            "endereco": response[i]['address'],
            "views": response[i]['num_reviews'],
            "estrelas": response[i]['rating']
        }   
            atracao['views'] = int(atracao['views'])
            atracao['estrelas'] = float(atracao['estrelas'])
            _dict.append(atracao)
        except:
            pass
    # return _dict

get_atracao(303631)