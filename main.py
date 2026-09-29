#BASE
import requests
from bs4 import BeautifulSoup
import csv
dictionnaire = {}
#1 je recup le html
reponse = requests.get("https://books.toscrape.com/catalogue/starving-hearts-triangular-trade-trilogy-1_990/index.html")
soup = BeautifulSoup(reponse.text, "html.parser")

#2 je cherche une info
lignes = soup.find_all("tr")
titre = soup.find("h1").get_text(strip=True)
dictionnaire["titre"] = titre
for ligne in lignes:
    valeur = ligne.find("th").get_text(strip=True)
    donnee = ligne.find("td").get_text(strip=True)
    dictionnaire[valeur] = donnee

print(dictionnaire)

with open("data.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=dictionnaire.keys())
    writer.writeheader()
    writer.writerow(dictionnaire)