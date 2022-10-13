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
                "nome": dados[i]['name'],
                "preco" : dados[i]['price'],
                "foto": dados[i]['photo']['images']['small']['url'],
                "avaliacao": dados[i]['raw_ranking'],
                "estrelas": dados[i]['hotel_class'],
                "endereco": dados[i]['address']
            }
            _dict.append(hotel)
        
        return _dict

# get_hotels(303631, '2022-03-15', 3, 1)