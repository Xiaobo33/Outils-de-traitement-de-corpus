import pandas as pd
# J'utilise la librairie scikit-learn pour split les données directement
from sklearn.model_selection import train_test_split

df = pd.read_csv("../../data/clean/headfi_labeled.csv")

sentence_ids = df['sentence_id'].unique()

# Séparer les données en train 80%, validation 10% et test 10%
train_ids, temp_ids = train_test_split(sentence_ids, test_size=0.2, random_state=42)
val_ids, test_ids = train_test_split(temp_ids, test_size=0.5, random_state=42)

train_df = df[df['sentence_id'].isin(train_ids)]
val_df = df[df['sentence_id'].isin(val_ids)]
test_df = df[df['sentence_id'].isin(test_ids)]

train_df.to_csv("../../data/clean/train.csv", index=False)
val_df.to_csv("../../data/clean/val.csv", index=False)
test_df.to_csv("../../data/clean/test.csv", index=False)

print(f"Train set size: {train_df['sentence_id'].nunique()} sentences")
print(f"Validation set size: {val_df['sentence_id'].nunique()} sentences")
print(f"Test set size: {test_df['sentence_id'].nunique()} sentences")