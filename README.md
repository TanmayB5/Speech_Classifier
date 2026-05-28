# Speech Command Classifier for Edge Deployment

Built this as part of an internship assignment — a lightweight offline voice command classifier that can run on edge devices like cars or IoT systems. Uses sentence embeddings + SVM, exported to ONNX.

## How it works

Text goes through normalization first (strip filler words, lowercase, fix contractions), then gets converted to a 384-dim embedding using paraphrase-MiniLM-L3-v2, then classified by an SVM. If the confidence is too low or two classes are too close, it returns "unknown" instead of guessing wrong.

More details in `architecture.md`.

## Setup

```bash
pip install sentence-transformers scikit-learn skl2onnx onnxruntime seaborn matplotlib
```

## Running

Train first, then everything else depends on the saved model.

```bash
python code/train.py
python code/evaluate.py
python code/export_onnx.py
python code/run.py
python code/threshold_experiment.py
python code/extension_analysis.py
```

Single command prediction:
```bash
python code/run.py "pause the music"
```

## Commands

10 core + 4 extension commands, 15 classes total including "unknown" for out-of-scope inputs.

| # | Label | Example phrase |
|---|---|---|
| 1 | decrease_volume | "turn it down" |
| 2 | increase_volume | "make it louder" |
| 3 | play_music | "start playing" |
| 4 | pause_music | "pause the song" |
| 5 | pick_up_call | "answer the phone" |
| 6 | decline_call | "reject the call" |
| 7 | play_next_song | "skip to next" |
| 8 | play_previous_song | "go back" |
| 9 | activate_dnd | "do not disturb me" |
| 10 | deactivate_dnd | "turn off dnd" |
| 11 | increase_brightness *(ext)* | "make it brighter" |
| 12 | decrease_brightness *(ext)* | "dim the screen" |
| 13 | start_vehicle *(ext)* | "start the engine" |
| 14 | stop_vehicle *(ext)* | "stop the car" |

## Results

| Metric | Value |
|---|---|
| Test Accuracy | 86.49% |
| Clean Eval Accuracy | 100% |
| Noise Test Accuracy | ~67% |
| OOS Rejection Rate | 100% |
| False Rejection Rate | 0% |

## Benchmark

| Model | Size | Avg Latency |
|---|---|---|
| classifier.pkl | 0.87 MB | — |
| classifier.onnx (FP32) | 0.54 MB | 0.38 ms |
| classifier_int8.onnx (INT8) | 0.54 MB | 0.33 ms |

INT8 size is basically the same as FP32 — this is because quantization works on neural network weights and SVM doesn't have those. Documented in self_assessment.md.

## Limitations

- Noise robustness is weak when too many words get dropped or corrupted
- Embedding model is not fine-tuned on this domain
- Benchmarked on Colab CPU, not actual mobile hardware
- "volume badao" maps to decrease_volume instead of increase_volume — Hinglish support is partial

## Project Structure

```
├── code/
│   ├── commands.py
│   ├── utils.py
│   ├── train.py
│   ├── evaluate.py
│   ├── export_onnx.py
│   ├── run.py
│   ├── threshold_experiment.py
│   └── extension_analysis.py
├── docs/
│   ├── architecture.md
│   ├── self_assessment.md
│   └── example_runs.md
├── results/
│   ├── metrics.json
│   ├── benchmark.csv
│   ├── confusion_matrix.png
│   └── threshold_results.csv
└── Speech_Classifier.ipynb
└── README.md

```
