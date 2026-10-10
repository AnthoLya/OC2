#BASE
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import os
import re

os.makedirs("data/images", exist_ok=True)

def letter_to_number(letter):
    letter_mapping = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    return letter_mapping.get(letter, 0)

def convertir_en_nombre(a):
    nombre = ""
    texte = a
    for caractere in texte:
        if caractere.isdigit() or caractere == ".":
            nombre = nombre + caractere
    nombre = str(float(nombre)) + " £"
    return nombre

def nettoyer_nom_fichier(nom):
    nom = re.sub(r'[\\/:*?"<>|]', '', nom)
    return nom.strip()

def extraire_urls_categories(url_base):
    reponse = requests.get(url_base)
    soup = BeautifulSoup(reponse.text, "html.parser")
    url_categories = soup.find("ul", class_="nav nav-list").find_all("li")
    tous_les_urls_categories = {}
    for categorie in url_categories[1:]:
        #avec le [1:]  car ej veux commener par la premeire categorie et pas books ou il y a tout avec les 50apges

        titre_categorie = categorie.find("a").get_text(strip=True)
        url_categorie = categorie.find("a")["href"]
        url_categorie = "https://books.toscrape.com/" + url_categorie
        tous_les_urls_categories[titre_categorie] = url_categorie
    return tous_les_urls_categories


def extraire_urls_livres(url_categorie):
    urls_livres = {}
    while url_categorie:
        reponse = requests.get(url_categorie)
        print("Page catégorie :", url_categorie)
        soup = BeautifulSoup(reponse.text, "html.parser")

        pagination = soup.select_one(".form-horizontal strong")
        nombre_livres_categorie = int(pagination.get_text(strip=True))
        nom_categorie = soup.find("h1").get_text(strip=True)
        urls = soup.find_all("article", class_="product_pod")
        for resultat in urls:

            titre_livre = resultat.find("h3").find("a")["title"]
            lien_url = resultat.find("a")["href"]
            lien_url = urljoin(url_categorie, lien_url)
            if titre_livre in urls_livres:
                titre_livre = titre_livre + " (doublon)"

            urls_livres[titre_livre] = lien_url


        suivant = soup.find("li", class_="next")
        if suivant:
            url_categorie = urljoin(url_categorie, suivant.find("a")["href"])
        else:
            url_categorie = None
    print("Catégorie :", nom_categorie)
    print("Nombre de livres annoncés :", nombre_livres_categorie)
    print("Nombre d'URL récupérées :", len(urls_livres))
    return urls_livres


def extraire_infos_livre(url, n):
    dictionnaire_categorie = {}

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

    description = soup.find("div", id="product_description")
    if description:
        description = description.find_next_sibling("p")
        if description:
            dictionnaire_categorie["product_description"] = description.get_text(strip=True)
        else:
            dictionnaire_categorie["product_description"] = "pas de description"
    else:
        dictionnaire_categorie["product_description"] = "pas de description"


    rating = soup.find("p", class_="star-rating")
    dictionnaire_categorie["review_rating"]  = rating["class"][1]

    category = soup.find("ul", class_="breadcrumb").find_all("li")
    dictionnaire_categorie["category"]  = category[2].get_text(strip=True)

    image = soup.find("img")
    image_url = urljoin(url, image["src"])
    dictionnaire_categorie["image_url"] = image_url

    nom_image = nettoyer_nom_fichier(dictionnaire_categorie["title"])
    nom_image = f"{n:05d} - {nom_image}"
    dictionnaire_categorie["lien_image"] = f"images/{nom_image}.jpg"

    reponse = requests.get(image_url)
    with open(f"data/images/{nom_image}.jpg", "wb") as fichier:
        fichier.write(reponse.content)


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


    # le prix je le garde en nombre aussi avec le symboles £
    dictionnaire_categorie["price_excluding_tax"] = convertir_en_nombre(dictionnaire_categorie["price_excluding_tax"])
    dictionnaire_categorie["price_including_tax"] = convertir_en_nombre(dictionnaire_categorie["price_including_tax"])

    #je passe la notation du texte a un nombre d etoiles
    dictionnaire_categorie["review_rating"] = letter_to_number(dictionnaire_categorie["review_rating"])

    # je remets tout dans l ordre
    dictionnaire_categorie_final = {
        "product_page_url": dictionnaire_categorie["product_page_url"],
        "universal_product_code (upc)": dictionnaire_categorie["universal_product_code (upc)"],
        "title": dictionnaire_categorie["title"],
        "price_including_tax": dictionnaire_categorie["price_including_tax"],
        "price_excluding_tax": dictionnaire_categorie["price_excluding_tax"],
        "number_available": dictionnaire_categorie["number_available"],
        "product_description": dictionnaire_categorie["product_description"],
        "category": dictionnaire_categorie["category"],
        "review_rating": dictionnaire_categorie["review_rating"],
        "image_url": dictionnaire_categorie["image_url"],
        "lien_image": dictionnaire_categorie["lien_image"]
    }

    return dictionnaire_categorie_final


def charger_csv(titre_categorie, livres):
    data_categorie = "data/data_" + titre_categorie + ".csv"
    with open(data_categorie, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=livres[0].keys())
        writer.writeheader()
        for livre in livres:
            writer.writerow(livre)