import numpy as np
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForTokenClassification, DataCollatorForTokenClassification, Trainer, TrainingArguments
import evaluate
import pandas as pd

from collections import Counter

label_all_tokens = True

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

# Les labels après convertir
unique_labels = ["O", "B-ORG", "I-ORG"]
label_to_id = {label: i for i, label in enumerate(unique_labels)}
id_to_label = {i: label for label, i in label_to_id.items()}

model_path = "../../models/results/checkpoint-7482"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForTokenClassification.from_pretrained(model_path, num_labels=len(unique_labels))

def load_and_group(path):
    df = pd.read_csv(path)
    df = df[df["token"].apply(lambda x: isinstance(x, str) and x.strip() != "text")]
    df = df[df["label"].apply(lambda x: isinstance(x, str) and len(x.strip()) > 0)]
    df["sentence_id"] = df["sentence_id"].astype(int)

    ### test : 
    print("Raw label distribution in dataset:", Counter(df["label"]))

    grouped = {
        "tokens": df.groupby("sentence_id")["token"].apply(list).tolist(),
        "labels": df.groupby("sentence_id")["label"].apply(list).tolist(),
    }
    return Dataset.from_dict(grouped)

test_dataset = load_and_group("../../data/clean/test.csv")

def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True, padding=True, max_length=128)
    all_labels = examples["labels"]
    new_labels = []
    for i, labels in enumerate(all_labels):
        converted_labels = convert_labels(labels)

        ### test
        if i < 2:
            print(f"Original labels: {labels}")
            print(f"Converted labels: {converted_labels}")

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

tokenized_test = test_dataset.map(tokenize_and_align_labels, batched=True)

data_collator = DataCollatorForTokenClassification(tokenizer)

metric = evaluate.load("seqeval")

def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    ### test
    print("Predictions sample:", predictions[0])
    print("Labels sample:", labels[0])

    true_labels = [
        [id_to_label[l] for l in label if l != -100]
        for label in labels
    ]
    true_predictions = [
        [id_to_label[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]

    ### test
    print("True labels example:", true_labels[0])
    print("True predictions example:", true_predictions[0])

    results = metric.compute(predictions=true_predictions, references=true_labels)

    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }

training_args = TrainingArguments(
    output_dir="./test_output",
    per_device_eval_batch_size=16,
    do_eval=True,
    logging_dir="./logs",
)

trainer = Trainer(
    model=model,
    args=training_args,
    eval_dataset=tokenized_test,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

results = trainer.evaluate()
print(results)

import json
with open("./test_output/evaluation.json", "w") as f:
    json.dump(results, f, indent=4)