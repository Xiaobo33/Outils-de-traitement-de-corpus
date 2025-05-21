# Visualisation des données

J'utilise le corpus que j'ai récupéré dans le TP2, sous le format CSV. Mais j'ai augmenté la taille à 25000 lignes pour mieux entraîner le modèle dans les étapes suivantes.

### 1. Analyse de la longueur des titres
J'utilise `len()` et `.split()` pour obtenir la longueur des titres. Et puis pour visualiser, je génére un histogramme avec `matplotlib`.

### 2. Analyse de la fréquence des mots et des entités nommées
- Pour la fréquence des mots, j'utilise `Counter()` de la bibliothèque `collections`. 

- Pour les entités nommées, j'utilise `spacy` (avec en_core_web_sm) pour le tokeniser et identifier les entités nommées. Par exemple ORG (les marques), PRODUCT (les modèles) et PERSON (j'ai pas beaucoup de noms de personnes dans le corpus mais ça peut être intéressant de voir). Pareil que la fréquence des mots, j'utilise `Counter()` pour obtenir les fréquences.

### 3. Nuage de mots
J'utilise `wordcloud` pour générer un nuage des titres, qui est plus compréhensible que le histogramme.


Enfin, tous les resulats sont enregistrés dans un dossier `figure`.