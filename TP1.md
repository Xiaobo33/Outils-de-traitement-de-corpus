# Partie 1 : étude de cas CoNLL 2003 : 
## 1. Quelle type de tâche propose CoNLL 2003 ? 
NER (Named Entity Recognition) et Token Classification. Les quatre types d'entité nommées sont : personnes, organisations, lieux et les autres entités.

## 2. Quel type de données y a-t-il dans CoNLL 2003 ? 
Il contient des journaux annotés : pour anglais c'est `Reuters Corpus`, pour allemand c'est `Frankfurter Rundschau`.

Les fichiers de données contiennet 4 colonnes séparées par un espace.
- Le premier élément est un mot.
- Le deuxième est le POS.
- Le troisième est chunking tag (tag de segmentation syntaxique).
- Le quatrième est le tag d'entité nommée.
- (Si la langue est allemand, il existe une colonne de plus pour mettre la lemme de chaque mot.)

## 3. A quel besoin répond CoNLL 2003 ?
CoNLL 2023 concerne l'aide au developpement et à l'évaluation de reconnaissance d'entités nommées.

## 4. Quels types de modèles ont été entraînés sur CoNLL 2003 ?
- Maximum Entropy Model : le plus fréquent
- Hidden Markov Models
- Conditional Markov Models

## 5. Est un corpus monolingue ou multilingue ? 
C'est un corpus multilingue, il contient deux langues : anglais et allemand.

## Référence : 
Introduction to the CoNLL-2003 Shared Task: Language-Independent Named Entity Recognition de Erik F. Tjong Kim Sang, Fien De Meulder

# Partie 2 : projet : Définis les besoins :
## 1. Besoin
L'objectif de mon projet est d'examiner les évaluations des produits d'Amazon et d'extraire des informations clés telles que les marques afin d'identifier les préférences des utilisateurs.

## 2. Sujet
Je décide d'analyse la catégorie `Digital Music` en traitant :
- L'extraction des entités nommées dans les titres de produits.
- La distribution des notes selon les marques ou les artistes.
- Peut-être la relation entre le prix et le note aussi. (pas encore décidé)

## 3. Type de tâche
Extraction des entités nommées

## 4. Type de données
J'utilise les métadonnées de la catégoire `Digitial Music`, qui contient : 
- main_category
- title
- average_rating
- description
- price
- images
- store
- details
- etc.
Je pense que je vais utiliser notamment `title`, `average_rating`, `price`, `store`, `details` pour extaire les informations.

## 5. Où je vais récupérer les données
J'ai trouvé un dataset d'Amazon review qui a plusieurs catégories dont DIgital Music : 

https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023

https://amazon-reviews-2023.github.io/

## 6. Les données sont libre d'accès ? 
Oui.