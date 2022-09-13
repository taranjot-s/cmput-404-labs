import requests

print(requests.__version__)

response = requests.get(
    "https://raw.githubusercontent.com/taranjot-s/cmput-404-labs/main/script1.py")

print(response.content)
