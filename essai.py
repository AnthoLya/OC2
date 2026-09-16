import requests
recherche = requests.get('https://books.toscrape.com/catalogue/full-moon-over-noahs-ark-an-odyssey-to-mount-ararat-and-beyond_811/index.html')
information1 = "product"
print(recherche.text)
if information1 in recherche.text:
    print("il y a product dans la recheche")
else:
    print("il n'y a pas product dans la recheche")
n=0
for information1 in recherche.text:
    n=n+1
print(f"il y a {n} fois le terme product")
