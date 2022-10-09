import requests
from datetime import datetime
import dateutil.parser


# Search (departures, one way) https://rapidapi.com/tipsters/api/priceline-com-provider
# class Passagem:
def get_passagem(data, passageiros, aero_origem, aero_destino):
    url = "https://priceline-com-provider.p.rapidapi.com/v2/flight/departures"
    querystring = {
        "sid":"iSiX639",
        "departure_date":data,
        "adults":passageiros,
        "convert_currency":"BRL",
        "origin_airport_code":aero_origem,
        "destination_airport_code":aero_destino
        }
    headers = {
        "X-RapidAPI-Key": "12bb9c7718mshe8cbe79cbc0f70cp10b4c1jsnfb9d6a4ccc43",
        "X-RapidAPI-Host": "priceline-com-provider.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response =  response.json()
    response = response['getAirFlightDepartures']['results']['result']['itinerary_data']
    
    _dict = []

    for i in response:
        # data_hora_partida = response[i]['slice_data']['slice_0']['departure']['datetime']['date_time'].split('T')
        # data_hora_chegada = response[i]['slice_data']['slice_0']['arrival']['datetime']['date_time'].split('T')
        # date_object = datetime.strptime(data_hora_partida[0], '%Y-%d-%m').date()
        # print(date_object)\

        voo = {
            "origem": response[i]['slice_data']['slice_0']['departure']['airport']['city'],
            "destino": response[i]['slice_data']['slice_0']['arrival']['airport']['city'],
            "aero_origem": response[i]['slice_data']['slice_0']['departure']['airport']['code'],
            "aero_destino": response[i]['slice_data']['slice_0']['arrival']['airport']['code'],
            "preco": response[i]['price_details']['display_total_fare_per_ticket'],
            "duracao": response[i]['slice_data']['slice_0']['info']['duration'],
            "qtde_conn": response[i]['slice_data']['slice_0']['info']['connection_count'],
            "empresa": response[i]['slice_data']['slice_0']['airline']['name'],
            "data_partida": response[i]['slice_data']['slice_0']['departure']['datetime']['date_time'],
            "data_chegada": response[i]['slice_data']['slice_0']['departure']['datetime']['date_time'],
        }

        voo['duracao'] = datetime.strptime(voo['duracao'], '%H:%M:%S').time()
        voo['data_partida'] = dateutil.parser.parse(voo['data_partida'])
        voo['data_partida'] = datetime.strptime(voo['data_partida'], "%Y/%m/%d %H:%M:%S").date()

        voo['data_chegada'] = dateutil.parser.parse(voo['data_chegada'])
        print(type(voo['data_partida']))
        
        _dict.append(voo)
    # print(_dict)

    return _dict

get_passagem('2022-10-16', 2, 'GRU', 'GIG')
# using strptime() to get datetime object
# datetime_obj = datetime.datetime.strptime(
#     date_string, '%Y-%m-%d %H:%M:%S.%f %z')origem': 'Sao Paulo', 'destino': 'Rio de Janeiro', 'aero_origem': 'GRU', 'aero_destino': 'GIG', 'preco': 1562.34, 'duracao': '00:01:00', 'qtde_conn': 0, 'empresa': 'LATAM Airlines', 'dt_partida': '2022-10-16T06:55:00', 'dt_chegada': '2022-10-16T07:55:00'}

# {'