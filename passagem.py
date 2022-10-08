import requests

# Search (departures, one way) https://rapidapi.com/tipsters/api/priceline-com-provider
class Passagem:
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
            voo = {
                "origem": response[i]['slice_data']['slice_0']['departure']['airport']['city'],
                "destino": response[i]['slice_data']['slice_0']['arrival']['airport']['city'],
                "aero_origem": response[i]['slice_data']['slice_0']['departure']['airport']['code'],
                "aero_destino": response[i]['slice_data']['slice_0']['arrival']['airport']['code'],
                "preco": response[i]['price_details']['display_total_fare_per_ticket'],
                "duracao": response[i]['slice_data']['slice_0']['info']['duration'],
                "qtde_conn": response[i]['slice_data']['slice_0']['info']['connection_count'],
                "empresa": response[i]['slice_data']['slice_0']['airline']['name'],
                "dt_partida": response[i]['slice_data']['slice_0']['departure']['datetime']['date_time'],
                "dt_chegada": response[i]['slice_data']['slice_0']['arrival']['datetime']['date_time']
            }
            _dict.append(voo)
        
        return _dict