import csv

# Dictionnaire des marques
"""
Ici, j'utilise les marques dans mon fichier de NER_100.csv, 
je ne peux pas tag tous les marques manuellement, mais au moins les 100 entités nommées sont inclues.
"""
brand_dict = [
    "sony", "grado","ultrasone","hifiman","denon", "grado", "whxm", "beats", "zmf","meze","fiio","moondrop",
    "sennheiser", "bose","sundara","stax","ipod","cal","fidelio","samson","fostex","xlr","dan clark","verum",
    "arya", "stealth", "clear", "og", "focal", "fender", "titanium", "hd","dac","audeze","focal","auribus",
    "beyer","pioneer","technica","koss", "logitech", "newbie", "shure","planar","akg","audiotechnica","campfire audio"
]

def annotate_tokens(tokens):
    tags = []
    inside_brand = False # si les marques sont dans une entité
    for i, token in enumerate(tokens):
        token_lower = token.lower()
        if token_lower in brand_dict:
            if not inside_brand:
                tags.append("B-BRAND")
                inside_brand = True
            else:
                tags.append("I-BRAND")
        else:
            tags.append("O")
            inside_brand = False  # 断开连续品牌词
    return tags

input_csv_path = "../../data/clean/headfi_merged.csv"
output_csv_path = "../../data/clean/headfi_labeled.csv"

with open(input_csv_path, newline='', encoding="utf-8") as infile, \
     open(output_csv_path, mode='w', newline='', encoding="utf-8") as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    writer.writerow(["sentence_id", "token", "label"])

    sentence_id = 0
    for row in reader:
        if not row or not row[0].strip():
            continue
        tokens = row[0].strip().split()
        labels = annotate_tokens(tokens)
        for token, label in zip(tokens, labels):
            writer.writerow([sentence_id, token, label])
        sentence_id += 1