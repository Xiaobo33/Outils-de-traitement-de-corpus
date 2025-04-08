import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re
import random
from sklearn.model_selection import train_test_split

import spacy
nlp = spacy.load("en_core_web_sm")

# chargement des données
df = pd.read_csv("../../data/raw/headfi_threads.csv")

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

'''
# augmentation de données : remplacement par synonymes
from nltk.corpus import wordnet
import nltk
nltk.download('wordnet')

def synonym_replacement(text, n=1):
    words = text.split()
    new_words = words.copy()
    for _ in range(n):
        candidates = [w for w in new_words if wordnet.synsets(w)]
        if not candidates:
            break
        word_to_replace = random.choice(candidates)
        synonyms = wordnet.synsets(word_to_replace)[0].lemma_names()
        if synonyms:
            new_word = random.choice(synonyms)
            new_words = [new_word if w == word_to_replace else w for w in new_words]
    return " ".join(new_words)

'''
    
# split les 3 sets
X_temp, X_test = train_test_split(df["title"], test_size=0.2, random_state=42)
X_train, X_valid = train_test_split(X_temp, test_size=0.25, random_state=42)

print(f"Taille du train : {len(X_train)}")
print(f"Taille du validation : {len(X_valid)}")
print(f"Taille du test : {len(X_test)}")