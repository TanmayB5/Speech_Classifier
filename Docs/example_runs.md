# Example Runs

These are end-to-end example runs from the pipeline showing input text, predicted command, and confidence score. Covers clean, noisy, OOS, and extension command cases.

---

## 1. Clean Input — Core Command

```
$ python run.py "increase the volume"

Input     : increase the volume
Predicted : increase_volume
Confidence: 0.88
```

---

## 2. Noisy Input — Filler Word + Dropped Article

```
$ python run.py "um pause music"

Input     : um pause music
Predicted : pause_music
Confidence: 0.92
```

Filler word "um" stripped by normalization. Missing article "the" handled by semantic embedding.

---

## 3. Out-of-Scope — Must Be Rejected

```
$ python run.py "what is the weather today"

Input     : what is the weather today
Predicted : unknown
Confidence: 0.85
```

Correctly rejected — does not match any known command.

---

## 4. Extension Command

```
$ python run.py "lower brightness"

Input     : lower brightness
Predicted : decrease_brightness
Confidence: 0.79
```

Paraphrase of "decrease the brightness" from the extension command set. Correctly classified despite different phrasing.

---

## 5. Noisy Input — Reordered Phrase

```
$ python run.py "pick the call up"

Input     : pick the call up
Predicted : pick_up_call
Confidence: 0.71
```

Words reordered compared to training phrase "pick up the call". Semantic embedding handles this correctly.

---

## 6. Hard Case — Semantically Close Commands

```
$ python run.py "stop the music"

Input     : stop the music
Predicted : pause_music
Confidence: 0.88

$ python run.py "stop the vehicle"

Input     : stop the vehicle
Predicted : stop_vehicle
Confidence: 0.83
```

Both use "stop the ..." but the target object disambiguates correctly. No interference between extension and core commands.

---

## 7. Indian English / Hinglish Input

```
$ python run.py "gaana band karo"

Input     : gaana band karo
Predicted : pause_music
Confidence: 0.71

$ python run.py "volume badao"

Input     : volume badao
Predicted : increase_volume
Confidence: 0.69
```

Hinglish phrases included in training data. Works without any translation layer.

---

## Notes

- All predictions run fully offline with no network calls
- Inference time is under 1ms for the classifier (ONNX) + ~50ms for embedding generation
- Confidence threshold: 0.45, Margin threshold: 0.10
- Tested on CPU only (no mobile device available — see self_assessment.md)
