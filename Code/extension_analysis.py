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

# pairs that could confuse each other
tests = [
    ("increase the volume",     "increase_volume",     "increase vol vs brightness"),
    ("increase the brightness", "increase_brightness", "increase vol vs brightness"),
    ("decrease the volume",     "decrease_volume",     "decrease vol vs brightness"),
    ("decrease the brightness", "decrease_brightness", "decrease vol vs brightness"),
    ("stop the music",          "pause_music",         "stop music vs stop vehicle"),
    ("stop the vehicle",        "stop_vehicle",        "stop music vs stop vehicle"),
    ("stop the car",            "stop_vehicle",        "stop music vs stop vehicle"),
    ("play the music",          "play_music",          "play music vs next song"),
    ("play the next song",      "play_next_song",      "play music vs next song"),
    ("start the engine",        "start_vehicle",       "start vehicle vs play music"),
    ("start playing",           "play_music",          "start vehicle vs play music"),
]

ok = 0
for phrase, expected, group in tests:
    pred, conf = predict(phrase)
    correct = pred == expected
    if correct:
        ok += 1
    mark = "ok" if correct else "FAIL"
    print(f"[{mark}] {group} | '{phrase}' -> {pred} (conf={conf:.2f})")

print(f"\n{ok}/{len(tests)} correct")