import requests

#AIRPORTS/SEARCH https://rapidapi.com/apidojo/api/travel-advisor
def search_location():
    url = "https://travel-advisor.p.rapidapi.com/airports/search"
    querystring = {
        "query":"São Paulo",
        "locale":"pt_BR"
        }

    headers = {
        "X-RapidAPI-Key": "12bb9c7718mshe8cbe79cbc0f70cp10b4c1jsnfb9d6a4ccc43",
        "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    #buscar aeroportos e location id

    print(response.text)

# Search (departures, one way) https://rapidapi.com/tipsters/api/priceline-com-provider
def search_flight():
    url = "https://priceline-com-provider.p.rapidapi.com/v2/flight/departures"

    querystring = {
        "sid":"iSiX639",
        "departure_date":"2022-10-02",
        "adults":"1",
        "origin_airport_code":"GIG",
        "destination_airport_code":"GRU"    
        }

    headers = {
        "X-RapidAPI-Key": "12bb9c7718mshe8cbe79cbc0f70cp10b4c1jsnfb9d6a4ccc43",
        "X-RapidAPI-Host": "priceline-com-provider.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

search_location()