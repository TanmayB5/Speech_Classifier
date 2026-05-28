# Self Assessment

## What went well

The core classifier works really well. Clean test accuracy is 100% after expanding the training data, and the OOS rejection is also 100% meaning it correctly ignores things like "open google maps" or "call mom". The extension commands (brightness, vehicle) don't interfere with the original 10 commands which I was worried about initially — things like "increase volume" vs "increase brightness" are handled correctly.

Adding the margin threshold (difference between top-1 and top-2 probability) on top of the confidence threshold helped a lot. Earlier I only had the confidence check and was getting false rejections on valid commands like "dont disturb me". The margin check fixed most of that.

The Hinglish phrases in training data also turned out to be useful — "gaana band karo" and "volume badao" both predict correctly without any translation step.

## Where it struggles

Noise robustness is the weakest part. When words get dropped or phonetically corrupted heavily, the embedding loses too much signal and the confidence drops below the threshold. So instead of predicting the wrong class it just rejects — which is technically "safe" but not useful in a real system.

The INT8 quantization didn't really help with size — the ONNX file is basically the same size before and after (0.543 MB vs 0.544 MB). I looked into this and apparently quantization mainly compresses neural network weight matrices. An SVM doesn't have those, it just stores support vectors, so there's almost nothing to compress. I kept it in because the latency is slightly better and the assignment asked for it, but the size benefit isn't there for this type of model.

Two commands — deactivate_dnd and decrease_brightness — were borderline cases in early testing. They would sometimes get rejected as unknown even for clean inputs. Adding more training phrases fixed this mostly but they still have lower confidence scores compared to other commands.

## What I'd improve with more time

Honestly the biggest improvement would be fine-tuning the embedding model on the actual command data instead of using the pretrained weights as-is. Right now the embeddings are good but generic — they weren't trained specifically on voice command paraphrases.

I'd also build a better noise simulation that uses real ASR error patterns from Indian English speech recognition systems instead of hand-coded substitutions. The current noise test is a bit artificial.

For production, Python is not really suitable — the whole pipeline would need to be reimplemented in C++ or Java for actual embedded deployment. The ONNX runtime has C++ APIs so the classifier part is doable, but the sentence-transformers embedding would need to be replaced with something that can run natively on device.

## TFLite vs ONNX

The assignment mentioned TFLite. I used ONNX instead because there's a direct sklearn-to-ONNX converter (skl2onnx) that works in one step. Converting to TFLite would require going sklearn → TensorFlow → TFLite which is more steps and more things that can break. ONNX runtime also supports Android and iOS so it's not really a limitation for mobile deployment.

## Honest score on the rubric

I think the core functionality (classifier, OOS rejection, ONNX export, extension commands) is solid. The documentation and evaluation are thorough. The main gap is noise robustness — if this were being deployed in a real car with actual ASR output, the accuracy would drop more than the clean test numbers suggest.
