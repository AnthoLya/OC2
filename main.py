#BASE
import requests
from bs4 import BeautifulSoup
import csv
dictionnaire = {}

#1 je recup le html
url = "https://books.toscrape.com/catalogue/starving-hearts-triangular-trade-trilogy-1_990/index.html"
reponse = requests.get(url)
soup = BeautifulSoup(reponse.text, "html.parser")


#2 je cherche une info et l ajoute au dictionnaire

lignes = soup.find_all("tr")
dictionnaire["product_page_url"] = url

titre = soup.find("h1").get_text(strip=True)
dictionnaire["title"] = titre

for ligne in lignes:
    valeur = ligne.find("th").get_text(strip=True)
    donnee = ligne.find("td").get_text(strip=True)
    dictionnaire[valeur] = donnee

description = soup.find("div", id="product_description").find_next_sibling("p")
dictionnaire["product_description"] = description.get_text(strip=True)

rating = soup.find("p", class_="star-rating")
dictionnaire["review_rating"]  = rating["class"][1]

category = soup.find("ul", class_="breadcrumb").find_all("li")
dictionnaire["category"]  = category[2].get_text(strip=True)

image = soup.find("img")
image_url = image["src"]
image_url = image_url.replace("../../", "https://books.toscrape.com/")
dictionnaire["image_url"] = image_url


#je change les noms recupérés en td et th par ceux demandés
dictionnaire["universal_product_code (upc)"] = dictionnaire["UPC"]
dictionnaire["price_including_tax"] = dictionnaire["Price (incl. tax)"]
dictionnaire["price_excluding_tax"] = dictionnaire["Price (excl. tax)"]
dictionnaire["number_available"] = dictionnaire["Availability"]


#le available je ne garde que le nombre
nombre = ""
texte = dictionnaire["number_available"]
for caractere in texte:
    if caractere.isdigit():
        nombre = nombre + caractere
print(nombre)
nombre = int(nombre)
dictionnaire["number_available"] = nombre

#je remets tout dans l ordre
dictionnaire_final = {
    "product_page_url": dictionnaire["product_page_url"],
    "universal_product_code (upc)": dictionnaire["UPC"],
    "title": dictionnaire["title"],
    "price_including_tax": dictionnaire["Price (incl. tax)"],
    "price_excluding_tax": dictionnaire["Price (excl. tax)"],
    "number_available": dictionnaire["number_available"],
    "product_description": dictionnaire["product_description"],
    "category": dictionnaire["category"],
    "review_rating": dictionnaire["review_rating"],
    "image_url": dictionnaire["image_url"]
}

print(dictionnaire_final)

#je fais mon fichier CSV
with open("data.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=dictionnaire_final.keys())
    writer.writeheader()
    writer.writerow(dictionnaire_final)