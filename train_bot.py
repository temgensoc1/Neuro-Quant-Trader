import pandas as pd
from sklearn.ensemble import RandomForestClassifier # type: ignore
from sklearn.metrics import accuracy_score # type: ignore
import joblib # type: ignore

# 1. Load the smart data
df = pd.read_csv("smart_eurusd.csv", index_col=0, parse_dates=True)

# 2. Match features exactly to what we created in features.py
features = ['Dist_EMA_20', 'RSI', 'RSI_Change', 'Momentum', 'Range']
X = df[features]
y = df['Target']

# 3. Split data (80% Train, 20% Test)
split = int(len(df) * 0.8)
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

print(f"Training on {len(X_train)} days. Testing on {len(X_test)} days...")

# 4. Initialize the Model
# We increased n_estimators to 200 for more 'experts'
model = RandomForestClassifier(n_estimators=200, max_depth=10, min_samples_split=25, random_state=1)
model.fit(X_train, y_train)

# 5. Accuracy Report
preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)

print("\n--- BOT INTELLIGENCE REPORT ---")
print(f"New Accuracy Score: {acc * 100:.2f}%")

# 6. Save the Brain
joblib.dump(model, "trading_brain.pkl")
print("\nSuccess! Brain saved to trading_brain.pkl")