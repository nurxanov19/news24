import requests

url = 'https://cbu.uz/oz/arkhiv-kursov-valyut/json/'
responses = requests.get(url)
data = responses.json()

for key in data:
    print(f"{key if float(key['Rate']) > 12940.58 else None}")