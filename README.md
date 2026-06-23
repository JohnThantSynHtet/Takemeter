# TakeMeter: Pokémon Discourse Classifier

## Project Overview

TakeMeter is a text classification project that classifies Pokémon gaming discussion posts into four discourse labels: `strategy_advice`, `hot_take`, `reaction`, and `team_help_question`.

The goal of this project is to determine whether a Pokémon-related post is providing strategic advice, expressing a strong opinion, reacting emotionally to gameplay events, or asking for team-building help. A fine-tuned DistilBERT model is compared against a local Ollama zero-shot baseline to evaluate classification performance.

---

## Community Choice

I chose Pokémon gaming discussion because the community contains many different types of discourse. Some users provide detailed strategy advice, some make strong unsupported claims, some react emotionally to gameplay moments, and some ask questions about team building or Pokémon choices.

This variety makes Pokémon communities a good environment for a text classification task.

---

## Label Taxonomy

### strategy_advice

Definition: A post gives useful gameplay advice, reasoning, matchup information, team-building logic, or explanation.

Examples:

1. "Use Tyranitar with Excadrill because Sand Rush gives your team strong speed control in sand."
2. "Keep Stealth Rock on your team because it pressures switches and breaks Focus Sash."

### hot_take

Definition: A post makes a strong opinion or claim with little real evidence.

Examples:

1. "Tyranitar is completely overrated and people only use it because it looks cool."
2. "Competitive Pokémon is mostly luck and barely takes skill."

### reaction

Definition: A post mainly expresses emotion, hype, frustration, surprise, or excitement.

Examples:

1. "NO WAY I finally got the shiny after three days of hunting!"
2. "I cannot believe Stone Edge missed again."

### team_help_question

Definition: A post asks for help choosing, building, improving, or evaluating a Pokémon team, Pokémon, move, item, or strategy.

Examples:

1. "Should I use Tyranitar or Garchomp on my team?"
2. "What is a good partner for Tyranitar?"

---

## Dataset

Dataset size: **200 examples**

The dataset consists of 200 Pokémon-style discussion examples created for this project and manually assigned to one of four discourse categories. The examples were designed to resemble common Pokémon community discourse, including competitive strategy discussion, casual reactions, hot takes, and team-building questions.

The dataset is synthetic/generated rather than scraped from Reddit or another public forum. AI assistance was used to generate Pokémon-style examples, and all examples and labels were manually reviewed before training.

Columns:

- `text`
- `label`
- `notes`

### Labeling Process

1. Defined four mutually exclusive discourse categories.
2. Generated Pokémon-style discussion examples representing each category.
3. Manually reviewed each example and assigned a label.
4. Balanced the dataset to contain 50 examples per label.
5. Split the dataset into train, validation, and test sets.

### Label Distribution

| Label | Count |
|---|---:|
| strategy_advice | 50 |
| hot_take | 50 |
| reaction | 50 |
| team_help_question | 50 |

---

## Difficult Labeling Examples

### Difficult Example 1

Text:

"Avoid four attacking moves on every Pokémon because some teams need utility and recovery."

Possible labels:

- strategy_advice
- hot_take

Final label:

- strategy_advice

Reason:

Although the statement sounds opinionated, it provides actionable team-building guidance and explains why utility and recovery are important.

### Difficult Example 2

Text:

"Competitive Pokémon is mostly luck and barely takes skill."

Possible labels:

- hot_take
- reaction

Final label:

- hot_take

Reason:

The primary purpose is making a strong claim about competitive Pokémon rather than expressing emotion.

### Difficult Example 3

Text:

"Can this team handle stall?"

Possible labels:

- team_help_question
- strategy_advice

Final label:

- team_help_question

Reason:

The user is asking for team evaluation and guidance rather than providing advice.

---

## Fine-Tuning Approach

I fine-tuned `distilbert-base-uncased` for this classification task.

I selected DistilBERT because it is lightweight, efficient, and commonly used for text classification tasks involving relatively small datasets.

### Training Configuration

- Base model: `distilbert-base-uncased`
- Dataset split:
  - Training: 70%
  - Validation: 15%
  - Test: 15%
- Training examples: 140
- Validation examples: 30
- Test examples: 30
- Epochs: 3
- Learning rate: 2e-5
- Batch size: 16

---

## Baseline Model

The original project specification requested a Groq `llama-3.3-70b-versatile` zero-shot baseline. I used a local Ollama `llama3.2` zero-shot baseline instead because I did not use a Groq API key.

### Baseline Configuration

- Platform: Ollama
- Model: `llama3.2`
- Classification method: Zero-shot prompting

The prompt included all four label definitions and instructed the model to return exactly one label.

---

## Evaluation Results

### Overall Accuracy

| Model | Accuracy |
|---|---:|
| Ollama Zero-Shot Baseline | 0.900 |
| Fine-Tuned DistilBERT | 0.533 |

