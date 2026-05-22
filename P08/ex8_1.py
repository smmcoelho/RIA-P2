# https://api.ptdata.org/docs#tag/Weather
# https://requests.readthedocs.io/en/latest/

import requests
import json

url_base = 'https://api.ptdata.org'
url = url_base + "/v1/geo/districts"

parametros = {}

resposta = requests.get(url, params=parametros)

# print(json.dumps(resposta.json(), indent=4))

for distrito in resposta.json()["data"]["districts"]:
    print(distrito)
