import numpy as np
from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer, AutoModelForTokenClassification, DataCollatorForTokenClassification, Trainer, TrainingArguments
import evaluate

# --- 1. Définir si on attribue une étiquette à tous les sous-tokens ---
label_all_tokens = True  # True : on étiquette tous les sous-tokens ; False : uniquement le premier sous-token

# --- 2. Fonction de conversion des labels pour adapter à notre modèle ---
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

# --- 3. Définition des labels uniques et des mappings label <-> id ---
unique_labels = ["O", "B-ORG", "I-ORG"]
label_to_id = {label: i for i, label in enumerate(unique_labels)}
id_to_label = {i: label for label, i in label_to_id.items()}

# --- 4. Chargement du tokenizer et du modèle BERT de base ---
model_name = "bert-base-cased"  # ici, j'utilise le modèle de base mais pas le modèle de NER
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name, num_labels=len(unique_labels))

# --- 5. Exemple de dataset minimal (à remplacer par votre propre dataset) ---
train_data = {
    "tokens": [["sennheiser", "hd"], ["sony", "headphones"]],
    "labels": [["B-BRAND", "I-BRAND"], ["B-BRAND", "O"]],
}
validation_data = {
    "tokens": [["beats", "studio"]],
    "labels": [["B-BRAND", "O"]],
}

# Conversion en DatasetDict compatible avec Hugging Face Datasets
train_dataset = Dataset.from_dict(train_data)
eval_dataset = Dataset.from_dict(validation_data)
datasets = DatasetDict({"train": train_dataset, "validation": eval_dataset})

# --- 6. Tokenization et alignement des labels ---
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

# --- 7. Préparation du data collator ---
data_collator = DataCollatorForTokenClassification(tokenizer)

# --- 8. Chargement de la métrique d'évaluation 'seqeval' ---
metric = evaluate.load("seqeval")

# --- 9. Fonction de calcul des métriques pour le Trainer ---
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

# --- 10. Configuration des paramètres d'entraînement ---
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)

# --- 11. Initialisation du Trainer ---
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

# --- 12. Lancement de l'entraînement ---
trainer.train()

# --- 13. Évaluation finale ---
trainer.evaluate()