### Fine-Tuned DistilBERT Metrics

| Label | Precision | Recall | F1 |
|---|---:|---:|---:|
| strategy_advice | 0.53 | 1.00 | 0.70 |
| hot_take | 0.00 | 0.00 | 0.00 |
| reaction | 0.53 | 1.00 | 0.70 |
| team_help_question | 0.00 | 0.00 | 0.00 |

### Ollama Baseline Metrics

| Label | Precision | Recall | F1 |
|---|---:|---:|---:|
| strategy_advice | 1.00 | 0.63 | 0.77 |
| hot_take | 0.73 | 1.00 | 0.84 |
| reaction | 1.00 | 1.00 | 1.00 |
| team_help_question | 1.00 | 1.00 | 1.00 |

---

## Confusion Matrix

### Fine-Tuned DistilBERT Confusion Matrix

| True Label | Predicted strategy_advice | Predicted hot_take | Predicted reaction | Predicted team_help_question |
|---|---:|---:|---:|---:|
| strategy_advice | 8 | 0 | 0 | 0 |
| hot_take | 7 | 0 | 0 | 0 |
| reaction | 0 | 0 | 8 | 0 |
| team_help_question | 1 | 0 | 6 | 0 |

The confusion matrix image is included in:

`outputs/confusion_matrix.png`

---

## Wrong Prediction Analysis

### Wrong Prediction 1

Text:

"Can this team handle stall?"

True label: `team_help_question`

Predicted label: `reaction`

Analysis:

The model failed to recognize the question as a request for team evaluation and instead associated the short sentence structure with another category.

### Wrong Prediction 2

Text:

"Competitive Pokémon is mostly luck and barely takes skill."

True label: `hot_take`

Predicted label: `strategy_advice`

Analysis:

The model focused on competitive terminology rather than identifying the statement as an unsupported opinion.

### Wrong Prediction 3

Text:

"What is a good partner for Tyranitar?"

True label: `team_help_question`

Predicted label: `reaction`

Analysis:

The model struggled with short question-based inputs and failed to learn the `team_help_question` category effectively.

---

## Sample Classifications

| Text | Predicted Label | Confidence |
|---|---|---:|
| "NO WAY I finally got the shiny after three days of hunting!" | reaction | 0.27 |
| "Use Tyranitar with Excadrill because Sand Rush gives your team strong speed control in sand." | strategy_advice | 0.28 |
| "Can this team handle stall?" | reaction | 0.26 |
| "Competitive Pokémon is mostly luck and barely takes skill." | strategy_advice | 0.28 |

Correct prediction explanation:

The shiny example was correctly predicted as `reaction` because the text is primarily expressing excitement and celebration.

Incorrect prediction explanation:

"Can this team handle stall?" was incorrectly predicted as `reaction`, even though the true label was `team_help_question`.

---

## Reflection

The fine-tuned DistilBERT model achieved 53.3% accuracy, while the Ollama zero-shot baseline achieved 90.0% accuracy.

The fine-tuned model successfully learned the `strategy_advice` and `reaction` categories but struggled to identify `hot_take` and `team_help_question` examples. This suggests that the dataset was too small and simplistic for effective fine-tuning, while the larger language model already possessed strong semantic understanding of the categories.

If I continued this project, I would collect a larger dataset with more diverse examples and create more challenging edge cases between the categories.

---

## Spec Reflection

### One way the spec helped

The planning phase forced me to clearly define the label taxonomy before collecting data. This improved annotation consistency and made edge cases easier to identify.

### One way my implementation diverged

I used a local Ollama zero-shot baseline instead of the Groq baseline named in the original project specification because I chose not to use a Groq API key.

---

## AI Usage

1. I used AI assistance to help design and refine the Pokémon discourse taxonomy.
2. I used AI assistance to generate the synthetic Pokémon-style discussion examples used in the dataset.
3. I manually reviewed the generated examples and labels before training.
4. I used AI assistance to analyze model errors and identify patterns in wrong predictions.
5. I made the final decisions about label definitions, evaluation analysis, and project conclusions.

---

## How to Run

### Install Dependencies

```bash
pip install transformers datasets evaluate torch scikit-learn pandas ollama
```

### Fine-Tune DistilBERT

1. Open the provided Google Colab notebook.
2. Upload `data/takemeter_pokemon_dataset.csv`.
3. Run Sections 1–4 of the notebook.
4. Download `outputs/confusion_matrix.png`.

### Run Ollama Baseline

Pull the model:

```bash
ollama pull llama3.2
```

Run the baseline:

```bash
python scripts/ollama_baseline.py
```

Results will be saved to:

`outputs/ollama_baseline_results.json`

### Compare Results

Compare:

- Ollama baseline accuracy
- Fine-tuned DistilBERT accuracy
- Per-class precision, recall, and F1 scores
- Wrong prediction examples

to evaluate classification performance.