import requests

#hotels/get-details https://rapidapi.com/apidojo/api/travel-advisor
class Hospedagem:
    def get_hotels(location_id, passageiros, data_ida, data_volta):
        url = "https://travel-advisor.p.rapidapi.com/hotels/get-details"
        querystring = {
            "location_id":location_id,
            "checkin":data_ida,
            "adults":passageiros,
            "currency":"BRL",
            "nights":"2" #CALCULAR NOITES
            }
        headers = {
            "X-RapidAPI-Key": "12bb9c7718mshe8cbe79cbc0f70cp10b4c1jsnfb9d6a4ccc43",
            "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        response =  response.json()
        response = response['data']
        _dict = []
        
        #VERIFICAR DE RESPONSE É VAZIO

        for i in range(5):
            hotel = {
                "nome": response[i]['name'],
                "preco" : response[i]['price'],
                "foto": response[i]['photo']['images']['small']['url'],
                "avaliacao": response[i]['raw_ranking'],
                "estrelas": response[i]['hotel_class'],
                "endereco": response[i]['address']
            }
            _dict.append(hotel)
        
        return _dict