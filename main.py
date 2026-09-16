import requests
from bs4 import BeautifulSoup
html_livre = requests.get('https://books.toscrape.com/catalogue/full-moon-over-noahs-ark-an-odyssey-to-mount-ararat-and-beyond_811/index.html')

soup = BeautifulSoup(html_livre.text, 'html.parser')
recherche = soup.find_all(['th','td'])
for ligne in recherche:
    print(ligne.get_text(" ", strip=True))