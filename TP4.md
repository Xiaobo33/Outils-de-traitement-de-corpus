# TP4 : Augmentation des données

### A partir des données que vous avez récupérées, augmentez vos données en créant un dataset synthétique.

Rapport : Après avoir écrire le script de remplacement des synonymes, j'ai trouvé que j'ai oublié de nettoyer les données, il existe plein de noises dedans, donc je recommence la tâche. Puis dans le cadre de l'enrichissement de mon corpus, j'ai mis en place une méthode simple du remplacement de mots par des synonymes. Pour chaque titre nettoyé, j'ai identifié un ou plusieurs mots ayant des synonymes disponibles via `WordNet` de NLTK, et j'ai remplacé aléatoirement un mot par un de ses synonymes. Finalement j'ai fusionné les titres originales et leurs synonymes dans mon fichier de sortie `headfi_merged.csv`.

Cependant, l'effet de ce remplacement n'est pas très bon, je suppose que c'est parce qu'il n'y a pas autant de synonymes pour chaque titre courte (surtout les titres sont avec beaucoup d'entités nommées).

### Choississez l'architecture adaptée à votre tâche et trouvez un modèle qui correspond à votre tâche et à cette architecture.

Rapport : Avant de choisir un modèle, il faut d'abord faire les étiquettes des marques que je veux récupérer, je les fais avec un script simple `label.py`, en utilisant un dictionnaire des marques que j'ai créé, je les annonte en trois catégories : `B-BRAND`, `I-BRAND`, `O`.

Ensuite j'ai séparé mon corpus en trois parties pour que je puisse mieux entraîner mon modèle suivant : 
- 80% pour l'entraînement
- 10% pour la validation
- 10% pour le test. 

Enfin pour le modèle, j'ai choisi un modèle de `Token classification` sur HuggingFace, qui s'appelle [bert-base-NER](https://huggingface.co/dslim/bert-base-NER). Ce modèle est un modèle de deep learning de classification des entités nommées, il est entraîné sur le corpus `conll2003` et est capable de traiter les données en anglais.