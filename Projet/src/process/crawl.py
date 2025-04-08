import requests
from bs4 import BeautifulSoup
import time
import csv

# éviter le blocage
headers = {
    "User-Agent": "Mozilla/5.0"
}

base_url = "https://www.head-fi.org/forums/headphones-full-size.4/page-{}"
output_file = "/home/sibel/Outils-de-traitement-de-corpus/Projet/data/raw/headfi_threads.csv"
results = []

for page in range(1, 101):  # je parcours les 100 premières pages du forum
    url = base_url.format(page)
    print(f"Récupération de la page {page} : {url}")
    # envoyer une requête de GET
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    threads = soup.find_all("div", class_="structItem-title")
    for t in threads:
        a = t.find("a")
        if a:
            title = a.text.strip()
            link = "https://www.head-fi.org" + a['href']
            results.append([title, link])

# enregistrer dans un fichier CSV
with open(output_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "url"])
    writer.writerows(results)

print("Enregistrées dans ：", output_file)