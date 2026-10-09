import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

def load_data():
    BASE_DIR = Path(__file__).resolve().parent.parent
    data_path = BASE_DIR / "data" / "PhiUSIIL_Phishing_URL_Dataset.csv"
    df = pd.read_csv(data_path)

    #print(data.head())

    # Check dataset
    #print(data.isnull().sum())

    # SELECT the features
    feature_cols = [
        'URLLength', 'DomainLength', 'IsDomainIP',
        'CharContinuationRate', 'TLDLength', 'NoOfSubDomain',
        'HasObfuscation', 'NoOfObfuscatedChar', 'ObfuscationRatio',
        'NoOfLettersInURL', 'LetterRatioInURL', 'NoOfDegitsInURL', 'DegitRatioInURL',
        'NoOfEqualsInURL', 'NoOfQMarkInURL', 'NoOfAmpersandInURL',
        'NoOfOtherSpecialCharsInURL', 'SpacialCharRatioInURL', 'IsHTTPS'
    ]
    
    df_clean = df.dropna(subset=feature_cols + ['label'])  # Drop rows with NaN in feature columns or label

    # Select the features
    X = df_clean[feature_cols]

    # Select the target, 0= phishing, 1=legitimate
    y = df_clean["label"]

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