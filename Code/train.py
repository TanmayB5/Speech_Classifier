import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# build training data from the command dicts
sentences, labels = [], []

for label, phrases in COMMANDS.items():
    for p in phrases:
        sentences.append(normalize_text(p))
        labels.append(label)

for label, phrases in EXTENSION_COMMANDS.items():
    for p in phrases:
        sentences.append(normalize_text(p))
        labels.append(label)

for p in OUT_OF_SCOPE:
    sentences.append(normalize_text(p))
    labels.append("unknown")

print(len(sentences), "examples,", len(set(labels)), "classes")

model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
embeddings = model.encode(sentences, show_progress_bar=True)

X_train, X_test, y_train, y_test = train_test_split(
    embeddings, labels, test_size=0.2, random_state=42, stratify=labels
)
print(f"train={len(X_train)} test={len(X_test)}")

# C=1 was underfitting, C=10 worked better
clf = SVC(kernel='rbf', C=10, gamma='scale', probability=True, random_state=42)
clf.fit(X_train, y_train)

print("train acc:", round(accuracy_score(y_train, clf.predict(X_train))*100, 2))
print("test acc: ", round(accuracy_score(y_test, clf.predict(X_test))*100, 2))
print()
print(classification_report(y_test, clf.predict(X_test)))

with open('classifier.pkl', 'wb') as f:
    pickle.dump(clf, f)
model.save('embedding_model')
print("done - saved classifier.pkl and embedding_model/")