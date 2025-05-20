import pandas as pd
import random
import nltk
from nltk.corpus import wordnet
import os

# Télécharger wordnet dans NLTK
nltk.download('wordnet')

# Fonction d'augmentation : remplacement par synonymes
def synonyme(text, n=1):
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

# Charger les titres originaux
df = pd.read_csv("../../data/raw/headfi_threads.csv")

# Supprimer les lignes vides
df = df.dropna(subset=["title"])

# Créer une nouvelle colonne avec la version augmentée
df["title_aug"] = df["title"].apply(lambda x: synonyme(str(x), n=1))

# Sauvegarder le nouveau dataset dans le fichier de data
os.makedirs("../../data/clean", exist_ok=True)
df.to_csv("../../data/clean/headfi_augmented.csv", index=False)

print("Fichier enregistré : headfi_augmented.csv")
print("Exemple :")
print(df[["title", "title_aug"]].head())
