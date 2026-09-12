import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

print("=== STAGE 1: Generating Synthetic CAN-Bus Data ===")
np.random.seed(42)
n_samples = 5000

# Normal Vehicle Telemetry (CAN IDs: 0x100 = Speed, 0x200 = RPM, 0x300 = Brake)
timestamps = np.linspace(0, 500, n_samples)
can_ids = np.random.choice([0x100, 0x200, 0x300], size=n_samples, p=[0.4, 0.4, 0.2])
data_bytes = np.random.randint(0, 256, size=(n_samples, 8))
labels = np.zeros(n_samples) # 0 = Normal

# Inject Cyber Attacks (~20% of traffic)
# Attack 1: DoS Flood (High-frequency 0x000 CAN IDs)
dos_indices = np.random.choice(n_samples, size=300, replace=False)
can_ids[dos_indices] = 0x000
labels[dos_indices] = 1 # 1 = Attack

# Attack 2: Throttle Spoofing (Max byte values on 0x100)
spoof_indices = np.random.choice(n_samples, size=300, replace=False)
can_ids[spoof_indices] = 0x100
data_bytes[spoof_indices] = 255
labels[spoof_indices] = 1

# Attack 3: Fuzzing (Random CAN IDs)
fuzz_indices = np.random.choice(n_samples, size=400, replace=False)
can_ids[fuzz_indices] = np.random.randint(0x400, 0x7FF, size=400)
labels[fuzz_indices] = 1

print(f"Generated {n_samples} CAN frames with {int(sum(labels))} injected attacks.")

print("\n=== STAGE 2: Extracting Features ===")
df = pd.DataFrame(data_bytes, columns=[f"byte_{i}" for i in range(8)])
df["can_id"] = can_ids
df["delta_time"] = np.diff(timestamps, prepend=0)

X = df
y = labels

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\n=== STAGE 3: Training Detection Models ===")

# Model 1: Random Forest
print("Training Random Forest Classifier...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_preds = rf_model.predict(X_test)

# Model 2: Multi-Layer Perceptron (Neural Network)
print("Training Neural Network (MLP)...")
nn_model = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=200, random_state=42)
nn_model.fit(X_train, y_train)
nn_preds = nn_model.predict(X_test)

# Model 3: Isolation Forest (Unsupervised Anomaly Detector)
print("Training Isolation Forest Anomaly Detector...")
iso_model = IsolationForest(contamination=0.2, random_state=42)
iso_model.fit(X_train)
iso_raw = iso_model.predict(X_test)
iso_preds = np.where(iso_raw == -1, 1, 0)

print("\n=== STAGE 4: Evaluation Results ===")

def evaluate_model(name, y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)
    fpr = cm[0][1] / (cm[0][1] + cm[0][0]) if (cm[0][1] + cm[0][0]) > 0 else 0
    print(f"{name:18} | Acc: {acc:.3f} | Recall: {rec:.3f} | F1: {f1:.3f} | FPR: {fpr*100:.1f}%")

print(f"{'Model':18} | {'Accuracy':8} | {'Recall':6} | {'F1-Score':8} | {'False Alarms':12}")
print("-" * 65)
evaluate_model("Random Forest", y_test, rf_preds)
evaluate_model("Neural Net (MLP)", y_test, nn_preds)
evaluate_model("Isolation Forest", y_test, iso_preds)

print("\nProcessing complete!")