import requests
import json
from pprint import pprint

url = "https://superhero-search.p.rapidapi.com/api/"

querystring = {"hero":"Spiderman"}

headers = {
    'x-rapidapi-host': "superhero-search.p.rapidapi.com",
    'x-rapidapi-key': "xxxxx"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

j_data = response.json()

with open("superhero-search_API.json", "w") as write_f:
    json.dump(j_data, write_f)