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

# Partie 2 : projet : 
## 1. Besoin
L'objectif de mon projet est d'extraire des entités nommées à partir d'un corpus web traitant des produits audio (Head-Fi : https://www.head-fi.org/forums/), plus précisément des casques audio, afin d'identifier les marques, modèles ou catégories de produits les plus fréquemment discutés par les utilisateurs dans le forum.

## 2. Sujet
Je décide d'analyse la catégorie casques `Headphones(full-size)` en traitant :
- L'extraction des entités nommées dans les titres des fils de discussion, qui composés de noms de marques, modèles ou des opinions particulières.

## 3. Type de tâche
Extraction des entités nommées

## 4. Type de données
Comment le site interdit de récupérer les contenus des posts, mon corpus ne contient que : 

- le titre
- url

Je vais les mettre dans un fichier CSV, qui peut être généré par mon script de scraping.

## 5. Où je vais récupérer les données

Les données viennent de ce site web : https://www.head-fi.org/forums/headphones-full-size.4/

Et j'ai écrit un scipt Python pour les collecter.

## 6. Les données sont libre d'accès ? 
Oui. J'ai déjà vérifier le fichier `robots.txt` du site.