import json
import os
import time

import ollama
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

MODEL_NAME = "llama3.2"
DATA_PATH = "data/takemeter_pokemon_dataset.csv"
OUTPUT_PATH = "outputs/ollama_baseline_results.json"

LABELS = [
    "strategy_advice",
    "hot_take",
    "reaction",
    "team_help_question",
]


def build_prompt(text):
    return f"""
You are classifying Pokémon gaming discussion posts.

Choose exactly one label:

strategy_advice
hot_take
reaction
team_help_question

Definitions:

strategy_advice:
Gives useful gameplay advice, matchup reasoning, team-building logic, or explanation.

hot_take:
Makes a strong opinion or claim with little supporting evidence.

reaction:
Primarily expresses emotion, excitement, frustration, surprise, or celebration.

team_help_question:
Asks for help choosing, building, improving, or evaluating a Pokémon team, Pokémon, move, item, or strategy.

Return only the label name. Do not explain.

Post:
{text}
""".strip()


def normalize_label(raw_output):
    raw_output = raw_output.strip().lower()

    for label in LABELS:
        if raw_output == label:
            return label

    for label in LABELS:
        if label in raw_output:
            return label

    return "unparseable"


def classify_with_ollama(text):
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": build_prompt(text)}
        ],
        options={
            "temperature": 0
        }
    )

    raw_output = response["message"]["content"]
    return normalize_label(raw_output)


def main():
    os.makedirs("outputs", exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    train_df, temp_df = train_test_split(
        df,
        test_size=0.30,
        random_state=42,
        stratify=df["label"]
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        random_state=42,
        stratify=temp_df["label"]
    )

    y_true = []
    y_pred = []
    wrong_examples = []

    print(f"Running Ollama baseline on {len(test_df)} test examples...")
    print(f"Model: {MODEL_NAME}")
    print()

    for index, row in test_df.iterrows():
        text = row["text"]
        true_label = row["label"]

        pred_label = classify_with_ollama(text)

        y_true.append(true_label)
        y_pred.append(pred_label)

        print(f"True: {true_label:<20} Predicted: {pred_label}")

        if pred_label != true_label:
            wrong_examples.append({
                "text": text,
                "true_label": true_label,
                "predicted_label": pred_label
            })

        time.sleep(0.2)

    accuracy = accuracy_score(y_true, y_pred)

    report_text = classification_report(
        y_true,
        y_pred,
        labels=LABELS,
        zero_division=0
    )

    report_dict = classification_report(
        y_true,
        y_pred,
        labels=LABELS,
        output_dict=True,
        zero_division=0
    )

    matrix = confusion_matrix(y_true, y_pred, labels=LABELS)

    results = {
        "baseline_type": "local_ollama_zero_shot",
        "model": MODEL_NAME,
        "accuracy": round(accuracy, 4),
        "labels": LABELS,
        "classification_report": report_dict,
        "confusion_matrix": matrix.tolist(),
        "wrong_examples": wrong_examples,
        "test_set_size": len(test_df)
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print()
    print("=" * 50)
    print("OLLAMA BASELINE RESULTS")
    print("=" * 50)
    print(f"Accuracy: {accuracy:.3f}")
    print()
    print(report_text)
    print("Confusion matrix:")
    print(matrix)
    print()
    print(f"Wrong predictions: {len(wrong_examples)} / {len(test_df)}")
    print(f"Saved results to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()