# Import dataset

import pandas as pd
from sklearn.model_selection import train_test_split

def load_data():
    data = pd.read_csv("src/PhiUSIIL_Phishing_URL_Dataset.csv")

    #print(data.head())

    # Check dataset
    #print(data.isnull().sum())


    # SELECT the features
    X = data[["URLLength", "DomainLength", "IsDomainIP", "NoOfQMarkInURL", "NoOfEqualsInURL", "NoOfAmpersandInURL", "NoOfOtherSpecialCharsInURL", "NoOfDegitsInURL"]]

    # Select the target, 0= phishing, 1=legitimate
    y = data["label"]

    # Split the data
    # Training 70%, validation 15%, Test 15%
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30, random_state=42)

    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42)
    
    return X_train, X_val, X_test, y_train, y_val, y_test

#test if it works
if __name__ == "__main__":
    X_train, X_val, X_test, y_train, y_val, y_test = load_data()
    print("Training:", X_train.shape)
    print("Validation:", X_val.shape)
    print("Test:", X_test.shape)