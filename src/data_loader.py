import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from .feature_extractor import extract_features_from_dataset

def load_data():
    BASE_DIR = Path(__file__).resolve().parent.parent
    data_path = BASE_DIR / "data" / "url_dataset.csv"
    df = pd.read_csv(data_path)

    # Extract features from raw URLs using the same pipeline as inference dataset
    X, y_df = extract_features_from_dataset(df, url_col='url', label_col='type', label_map={'phishing': 0, 'legitimate': 1})

    # Select the target, 0= phishing, 1=legitimate
    y = y_df['label']

    # Split the data
    # Training 70%, Validation 15%, Test 15%
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)

    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp)

    return X_train, X_val, X_test, y_train, y_val, y_test

#test if it works
if __name__ == "__main__":
    X_train, X_val, X_test, y_train, y_val, y_test = load_data()
    print("Training:", X_train.shape)
    print("Validation:", X_val.shape)
    print("Test:", X_test.shape)