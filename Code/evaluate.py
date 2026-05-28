import pickle
import random
import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt


# these thresholds came from threshold_experiment.py
CONF_THRESH  = 0.30
MARGIN_THRESH = 0.05

os.makedirs("results", exist_ok=True)

model = SentenceTransformer('embedding_model')
with open('classifier.pkl', 'rb') as f:
    clf = pickle.load(f)


def predict(text):
    text = normalize_text(text)
    emb = model.encode([text])
    probs = clf.predict_proba(emb)[0]
    top = sorted(probs, reverse=True)
    conf   = top[0]
    margin = top[0] - top[1]
    if conf < CONF_THRESH or margin < MARGIN_THRESH:
        return "unknown", conf, margin
    return clf.predict(emb)[0], conf, margin


# ------- test set -------
test_data = [
    # decrease_volume
    ("make it quieter",                "decrease_volume"),
    ("volume is too high",             "decrease_volume"),
    ("turn it down",                   "decrease_volume"),
    ("it is hurting my ears",          "decrease_volume"),
    ("way too loud in here",           "decrease_volume"),

    # increase_volume
    ("make it louder",                 "increase_volume"),
    ("sound is too low turn it up",    "increase_volume"),
    ("raise the sound",                "increase_volume"),
    ("i can barely hear it",           "increase_volume"),
    ("crank it up",                    "increase_volume"),

    # play_music
    ("start playing",                  "play_music"),
    ("play some music",                "play_music"),
    ("resume music",                   "play_music"),
    ("get some tunes going",           "play_music"),
    ("i want something to listen to",  "play_music"),

    # pause_music
    ("stop the music",                 "pause_music"),
    ("pause it",                       "pause_music"),
    ("music pause karo",               "pause_music"),
    ("cut the music",                  "pause_music"),
    ("hold on stop the song",          "pause_music"),

    # pick_up_call
    ("answer the call",                "pick_up_call"),
    ("pick up",                        "pick_up_call"),
    ("take the call",                  "pick_up_call"),
    ("yes receive it",                 "pick_up_call"),
    ("get that call",                  "pick_up_call"),

    # decline_call
    ("reject the call",                "decline_call"),
    ("ignore the call",                "decline_call"),
    ("cut the call",                   "decline_call"),
    ("not now send it away",           "decline_call"),
    ("do not answer it",               "decline_call"),

    # play_next_song
    ("next song",                      "play_next_song"),
    ("skip this song",                 "play_next_song"),
    ("next track please",              "play_next_song"),
    ("i dont like this one skip it",   "play_next_song"),
    ("move on to the next one",        "play_next_song"),

    # play_previous_song
    ("previous song",                  "play_previous_song"),
    ("go back",                        "play_previous_song"),
    ("pichla gaana chalao",            "play_previous_song"),
    ("that last song was better",      "play_previous_song"),
    ("replay the one before",          "play_previous_song"),

    # activate_dnd
    ("turn on dnd",                    "activate_dnd"),
    ("enable do not disturb",          "activate_dnd"),
    ("disturb mat karo",               "activate_dnd"),
    ("no notifications for now",       "activate_dnd"),
    ("i need some quiet",              "activate_dnd"),

    # deactivate_dnd
    ("turn off dnd",                   "deactivate_dnd"),
    ("disable do not disturb",         "deactivate_dnd"),
    ("dnd band karo",                  "deactivate_dnd"),
    ("i am available now",             "deactivate_dnd"),
    ("notifications back on",          "deactivate_dnd"),

    # increase_brightness
    ("make it brighter",               "increase_brightness"),
    ("brightness up",                  "increase_brightness"),
    ("brightness badao",               "increase_brightness"),
    ("screen is too dark",             "increase_brightness"),
    ("cant see the display",           "increase_brightness"),

    # decrease_brightness
    ("make it dimmer",                 "decrease_brightness"),
    ("brightness down",                "decrease_brightness"),
    ("thoda dim karo",                 "decrease_brightness"),
    ("screen is blinding me",          "decrease_brightness"),
    ("tone down the screen",           "decrease_brightness"),

    # start_vehicle
    ("start the car",                  "start_vehicle"),
    ("engine start",                   "start_vehicle"),
    ("gaadi start karo",               "start_vehicle"),
    ("fire it up",                     "start_vehicle"),
    ("lets get moving start it",       "start_vehicle"),

    # stop_vehicle
    ("stop the car",                   "stop_vehicle"),
    ("engine stop",                    "stop_vehicle"),
    ("gaadi band karo",                "stop_vehicle"),
    ("kill the engine",                "stop_vehicle"),
    ("shut the car off",               "stop_vehicle"),

    # OOS
    ("what is the weather today",      "unknown"),
    ("call mom",                       "unknown"),
    ("open spotify",                   "unknown"),
    ("set an alarm for 7am",           "unknown"),
    ("how far is the nearest hospital","unknown"),
    ("book a cab",                     "unknown"),
    ("what song is this",              "unknown"),
]
print("=" * 60)
print("EVAL 1 — CLEAN TEST")
print("=" * 60)

