import pickle
from sentence_transformers import SentenceTransformer

CONF_THRESH   = 0.45
MARGIN_THRESH = 0.10

model = SentenceTransformer('embedding_model')
with open('classifier.pkl', 'rb') as f:
    clf = pickle.load(f)

def predict(text):
    norm = normalize_text(text)
    emb  = model.encode([norm])
    probs = clf.predict_proba(emb)[0]
    top = sorted(probs, reverse=True)
    conf, margin = top[0], top[0] - top[1]
    if conf < CONF_THRESH or margin < MARGIN_THRESH:
        return "unknown", conf
    return clf.predict(emb)[0], conf

# demo
demo = [
    ("increase the volume",       "increase_volume"),
    ("um pause music",            "pause_music"),
    ("what is the weather today", "unknown"),
    ("stop the car",              "stop_vehicle"),
    ("make it brighter",          "increase_brightness"),
    ("dont disturb me",           "activate_dnd"),
    ("skip to next track",        "play_next_song"),
    ("open navigation",           "unknown"),
    ("pick the call up",          "pick_up_call"),
    ("lower brightness",          "decrease_brightness"),
]

ok = 0
for text, expected in demo:
    got, conf = predict(text)
    correct = got == expected
    if correct: ok += 1
    mark = "ok" if correct else "FAIL"
    print(f"[{mark}] '{text}' -> {got} (conf={conf:.2f})")

print(f"\n{ok}/{len(demo)} correct")

# try a few extra ones
print("\n-- extra tests --")
extras = [
    "gaana band karo",
    "volume badao",
    "open maps",
    "start the engine",
]
for t in extras:
    label, conf = predict(t)
    print(f"  '{t}' -> {label} (conf={conf:.2f})")