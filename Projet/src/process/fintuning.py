import numpy as np
from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer, AutoModelForTokenClassification, DataCollatorForTokenClassification, Trainer, TrainingArguments
import evaluate

################# Définir si on attribue une étiquette à tous les sous-tokens ###############
label_all_tokens = True  # True : on étiquette tous les sous-tokens ; False : uniquement le premier sous-token

################# Fonction de conversion des labels pour adapter à notre modèle #################

# Ici, on remplace "B-BRAND" et "I-BRAND" par "B-ORG" et "I-ORG" car le modèle pré-entraîné utilise ces labels
def convert_labels(labels):
    new_labels = []
    for label in labels:
        if label == "B-BRAND":
            new_labels.append("B-ORG")
        elif label == "I-BRAND":
            new_labels.append("I-ORG")
        else:
            new_labels.append(label)
    return new_labels

################# Définition des labels uniques et des mappings label <-> id #################
unique_labels = ["O", "B-ORG", "I-ORG"]
label_to_id = {label: i for i, label in enumerate(unique_labels)}
id_to_label = {i: label for label, i in label_to_id.items()}

################# Chargement du tokenizer et du modèle BERT de base #################

model_name = "bert-base-cased"  # ici, j'utilise le modèle de base mais pas le modèle de NER
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name, num_labels=len(unique_labels))


################# datasets #################
import pandas as pd

def load_and_group(path):
    df = pd.read_csv(path)
    # Sauter les lignes inutiles
    df = df[df["token"].apply(lambda x: isinstance(x, str) and x.strip() != "text")]
    df = df[df["label"].apply(lambda x: isinstance(x, str) and x.strip() in {"O", "B-BRAND", "I-BRAND"})]
    df["sentence_id"] = df["sentence_id"].astype(int)

    grouped = {
        "tokens": df.groupby("sentence_id")["token"].apply(list).tolist(),
        "labels": df.groupby("sentence_id")["label"].apply(list).tolist(),
    }
    return Dataset.from_dict(grouped)

train_dataset = load_and_group("../../data/clean/train.csv")
eval_dataset = load_and_group("../../data/clean/val.csv")

datasets = DatasetDict({
    "train": train_dataset,
    "validation": eval_dataset
})

################# Tokenization et alignement des labels #################
def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True)

    all_labels = examples["labels"]
    new_labels = []
    for i, labels in enumerate(all_labels):
        converted_labels = convert_labels(labels)
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)
            elif word_idx != previous_word_idx:
                label_ids.append(label_to_id[converted_labels[word_idx]])
            else:
                label_ids.append(label_to_id[converted_labels[word_idx]] if label_all_tokens else -100)
            previous_word_idx = word_idx
        new_labels.append(label_ids)

    tokenized_inputs["labels"] = new_labels
    return tokenized_inputs

tokenized_datasets = datasets.map(tokenize_and_align_labels, batched=True)

################# Préparation du data collator #################
data_collator = DataCollatorForTokenClassification(tokenizer)

################# Chargement de la métrique d'évaluation 'seqeval' #################
metric = evaluate.load("seqeval")

################# Fonction de calcul des métriques pour le Trainer #################
def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    true_labels = [
        [id_to_label[l] for l in label if l != -100]
        for label in labels
    ]
    true_predictions = [
        [id_to_label[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]

    results = metric.compute(predictions=true_predictions, references=true_labels)

    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }

################# Configuration des paramètres d'entraînement #################
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

################# Initialisation du Trainer #################
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

################# Lancement de l'entraînement #################
trainer.train()
