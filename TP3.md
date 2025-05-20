# Visualisation des données

J'utilise le corpus que j'ai récupéré dans le TP2, sous le format CSV. Mais j'ai augmenté la taille à 25000 lignes pour mieux entraîner le modèle dans les étapes suivantes.

### 1. Analyse de la longueur des titres
J'utilise `len()` et `.split()` pour obtenir la longueur des titres. Et puis pour visualiser, je génére un histogramme avec `matplotlib`.

### 2. Analyse de la fréquence des mots et des entités nommées
- Pour la fréquence des mots, j'utilise `Counter()` de la bibliothèque `collections`. 

- Pour les entités nommées, j'utilise `spacy` (avec en_core_web_sm) pour le tokeniser et identifier les entités nommées. Par exemple ORG (les marques), PRODUCT (les modèles) et PERSON (j'ai pas beaucoup de noms de personnes dans le corpus mais ça peut être intéressant de voir). Pareil que la fréquence des mots, j'utilise `Counter()` pour obtenir les fréquences.

### 3. Augmentation de données
J'ai augmenté le corpus en remplaçant les mots par synonymes, pour réaliser, j'ai utilisé `nltk.corpus.wordnet` et remplacé les mots par hasard. Mais pour l'instant j'ai pas encore enreigistré les résultats, car je pense que cela change la fréquence des mots.

### 4. Division du corpus
En utilisant la modèle `sklearn.model_selection.train_test_split()`, j'ai divisé le corpus en 3 datasets : train 60%, test 20%, validation 20%. (Cela peut être modifié plus tard en fonction des performances du modèle).


Enfin, tous les resulats sont enregistrés dans un dossier `figure`.