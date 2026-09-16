import requests
recherche = requests.get('https://books.toscrape.com/catalogue/full-moon-over-noahs-ark-an-odyssey-to-mount-ararat-and-beyond_811/index.html')
information1 = "product"
information2 = "price_color"
print(recherche.text)
if information1 in recherche.text:
    print(f"il y a {information1} dans la recheche")
else:
    print(f"il n'y a pas {information1} dans la recheche")
n1=0
for information1 in recherche.text:
    n1=n1+1
print(f"il y a {n1} fois le terme {information1}")

if information2 in recherche.text:
    print(f"il y a {information2} dans la recheche")
else:
    print(f"il n'y a pas {information2} dans la recheche")
n2=0
for information2 in recherche.text:
    n2=n2+1
print(f"il y a {n2} fois le terme {information2}")

#ca se repete je dois faire une fonction, et j'ai pas le retour de la valeur de {information1} et {information2} dans mon print
