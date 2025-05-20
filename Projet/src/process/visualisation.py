import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re
import random

import spacy
nlp = spacy.load("en_core_web_sm")

# chargement des données
df = pd.read_csv("../../data/clean/headfi_threads_clean.csv")

## longueur des titres (en mots et en caractères)
df["nb_mots"] = df["title"].apply(lambda x: len(str(x).split()))
df["nb_caractères"] = df["title"].apply(lambda x: len(str(x)))

## histogramme de la longueur des titres
plt.hist(df["nb_mots"], bins=20)
plt.title("Distribution du nombre de mots par titre")
plt.xlabel("Nombre de mots")
plt.ylabel("Nombre de titres")
plt.savefig("../../figure/histogramme_longueur_titres.png")
print("Enregistrement de l'histogramme dans le dossier 'figure'")
# plt.show() ca affiche pas dans le terminal

# analyse des mots fréquents (Zipf)
corpus = " ".join(df["title"].dropna())
tokens = re.findall(r'\b\w+\b', corpus.lower())
freq = Counter(tokens)

import csv

words_zipf = freq.most_common(100)

with open("../../figure/zipf_100.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["mot", "fréquence"])
    writer.writerows(words_zipf)

print("Enregistrement du fichier 'zipf_100.csv' dans le dossier 'figure'")

# Extraction des entités nommées
titles = df["title"].dropna().tolist()
entites = []

for title in titles:
    doc = nlp(title)
    entites.extend([ent.text for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT", "PERSON"]])

freq_ents = Counter(entites)

with open("../../figure/NER_100.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["entité", "fréquence"])
    writer.writerows(freq_ents.most_common(100))

print("Enregistrement de 'NER_100.csv' dans le dossier 'figure'")