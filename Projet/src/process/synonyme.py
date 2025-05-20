import pandas as pd
import random
import nltk
from nltk.corpus import wordnet
import os

# Utiliser le dictionnaire de WordNet
nltk.download('wordnet')

# Définition de la fonction d'augmentation par synonymes
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

# Input
df = pd.read_csv("../../data/clean/headfi_threads_clean.csv")
df = df.dropna(subset=["title_clean"])

# Génération d'une version augmentée
df["title_aug"] = df["title_clean"].apply(lambda x: synonyme(str(x), n=1))

# Je crée deux classes de données : la version originale et la version augmentée
df_orig = df[["title_clean"]].rename(columns={"title_clean": "text"})
df_aug = df[["title_aug"]].rename(columns={"title_aug": "text"})

# Ajouter une colonne source
df_orig["source"] = "original"
df_aug["source"] = "augmented"

# Merge les deux
df_merged = pd.concat([df_orig, df_aug], ignore_index=True)

# Sauvegarder
df_merged.to_csv("../../data/clean/headfi_merged.csv", index=False)

print("Fichier enregistré : headfi_merged.csv")