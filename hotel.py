import requests

def get_hotels():
    url = "https://travel-advisor.p.rapidapi.com/hotels/get-details"
    querystring = {
        "location_id":"303631",
        "checkin":"2022-10-15",
        "adults":"1",
        "lang":"pt_BR",
        "currency":"BRL",
        "nights":"2"
        }
    headers = {
        "X-RapidAPI-Key": "12bb9c7718mshe8cbe79cbc0f70cp10b4c1jsnfb9d6a4ccc43",
        "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response =  response.json()
    
    print(response.text)

get_hotels()