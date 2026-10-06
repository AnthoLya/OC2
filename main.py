
from utils import convertir_en_nombre, extraire_infos_livre, extraire_urls_categories, extraire_urls_livres, charger_csv
n = 0
tous_les_urls_categories = extraire_urls_categories("https://books.toscrape.com/index.html")

for titre_categorie, url_categorie in tous_les_urls_categories.items():

    urls_livres = extraire_urls_livres(url_categorie)

    tous_les_livres = []

    for url_livre in urls_livres.values():
        n += 1
        print(f"Je commence l'extraction du livre {n}")
        livre = extraire_infos_livre(url_livre, n)
        print("Extraction infos livre terminée")
        tous_les_livres.append(livre)
    print("je commence le CSV")
    charger_csv(titre_categorie, tous_les_livres)
