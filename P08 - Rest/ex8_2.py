# https://api.ptdata.org/docs#tag/Weather
# https://requests.readthedocs.io/en/latest/

import requests
import json

url_base = 'https://api.ptdata.org'
url = url_base + '/v1/weather/forecasts'
parametros = ""

resultado = requests.get(url, params=parametros)

print(json.dumps(resultado.json(), indent=2, ensure_ascii=False))
