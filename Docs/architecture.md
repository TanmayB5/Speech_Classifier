# Architecture

## Pipeline

```
Input Text
    ↓
Text Normalization (utils.py)
    ↓
Sentence Embedding (paraphrase-MiniLM-L3-v2)
    ↓
SVM Classifier (RBF kernel)
    ↓
OOS Rejection (confidence + margin check)
    ↓
Predicted Command or "unknown"
```

## How it works

The input text first goes through normalization — lowercase, punctuation removed, filler words like "um" and "uh" stripped out, contractions expanded. This makes sure the model sees clean input even if the user speaks casually or the ASR adds noise.

After normalization, the text is passed to paraphrase-MiniLM-L3-v2 which converts it into a 384-dimensional vector. This is the embedding — it captures the meaning of the sentence so similar phrases end up close together in the vector space. This is why "turn it down" and "lower the volume" both work even though the words are different.

The SVM then takes this vector and predicts which command it belongs to. It also gives probability scores for each class which we use for the OOS rejection step.

If the top probability is below 0.45 or the gap between top-1 and top-2 is less than 0.10, we reject the input as unknown. This handles out-of-scope queries that the classifier would otherwise force into a wrong class.

## Why I chose this stack

I tried a few options and settled on SentenceTransformer + SVM because it was the simplest thing that actually worked well. The embedding model is only 17MB and runs fast on CPU. Training the SVM takes a few seconds even with 370 examples. And I didn't need to write any neural network training code which would have been much harder to get right.

The main tradeoff is that the embedding model is fixed — I can't fine-tune it on this specific domain. But for 14 commands with clean paraphrases it works well enough.

## Files

- `utils.py` — normalization, used by all other scripts
- `commands.py` — all training phrases
- `train.py` — trains and saves the model
- `evaluate.py` — runs all evaluation tests
- `export_onnx.py` — ONNX export and INT8 quantization
- `run.py` — demo and interactive mode
- `threshold_experiment.py` — tests different thresholds
- `extension_analysis.py` — checks if extension commands break existing ones

## Edge deployment

The SVM is exported to ONNX which can run without Python dependencies on mobile or embedded devices. The ONNX file is only 0.54MB. The embedding model is the bigger piece at 17MB but that's still well under the 25MB limit.

Inference latency for the ONNX classifier alone is under 1ms on CPU. The embedding step adds around 50ms but that's mostly model loading overhead.
