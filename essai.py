import requests
recherche = requests.get('https://books.toscrape.com/')

print(recherche.text)

