import pickle
import csv
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics import accuracy_score

os.makedirs("results", exist_ok=True)

model = SentenceTransformer('embedding_model')
with open('classifier.pkl', 'rb') as f:
    clf = pickle.load(f)

test_data = [
    ("turn down the volume",        "decrease_volume"),
    ("make it louder",              "increase_volume"),
    ("start playing music",         "play_music"),
    ("pause the song",              "pause_music"),
    ("answer the phone",            "pick_up_call"),
    ("reject the call",             "decline_call"),
    ("skip to next track",          "play_next_song"),
    ("go back to previous song",    "play_previous_song"),
    ("do not disturb me",           "activate_dnd"),
    ("turn off do not disturb",     "deactivate_dnd"),
    ("brighten the screen",         "increase_brightness"),
    ("dim the screen",              "decrease_brightness"),
    ("start the engine",            "start_vehicle"),
    ("turn off the car",            "stop_vehicle"),
    ("what is the weather",         "unknown"),
]

oos = [
    "open google maps", "what time is it", "call my wife",
    "set an alarm for 8am", "how far is the nearest hospital",
    "send a message to john", "navigate to home", "read my notifications",
    "turn on bluetooth", "check my calendar",
]

# sweep thresholds - picked 0.45 because its the sweet spot
THRESHOLDS = [0.30, 0.35, 0.40, 0.45, 0.50, 0.60]

def predict_t(text, thresh, margin_thresh=0.10):
    norm = normalize_text(text)
    emb  = model.encode([norm])
    probs = clf.predict_proba(emb)[0]
    top = sorted(probs, reverse=True)
    if top[0] < thresh or (top[0]-top[1]) < margin_thresh:
        return "unknown"
    return clf.predict(emb)[0]

print("thresh     clean_acc    oos_rate     false_rej")
print("-" * 48)

rows = []
y_true = [e for _, e in test_data]

for t in THRESHOLDS:
    preds = [predict_t(p, t) for p, _ in test_data]
    clean_acc = accuracy_score(y_true, preds) * 100

    rej = sum(1 for p in oos if predict_t(p, t) == "unknown")
    oos_rate = rej / len(oos) * 100

    valid = [(p, e) for p, e in zip(preds, y_true) if e != "unknown"]
    frej = sum(1 for p, e in valid if p == "unknown") / len(valid) * 100

    print(f"{t:<10} {clean_acc:<12.1f} {oos_rate:<12.1f} {frej:<12.1f}")
    rows.append({"threshold": t, "clean_acc": round(clean_acc,1),
                 "oos_rate": round(oos_rate,1), "false_rej": round(frej,1)})

with open('results/threshold_results.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print("saved threshold_results.csv")