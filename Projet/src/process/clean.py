import pandas as pd
import re
import os
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Je definie la fonction de nettoyage
def clean_text(text):
    text = str(text).lower()  # minuscule
    text = re.sub(r"http\S+", "", text)  # supprimer les URLs
    text = re.sub(r"[^a-z0-9\s]", "", text)  # supprimer ponctuation
    text = re.sub(r"\s+", " ", text).strip()  # espaces multiples
    text = re.sub(r"[^\x00-\x7F]+", "", text) # emojis
    text = " ".join([word for word in text.split() if word not in stop_words]) # stopwords
    text = re.sub(r"\d+", "", text) # les nombres
    return text

# Charger les titres
df = pd.read_csv("../../data/raw/headfi_threads.csv")

# Supprimer les lignes vides
df = df.dropna(subset=["title"])

# Appliquer le nettoyage
df["title_clean"] = df["title"].apply(clean_text)

# Et auvegarder
os.makedirs("../../data/clean", exist_ok=True)
df.to_csv("../../data/clean/headfi_threads_clean.csv", index=False)

print("Fichier enregistré : headfi_threads_clean.csv")

# Pour vérifier le résultat
print(df[["title", "title_clean"]].head())
