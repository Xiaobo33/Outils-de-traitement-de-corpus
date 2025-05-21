# TP 5 Finetuner le modèle pretrained qui correspond le plus à vos données grâce au trainer d'hugging face

Rapport : 

Le but de cette étape était de détecter des marques (labels B-BRAND, I-BRAND) dans le corpus, mais comme le modèle pré-entraîné utilise B-ORG et I-ORG, j'ai d'abord remplacé ces étiquettes.

Et puis pour le prétraitement des données, j'ai utilisé mes deux fichiers CSV (train.csv et val.csv) pour créer des ensembles d'entraînement et de validation. Les données ont été regroupées par phrase. J'ai tokenisé les phrases avec le tokenizer de BERT, en alignant les étiquettes avec les sous-tokens.
De plus, j'ai utilisé `label_all_tokens = True` pour attribuer une étiquette à tous les sous-tokens, ce qui donne un apprentissage plus précis mais plus long.

Le modèle utilisé est `AutoModelForTokenClassification` avec 3 étiquettes : `O`, `B-ORG`, `I-ORG`.J'ai aussi utilisé un `DataCollatorForTokenClassification` pour gérer les lots (batches) pendant l'entraînement.



Voici les paramètres principaux :
- learning_rate = 2e-5
- num_train_epochs = 3
- per_device_train_batch_size = 16 : j'ai augmenté la taille de lot pour accélérer l'entraînement
- per_device_eval_batch_size = 16 : pareil
- weight_decay = 0.01 : pour éviter le surapprentissage

Problèmes rencontrés : L'entraînement a pris beaucoup de temps, j'ai dû interrompre une première fois puis relancer avec une augmentation de `batch_size` pour accélérer le processus.

Résultats obtenus : 
Après avoir entraîné le modèle pendant 7482 étapes, j'ai obtenu les résultats suivants sur les données de validation, extraits directement du checkpoint correspondant :
À l'époque 1.0 (étape 2494) :

- Accuracy : 99.96%
- Précision : 99.75%
- Rappel : 99.93%
- F1-score : 99.84%
- Perte : 0.00275

À l'époque 2.0 (étape 4988) :

- Accuracy : 99.97%
- Précision : 99.82%
- Rappel : 99.95%
- F1-score : 99.89%
- Perte : 0.00241

Ces résultats montrent que le modèle atteint une excellente performance de reconnaissance.
---

# TP 6 Evaluer votre modèle

Rapport : 

Le modèle a été évalué sur le jeu de test. L'évaluation a été effectuée à l'aide du script `evaluer.py`, avec le tokenizer et les poids du modèle chargés depuis le dossier de `checkpoint-7482`. Dans le script, je reutilise les fonctions dans l'ancien script commme la fonction de Tokenization et alignement des labels.

Première fois, j'ai obtenu des résultats pas très normals : 

{
    "eval_loss": 4.010585598734906e-06,
    "eval_model_preparation_time": 0.0048,
    "eval_precision": 0.0,
    "eval_recall": 0.0,
    "eval_f1": 0.0,
    "eval_accuracy": 1.0,
    "eval_runtime": 37.6992,
    "eval_samples_per_second": 131.806,
    "eval_steps_per_second": 8.25
}

En particulier, la précision, le rappel et le F1-score étaient tous à zéro, alors que l'exactitude était égale à 1.0, ce qui est incohérent. Donc je suppose qu'il y a eu un problème dans la correspondance entre les prédictions et les labels réels, ou une erreur dans le calcul des métriques

Après une revue les codes, en ajoutant des print pour tester chaque étape, notamment de la conversion des labels et de l'alignement entre tokens et annotations, une deuxième exécution a donné des résultats plus cohérents et très satisfaisants :

{
    "eval_loss": 4.711645942734322e-06,
    "eval_model_preparation_time": 0.001,
    "eval_precision": 1.0,
    "eval_recall": 1.0,
    "eval_f1": 1.0,
    "eval_accuracy": 1.0,
    "eval_runtime": 50.3118,
    "eval_samples_per_second": 99.142,
    "eval_steps_per_second": 6.201
}

Le modèle a obtenu une précision, un rappel, un F1-score et une exactitude parfaits sur le jeu de test.


Analyse et remarques : 

Le premier résultat anormal était probablement dû à un problème dans la gestion des labels ou dans la fonction de calcul des métriques (par exemple, une conversion incorrecte des tags BIO vers les classes attendues).

E pour le second résultat, avec des scores parfaits, est suspect dans un contexte réel, car il est rare qu'un modèle obtienne une performance parfaite sur un jeu de test non vu auparavant. Cela peut indiquer que le jeu de test est trop proche des données d'entraînement, car je n'ai que 3 labels (O, B-ORG, I-ORG), donc le modèle a eu facilité à apprendre à reconnaître ces labels.

En conclusion, je pense que le modèle a été évalué avec succès, et les métriques obtenues montrent une très bonne performance sur le jeu de test fourni. Cependant, il faut d'utiliser un jeu de test plus varié la prochaine fois pour mieux évaluer la généralisation du modèle.