y_true, y_pred = [], []
for phrase, expected in test_data:
    pred, conf, margin = predict(phrase)
    y_true.append(expected)
    y_pred.append(pred)
    mark = "OK" if pred == expected else "FAIL"
    print(f"  [{mark}] '{phrase}'")
    print(f"        expected={expected}  got={pred}  conf={conf:.2f}  margin={margin:.2f}\n")

clean_acc = accuracy_score(y_true, y_pred)
print(f"clean accuracy: {clean_acc*100:.2f}%\n")
print(classification_report(y_true, y_pred, zero_division=0))

# false rejection = predicted unknown when it shouldnt be
valid = [(p, e) for p, e in zip(y_pred, y_true) if e != "unknown"]
false_rej = sum(1 for p, e in valid if p == "unknown")
print(f"false rejections: {false_rej}/{len(valid)}\n")


# ------- noise -------
PHONETIC = {
    "the": "da", "pause": "paws", "stop": "stap", "start": "staart",
    "answer": "answr", "reject": "rejet", "volume": "volum",
    "music": "musik", "song": "sang", "call": "cal",
    "engine": "engin", "screen": "scren", "previous": "previus",
    "disturb": "distrub", "brightness": "brightnes",
}

def add_noise(text, seed=0):
    random.seed(seed)
    ntype = random.choice(["filler_drop", "phonetic", "reorder", "merge", "repeat"])
    words = text.lower().split()

    if ntype == "filler_drop":
        filler = random.choice(["um", "uh", "like", "okay", "yaar"])
        words = [filler] + words
        if len(words) > 3:
            words.pop(random.randint(1, len(words)-1))

    elif ntype == "phonetic":
        for i, w in enumerate(words):
            if w in PHONETIC:
                words[i] = PHONETIC[w]
                break

    elif ntype == "reorder":
        if len(words) >= 3:
            i = random.randint(0, len(words)-2)
            words[i], words[i+1] = words[i+1], words[i]

    elif ntype == "merge":
        if len(words) >= 2:
            i = random.randint(0, len(words)-2)
            words = words[:i] + [words[i]+words[i+1]] + words[i+2:]

    elif ntype == "repeat":
        i = random.randint(0, len(words)-1)
        words.insert(i, words[i])

    return " ".join(words), ntype


print("=" * 60)
print("EVAL 2 — NOISE TEST")
print("=" * 60)

noise_true, noise_pred = [], []
per_type = {}

for i, (phrase, expected) in enumerate(test_data):
    noisy, ntype = add_noise(phrase, seed=42+i)
    pred, conf, _ = predict(noisy)
    noise_true.append(expected)
    noise_pred.append(pred)
    per_type.setdefault(ntype, []).append(pred == expected)
    mark = "OK" if pred == expected else "FAIL"
    print(f"  [{mark}] original: '{phrase}'")
    print(f"        noisy ({ntype}): '{noisy}'")
    print(f"        expected={expected}  got={pred}  conf={conf:.2f}\n")

noise_acc = accuracy_score(noise_true, noise_pred)
print(f"noise accuracy: {noise_acc*100:.2f}%\n")
for nt, res in per_type.items():
    print(f"  {nt}: {sum(res)}/{len(res)} = {sum(res)/len(res)*100:.0f}%")
print()
print(classification_report(noise_true, noise_pred, zero_division=0))


# ------- OOS rejection -------
oos = [
    "open google maps", "what time is it", "call my wife",
    "set an alarm for 8am", "how far is the nearest hospital",
    "send a message to john", "navigate to home", "read my notifications",
    "turn on bluetooth", "check my calendar",
    "increase bass", "play movie", "open youtube", "check traffic",
]

print("=" * 60)
print("EVAL 3 — OOS REJECTION")
print("=" * 60)

rej_count = 0
for phrase in oos:
    pred, conf, _ = predict(phrase)
    ok = pred == "unknown"
    if ok:
        rej_count += 1
    print(f"  {'REJECTED' if ok else 'WRONG ' + pred} — '{phrase}'  (conf={conf:.2f})")

print(f"\nrejection rate: {rej_count}/{len(oos)} = {rej_count/len(oos)*100:.1f}%\n")


# confusion matrix
labels_all = sorted(set(y_true + y_pred))
cm = confusion_matrix(y_true, y_pred, labels=labels_all)

plt.figure(figsize=(14, 10))
sns.heatmap(cm, annot=True, fmt='d', xticklabels=labels_all,
            yticklabels=labels_all, cmap='Blues')
plt.title('confusion matrix - clean test')
plt.ylabel('true')
plt.xlabel('predicted')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('results/confusion_matrix.png', dpi=150)
print("saved results/confusion_matrix.png")

# save metrics
metrics = {
    "clean_accuracy": round(clean_acc*100, 2),
    "noise_accuracy": round(noise_acc*100, 2),
    "oos_rejection_rate": round(rej_count/len(oos)*100, 1),
    "false_rejection_rate": round(false_rej/len(valid)*100, 1),
    "conf_threshold": CONF_THRESH,
    "margin_threshold": MARGIN_THRESH,
}
with open('results/metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)
print("saved results/metrics.json")