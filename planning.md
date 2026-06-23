# TakeMeter Planning

## Community

I chose Pokémon gaming discussion as my community. This community is a good fit because Pokémon discussions include strategy advice, strong opinions, emotional reactions, and short low-context questions. These types of posts appear often in Pokémon team-building, Pokémon GO, and general gameplay discussions.

## Label Taxonomy

### strategy_advice

A post is `strategy_advice` if it gives useful gameplay advice, reasoning, matchup information, team-building logic, or explanation.

Examples:
1. "Tyranitar works better if you pair it with a Pokémon that can handle Fighting types."
2. "Rotom is useful here because it gives your team better coverage and can pivot safely."

### hot_take

A post is `hot_take` if it makes a strong opinion or claim with little real evidence.

Examples:
1. "Tyranitar is overrated and people only use it because it looks cool."
2. "That team is trash. You should never run it."

### reaction

A post is `reaction` if it mainly expresses emotion, hype, frustration, surprise, or excitement without much analysis.

Examples:
1. "NO WAY I finally got the shiny!"
2. "That battle was so annoying. I hate this matchup."

### low_effort_question

A post is `low_effort_question` if it asks for help or a decision with very little context.

Examples:
1. "Who should I recruit?"
2. "Is this team good?"

## Hard Edge Cases

Some posts may sit between `strategy_advice` and `hot_take`.

Example:
"Tyranitar is bad because Fighting types destroy it."

This gives one reason, but it is still mostly a strong claim. My decision rule is: if the post explains what to do next or gives useful gameplay reasoning, I will label it `strategy_advice`. If it only makes a strong claim with shallow support, I will label it `hot_take`.

Some posts may sit between `reaction` and `hot_take`.

Example:
"This Pokémon is so broken, I hate fighting it."

My decision rule is: if the main purpose is emotion, I will label it `reaction`. If the main purpose is a claim about strength, balance, or quality, I will label it `hot_take`.

## Data Collection Plan

I will collect at least 200 public Pokémon-related posts or comments. I will use only public text, not private messages or private Discord content.

Target label distribution:
- strategy_advice: about 50 examples
- hot_take: about 50 examples
- reaction: about 50 examples
- low_effort_question: about 50 examples

The dataset will be saved as one CSV file:

data/takemeter_pokemon_dataset.csv

The CSV will have these columns:
- text
- label
- notes

If one label is too common or too rare, I will collect more examples for the weaker labels before training.

## Evaluation Metrics

I will report overall accuracy, precision, recall, and F1 score for each class. Accuracy alone is not enough because the model could perform well overall while failing on one label. Per-class F1 is useful because it shows whether the classifier learned each discourse type.

I will also include a confusion matrix to show which labels the model confuses most often.

## Definition of Success

The classifier will be successful if the fine-tuned DistilBERT model performs better than the local Ollama zero-shot baseline on the same test set.

A useful result would be:
- Overall accuracy of at least 70%
- Most per-class F1 scores at or above 0.65
- Errors that are understandable from the label boundaries

## AI Tool Plan

For label stress-testing, I will ask an AI tool to generate borderline examples between my labels. If I cannot label those examples cleanly, I will revise my definitions before annotating the full dataset.

For annotation assistance, I may ask an AI tool to suggest labels for some examples. However, I will manually review and correct every label myself.

For failure analysis, I will give the wrong predictions to an AI tool and ask it to identify patterns. I will verify the patterns myself before writing them in the README.

## Baseline Plan Change

The original project asks for a Groq zero-shot baseline. I plan to use a local Ollama zero-shot baseline instead. I will document this clearly in the README and compare Ollama against the fine-tuned DistilBERT model on the same test set.