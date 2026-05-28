import pickle
import time
import os
import csv
import numpy as np
from sentence_transformers import SentenceTransformer
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import onnxruntime as rt
from onnxruntime.quantization import quantize_dynamic, QuantType

from utils import normalize_text

os.makedirs("results", exist_ok=True)

print("loading models...")
model = SentenceTransformer('embedding_model')
with open('classifier.pkl', 'rb') as f:
    clf = pickle.load(f)

initial_type = [('float_input', FloatTensorType([None, 384]))]
onnx_model = convert_sklearn(clf, initial_types=initial_type, target_opset=12)

with open('classifier.onnx', 'wb') as f:
    f.write(onnx_model.SerializeToString())
print("saved classifier.onnx")

quantize_dynamic('classifier.onnx', 'classifier_int8.onnx', weight_type=QuantType.QUInt8)
print("saved classifier_int8.onnx")

def get_mb(path):
    return os.path.getsize(path) / (1024 * 1024)

pkl_size  = get_mb('classifier.pkl')
fp32_size = get_mb('classifier.onnx')
int8_size = get_mb('classifier_int8.onnx')

print(f"\nmodel sizes:")
print(f"  classifier.pkl       : {pkl_size:.3f} MB")
print(f"  classifier.onnx      : {fp32_size:.3f} MB")
print(f"  classifier_int8.onnx : {int8_size:.3f} MB")
print(f"  (int8 size is similar to fp32 — expected for SVM, quantization helps more with neural nets)\n")

sess_fp32 = rt.InferenceSession('classifier.onnx')
sess_int8 = rt.InferenceSession('classifier_int8.onnx')

inp_name = sess_fp32.get_inputs()[0].name
out_name = sess_fp32.get_outputs()[0].name

test_phrases = [
    "turn down the volume", "skip to next song",
    "answer the call", "start the engine", "pause the music",
] * 20

def run_benchmark(sess):
    times = []
    for p in test_phrases:
        emb = model.encode([normalize_text(p)]).astype(np.float32)
        t0 = time.perf_counter()
        sess.run([out_name], {inp_name: emb})
        times.append((time.perf_counter() - t0) * 1000)
    return np.mean(times), np.percentile(times, 95)

avg_fp32, p95_fp32 = run_benchmark(sess_fp32)
avg_int8, p95_int8 = run_benchmark(sess_int8)

print("latency (100 runs each):")
print(f"  fp32 — avg: {avg_fp32:.3f}ms  p95: {p95_fp32:.3f}ms")
print(f"  int8 — avg: {avg_int8:.3f}ms  p95: {p95_int8:.3f}ms\n")

acc_phrases = [
    ("turn down the volume",     "decrease_volume"),
    ("make it louder",           "increase_volume"),
    ("start playing music",      "play_music"),
    ("pause the song",           "pause_music"),
    ("answer the phone",         "pick_up_call"),
    ("reject the call",          "decline_call"),
    ("skip to next track",       "play_next_song"),
    ("go back to previous song", "play_previous_song"),
    ("do not disturb me",        "activate_dnd"),
    ("turn off do not disturb",  "deactivate_dnd"),
]

fp32_correct = 0
int8_correct = 0

for phrase, expected in acc_phrases:
    emb = model.encode([normalize_text(phrase)]).astype(np.float32)
    pred_fp32 = sess_fp32.run([out_name], {inp_name: emb})[0][0]
    pred_int8 = sess_int8.run([out_name], {inp_name: emb})[0][0]
    if pred_fp32 == expected:
        fp32_correct += 1
    if pred_int8 == expected:
        int8_correct += 1

fp32_acc = fp32_correct / len(acc_phrases) * 100
int8_acc  = int8_correct / len(acc_phrases) * 100

print(f"accuracy on 10 test phrases:")
print(f"  fp32: {fp32_acc:.0f}%")
print(f"  int8: {int8_acc:.0f}%\n")

print(f"size constraint  (<25MB)   : {'PASS' if int8_size < 25 else 'FAIL'}")
print(f"speed constraint (<1000ms) : {'PASS' if avg_int8 < 1000 else 'FAIL'}\n")

rows = [
    {"stage": "sklearn_pkl", "size_mb": round(pkl_size, 3),  "avg_latency_ms": "-",             "accuracy": round(fp32_acc, 1)},
    {"stage": "onnx_fp32",   "size_mb": round(fp32_size, 3), "avg_latency_ms": round(avg_fp32, 3), "accuracy": round(fp32_acc, 1)},
    {"stage": "onnx_int8",   "size_mb": round(int8_size, 3), "avg_latency_ms": round(avg_int8, 3), "accuracy": round(int8_acc, 1)},
]

with open('results/benchmark.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
print("saved results/benchmark.csv")
