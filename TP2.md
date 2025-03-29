# TP2 : Récuperer votre corpus de travail à partir d'une resource web

Consigne : Mettez votre script de crawling et de scraping sur votre github en respectant l'arborescence de dossiers présenté aujourd'hui.

## Quelques précisions sur l'évaluation

Le projet à rendre comprend:

- l'analyse d'un corpus pré-existant
- la constitution d'un corpus similaire à partir de données ouverte
- l'applications de visualisation sur ces données
- l'évaluation du corpus constitué

## Rapport de TP2 

Avant je voudrais récupérer les données d'Amazon mais il me semble qu'il est ilégale de les récupérer. J'ai donc trouvé un autre site `Head-fi`(https://www.head-fi.org/forums/), qui discute des produits électroniques, et après avoir vérifier la page de `robots.txt`(ici https://www.head-fi.org/robots.txt), je prévois de scraper la section du forum dédiée aux casques audio.

Je d'abord crée l'arborescence de mon dossier Projet selon les consignes du cours. Mon script `crawl.py` est sous `process/src`, et les résultats sont sous `data/raw`. Après avoir tester mon script, tout fonctionne bien.