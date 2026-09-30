#BASE
import requests
from bs4 import BeautifulSoup
import csv
dictionnaire = {}

# je recup le html
url = "https://books.toscrape.com/catalogue/starving-hearts-triangular-trade-trilogy-1_990/index.html"
reponse = requests.get(url)
soup = BeautifulSoup(reponse.text, "html.parser")


# je cherche une info et l ajoute au dictionnaire
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


# je change les noms recupérés en td et th par ceux demandés
dictionnaire["universal_product_code (upc)"] = dictionnaire["UPC"]
dictionnaire["price_including_tax"] = dictionnaire["Price (incl. tax)"]
dictionnaire["price_excluding_tax"] = dictionnaire["Price (excl. tax)"]
dictionnaire["number_available"] = dictionnaire["Availability"]


# le available je ne garde que le nombre
nombre = ""
texte = dictionnaire["number_available"]
for caractere in texte:
    if caractere.isdigit():
        nombre = nombre + caractere
nombre = int(nombre)
dictionnaire["number_available"] = nombre

# je remets tout dans l ordre
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

#chercher si il y a next en bas de page pr page suivante
suivant = soup.find("li", class_="next")
if suivant:
    lien_suivant = suivant.find("a")["href"]
    print(lien_suivant)
else:
    print("pas de page suivante")


# je fais mon fichier CSV
with open("data.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=dictionnaire_final.keys())
    writer.writeheader()
    writer.writerow(dictionnaire_final)


#2eme phase : extraire tout les urls d'une categorie
tous_les_urls = {}

url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
reponse = requests.get(url)
soup = BeautifulSoup(reponse.text, "html.parser")
urls = soup.find_all("article", class_="product_pod")

for resultat in urls:
    titre = resultat.find("h3").get_text(strip=True)
    lien_url = resultat.find("a")["href"]
    lien_url = lien_url.replace("../../../", "https://books.toscrape.com/catalogue/")
    tous_les_urls[titre] = lien_url
print(tous_les_urls)

#je vais un csv avec tous les urls
with open("data_urls.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=tous_les_urls.keys())
    writer.writeheader()
    writer.writerow(tous_les_urls)

# je vais utiliser mes urls trouvées pour rechercher dans les pages des livres les infos
tous_les_livres = []


for url in tous_les_urls.values():
    dictionnaire_categorie = {}
    print(url)
# je recup le html
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")


# je cherche une info et l ajoute au dictionnaire
    lignes = soup.find_all("tr")
    dictionnaire_categorie["product_page_url"] = url

    titre = soup.find("h1").get_text(strip=True)
    dictionnaire_categorie["title"] = titre

    for ligne in lignes:
        valeur = ligne.find("th").get_text(strip=True)
        donnee = ligne.find("td").get_text(strip=True)
        dictionnaire_categorie[valeur] = donnee

    description = soup.find("div", id="product_description").find_next_sibling("p")
    dictionnaire_categorie["product_description"] = description.get_text(strip=True)

    rating = soup.find("p", class_="star-rating")
    dictionnaire_categorie["review_rating"]  = rating["class"][1]

    category = soup.find("ul", class_="breadcrumb").find_all("li")
    dictionnaire_categorie["category"]  = category[2].get_text(strip=True)

    image = soup.find("img")
    image_url = image["src"]
    image_url = image_url.replace("../../", "https://books.toscrape.com/")
    dictionnaire_categorie["image_url"] = image_url


# je change les noms recupérés en td et th par ceux demandés
    dictionnaire_categorie["universal_product_code (upc)"] = dictionnaire_categorie["UPC"]
    dictionnaire_categorie["price_including_tax"] = dictionnaire_categorie["Price (incl. tax)"]
    dictionnaire_categorie["price_excluding_tax"] = dictionnaire_categorie["Price (excl. tax)"]
    dictionnaire_categorie["number_available"] = dictionnaire_categorie["Availability"]


# le available je ne garde que le nombre
    nombre = ""
    texte = dictionnaire_categorie["number_available"]
    for caractere in texte:
        if caractere.isdigit():
            nombre = nombre + caractere
    nombre = int(nombre)
    dictionnaire_categorie["number_available"] = nombre

# je remets tout dans l ordre
    dictionnaire_categorie_final = {
        "product_page_url": dictionnaire_categorie["product_page_url"],
        "universal_product_code (upc)": dictionnaire_categorie["UPC"],
        "title": dictionnaire_categorie["title"],
        "price_including_tax": dictionnaire_categorie["Price (incl. tax)"],
        "price_excluding_tax": dictionnaire_categorie["Price (excl. tax)"],
        "number_available": dictionnaire_categorie["number_available"],
        "product_description": dictionnaire_categorie["product_description"],
        "category": dictionnaire_categorie["category"],
        "review_rating": dictionnaire_categorie["review_rating"],
        "image_url": dictionnaire_categorie["image_url"]
    }
    tous_les_livres.append(dictionnaire_categorie_final)

# je fais mon fichier CSV
with open("data_categorie.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=tous_les_livres[0].keys())
    writer.writeheader()
    for livre in tous_les_livres:
        writer.writerow(livre)
