
from utils import convertir_en_nombre, extraire_infos_livre, extraire_urls_categories, extraire_urls_livres, charger_csv

tous_les_urls_categories = extraire_urls_categories("https://books.toscrape.com/index.html")

for titre_categorie, url_categorie in tous_les_urls_categories.items():

    urls_livres = extraire_urls_livres(url_categorie)

    tous_les_livres = []

    for url_livre in urls_livres.values():
        print("Je commence l'extraction du livre")
        livre = extraire_infos_livre(url_livre)
        print("Extraction infos livre terminée")
        tous_les_livres.append(livre)
    print("je commence le CSV")
    charger_csv(titre_categorie, tous_les_livres)
