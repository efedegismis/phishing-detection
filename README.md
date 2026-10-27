# Project Report - Phishing Website Detection

## Problem Statement

### Introduction

Phishing is a common cybersecurity threat in which attackers attempt to trick users into revealing sensitive data and credentials, often as a first step toward credential theft, malware distribution, and other attacks. It involves a four-step process of gaining trust, redirection, gaining data, and executing the attack (Varshney et al., 2024). The first step can be performed in many ways, such as through email spoofing or DNS poisoning, but an easy and increasingly common method is using fake websites (Varshney et al., 2024). Fake websites typically attempt to mimic the appearance of a known legitimate website by copying the source HTML code and using a similar URL (Gupta et al., 2018; Varshney et al., 2024). By gaining trust, an attacker can then prompt the victim to hand over sensitive data.

Traditional phishing detection methods may rely on blacklists or analysis of the web page content. Examples of blacklist-based services include Google Safe Browsing (GSB) and PhishTank. However, these approaches can have limitations such as failing to detect previously unknown phishing websites or requiring additional time and resources. This motivates investigating whether phishing websites can be detected using only characteristics extracted from their URLs.

### Goal

The goal of this project is to investigate whether an application that takes only a URL as input can effectively and accurately identify phishing websites and potentially warn users before visiting them.

To investigate this, we compared four machine learning models:

- Logistic Regression
- Random Forest
- XGBoost
- Support Vector Machine

The project also aims to determine which features of a URL are the most important to consider in phishing detection.

### Research Question

**RQ1.** How effectively can machine learning models detect phishing websites using only features extracted from URLs, and which model offers the best balance between performance and practical feasibility?

**RQ1.1** Which URL features are the most influential in phishing detection?

### Threat Model

- The primary threat actor is an attacker who creates or controls phishing URLs to deceive users into visiting fraudulent websites.
- The attack surface consists of URLs from any source, such as emails or search results that the user might encounter.
- The attacker can control the URL of a phishing website, including its domain name, path, and query parameters.
- Attackers may use deceptive domain names, suspicious URL structures, or obfuscation techniques. They may also construct URLs resembling legitimate websites.
- The proposed countermeasure is a machine learning-based classifier that analyzes URL features to distinguish phishing URLs from legitimate URLs.
- Since the detector only analyzes URL characteristics, it cannot determine the actual behaviour or content of a website. An attacker may construct a normal-looking URL that is incorrectly classified as legitimate by the model.

### Scope

The project focuses exclusively on features extracted directly from URL strings. Webpage source code, website behaviour, and other external information are not included. The project primarily evaluates the classification capabilities of the models rather than implementing and testing a complete user-friendly warning application.

## Project Reference

Our project was initially inspired by the project idea *Phishing Website Detection*, presented during the project startup lecture. We were also influenced by the study *An Effective Phishing Detection Model Based on Character Level Convolutional Neural Network from URL* by Aljofey et al. (2020). The authors demonstrate the potential of URL-only phishing detection, motivating our investigation into whether simpler, traditional machine learning algorithms can provide effective and practical alternatives.

## Documentation of Project

### Datasets

Two datasets were used in this project to investigate machine learning-based detection:

1. The first dataset was obtained from Kaggle and contains 450,176 URLs classified as phishing or legitimate. About 77% of the URLs are legitimate, and 23% are phishing.

2. The second dataset, PhiUSIIL, was obtained from the UCI Machine Learning Repository and contains 235,795 labeled URLs, of which approximately 57% are legitimate and 43% are phishing.

The Kaggle dataset was used for training, validation, and testing, while the PhiUSIIL dataset was used to evaluate how well the models generalize to URLs from a different source. Unlike the Kaggle dataset, PhiUSIIL includes pre-calculated website features. To ensure a consistent approach, we used a feature extractor and applied it to the URLs in both datasets rather than relying on the pre-calculated features. A binary label convention is used to label whether URLs in the datasets are phishing or legitimate, where 0 represents phishing and 1 represents legitimate.

### Data Processing and Feature Extraction

To prepare the datasets for machine learning, data loading and preprocessing functions were implemented in Python.

A shared data loader was implemented in src/data_loader.py to load the training dataset from Kaggle, extract relevant features, and separate the input features from the classification labels. The dataset was divided into training data (70%), validation data (15%), and testing data (15%).

To extract features from each dataset, a feature extraction function was implemented to convert the URL strings into numerical features that could be used by the machine learning models. The extracted features include URL length, domain characteristics, digits, special characters, and other URL-based properties. The selection of the 19 URL-based features was inspired by the research of Aljofey et al. (2020), which investigates phishing detection using URL characteristics and discusses manually engineered features such as those previously mentioned.

**Table 1: Model Features**

| Category | Features | Description |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| URL Structure | URLLength, DomainLength, TLDLength, NoOfSubDomain | Captures long nested subdomains, unusual TLD lengths and URL paths often used in spoofing. |
| Host | IsDomainIP, IsHTTPS | Flags direct IP addressing and whether the URL uses HTTPS. |
| Character | NoOfLettersInURL, LetterRatioInURL, NoOfDegitsInURL, DegitRatioInURL, CharContinuationRate | Distinguishes word-like domain words from machine-generated token strings or hashes. |
| Obfuscation | HasObfuscation, NoOfObfuscatedChar, ObfuscationRatio, NoOfEqualsInURL, NoOfQMarkInURL, NoOfAmpersandInURL, NoOfOtherSpecialCharsInURL, SpacialCharRatioInURL | Measures @ symbols, percent-encoding (%xx) and query parameter (=, ?, &) density. Also whether any obfuscation was detected. |

Finally, for the logistic regression and support vector machine models, the features are normalized with a StandardScaler object from the scikit-learn library, fitted on the training data and applied to all input sets. The other two models, random forest and XGBoost, work without prior input normalization.

### Models and Implementation

The four models were selected to compare different machine learning approaches suitable for binary classification. Logistic Regression and Support Vector Machine were chosen as relatively simple linear classifiers. Random Forest and XGBoost were selected as more complex, tree-based ensemble methods capable of capturing non-linear relationships between URL features. By comparing these approaches, we aimed to investigate whether increased model complexity improves phishing detection and which model offers the best balance between classification performance and computational efficiency.

#### Logistic Regression

Logistic Regression (LR) is a linear classification algorithm that estimates the probability of an observation belonging to a particular class. It uses a sigmoid function to transform its output into a probability between 0 and 1, typically applying a threshold of 0.5 for binary classification.

The Python package scikit-learn was used to implement and train an LR model. Various hyperparameter combinations were tested, but the standard configuration with the default values gave the best results for the validation dataset.

#### Random Forest

Random forest (RF) consists of decision trees, each trained on a bootstrap sample with random feature sub-selection at each split. Every tree sees a different version of the data and slightly different subsets of the features. Prediction of RF is stable and has lower variance because averaging many trees avoids overfitting. It captures non-linear interactions between features and does not require feature scaling because each split compares on a single feature, and the numerical scale of inputs does not matter.

The RF model was implemented using scikit-learn’s RandomForestClassifier. The classifier was then configured with the parameters: number of trees in n_estimators, maximum depth of each tree in max_depth, number of features in each split in max_features, among other parameters.

#### XGBoost

XGBoost is a tree-based machine learning algorithm that builds decision trees sequentially. Unlike Random Forest, where trees are trained independently, each new tree in XGBoost aims to correct the errors made by previous trees, which allows the model to capture complex, non-linear relationships between features and improve classification performance.

The XGBoost model was implemented using the XGBClassifier from the XGBoost Python library. Hyperparameters such as the number of trees (n_estimators), learning rate (learning_rate), and maximum tree depth (max_depth) were configured. Furthermore, unlike Logistic Regression, Support Vector Machines (SVM), and Random Forest, XGBoost utilized a validation set via the eval_set parameter. This allowed the algorithm to monitor validation performance in boosting rounds and execute early stopping (early_stopping_rounds), stopping training automatically to prevent overfitting.

#### Support Vector Machine

Support Vector Machine (SVM) is a supervised learning algorithm that identifies a decision boundary separating different classes.

The SVM model was implemented using scikit-learn. During development, both linear and Radial Basis Function (RBF) kernels were investigated, along with different values of the regularization parameter C, gamma for the RBF kernel, and class weights. The final implementation used LinearSVC(max_iter=5000) with standardized input features.

### Project Structure

The project was implemented in Python using libraries including scikit-learn, pandas, and XGBoost.

The repository is organized as follows:

- The *data* directory should contain the .csv files of the datasets. These are not pushed to the repository because they tend to be large files.
- The *notebooks* directory contains Jupyter notebooks with the training and validation methods for each model, as well as a notebook for comparing the data in the datasets for debugging, and an evaluation notebook, which visualizes and compares the performance of all four models.
- The *saved_models* directory is populated with trained model files when the model-training notebooks are run. These are then used by *final_evaluation.ipynb*.
- The *src* directory contains scripts with shared functions used by all or most of the notebooks.

## Documentation on Testing the Project

### Testing Method

The models were evaluated to investigate their ability to classify previously unseen URLs as phishing or legitimate. To ensure a fair comparison, all four models were trained and tested using the same dataset and data splits. The Kaggle dataset was divided into 70% training, 15% validation, and 15% testing data. All four models were trained using the training set, while the test set was used to evaluate their performance on unseen URLs.

To evaluate how well the models generalize to data from a different source, they were also tested on the PhiUSIIL dataset. The same 19 URL features were extracted from both datasets to ensure consistent input representations.

During development, different model configurations and hyperparameters were explored to investigate their effects on classification performance. For example, the SVM was evaluated using linear and RBF kernels, different regularization parameters, and class weights. The differences in performance between the two datasets also led us to compare their feature distributions and examine whether the features were extracted consistently.

Finally, an additional experiment was conducted where four easily manipulated URL features, IsHTTPS, URLLength, NoOfLettersInURL, and NoOfDegitsInURL, were removed and the models were retrained. This was done to investigate how strongly the models depend on these features and how their removal affects phishing detection.

### Generative AI for Visualization

The visualizations used to present and compare the evaluation results were created with assistance from Claude. This assistance is acknowledged with comments in the corresponding code.

Examples of prompts include: “Visualize the training and accuracy of the following models” and “Create a stacked bar chart comparing feature categories”

### Evaluation Metrics

The following evaluation metrics were used:

- Accuracy: The proportion of correctly classified URLs.

- Phishing recall: The proportion of phishing URLs correctly identified as phishing.

- Legitimate recall: The proportion of legitimate URLs correctly classified as legitimate.

- F1-score: The harmonic mean of precision and recall.

### Results

The four models were evaluated on the test split of the training dataset (Kaggle) and on the independent inference dataset (PhiUSIIL).

**Table 2: Prediction Accuracy and F1 scores**

| Model | Test Accuracy | Test F1 | Inference Accuracy | Inference F1 |
| ---------------------- | ------------- | ------- | ------------------ | ------------ |
| Logistic Regression | 98.71% | 99.16% | 82.75% | 86.90% |
| Support Vector Machine | 98.51% | 99.04% | 79.41% | 84.74% |
| Random Forest | 99.28% | 99.53% | 84.56% | 87.96% |
| XGBoost | 99.07% | 99.40% | 85.28% | 88.60% |

All models achieved high accuracy on the test split of the training dataset, with Random Forest performing best at 99.28%. However, performance decreased when evaluated on the independent dataset. XGBoost achieved the highest inference accuracy of 85.28%, indicating that the model might outperform the others when faced with URLs from different sources.

It is vitally important that as few phishing websites as possible avoid detection, since one wrong classification can lead to data leakage. Therefore, phishing recall was also evaluated.

**Table 3: Phishing Recall**

| Model | Test Phishing Recall | Inference Phishing Recall |
| ---------------------- | -------------------- | ------------------------- |
| Logistic Regression | 94.62% | 59.71% |
| Support Vector Machine | 93.66% | 51.90% |
| Random Forest | 97.12% | 65.74% |
| XGBoost | 96.15% | 65.65% |

Random Forest and XGBoost demonstrated the strongest classification performance, while the differences between datasets challenge generalizing to previously unseen data from a different source.

**Table 4: Training and Prediction Time**

| Model | Training Time (s) | Prediction Time (1k URLs, s) |
| ---------------------- | ----------------- | ---------------------------- |
| Logistic Regression | 0.6848 | 0.0002 |
| Support Vector Machine | 3.0591 | 0.0001 |
| Random Forest | 22.3850 | 0.0332 |
| XGBoost | 2.0828 | 0.0014 |

The prediction times of the models were calculated on 1000 URLs. The Random Forest classifier takes the longest time to train and predict, whereas XGBoost, Support Vector Machine, and Logistic Regression predict faster than they train. This prolonged time may be due to the numerous decision trees built and run in the random forest classifier. The trees stored in memory may slow down data retrieval during inference.

### Feature Importance

The feature importance analysis in the *final_evaluation* notebook showed that the features classified as “easy to manipulate” were generally the most influential across all four models. This suggests that the models rely heavily on URL characteristics that attackers can relatively easily modify, which may affect their reliability in phishing detection.

To investigate how the models are affected by easily manipulated URL characteristics, four features were removed, and the models were retrained. Performance decreased for most models, particularly in phishing recall. However, Random Forest maintained nearly the same phishing recall on the independent dataset, increasing slightly from 65.74% to 66.23%. This suggests that Random Forest can effectively use other URL characteristics to identify phishing websites, even without the four removed features.

### Discussion and Limitations

The results demonstrate that all four machine learning models achieved high accuracy on the Kaggle test dataset, but their performance decreased when evaluated on the PhiUSIIL dataset (Table 2). This shows limitations in how well the models generalize to URLs from different sources. Differences in feature distributions, like URL length and character composition, may have contributed to this decrease. The dataset also contains different proportions of phishing and legitimate URLs, which could have affected the overall accuracy.

From a cybersecurity perspective, the main risk is that phishing URLs are incorrectly classified as legitimate, allowing users to visit malicious websites without receiving a warning. Although Random Forest and XGBoost achieved approximately 85% accuracy on the inference dataset, both failed to identify around 34% of phishing URLs (Table 3). This is why phishing recall is particularly important when evaluating the models.

Another limitation is that attackers can manipulate URL characteristics to avoid detection. For example, attackers may use HTTPS or construct URLs that resemble legitimate websites. This is especially relevant since HTTPS was identified as an influential feature for all models, even though it does not guarantee that a website is trustworthy

### Conclusion

This project investigated the effectiveness of four machine learning models in detecting phishing websites using only URL-based features. The results demonstrate that this approach can achieve high classification accuracy without requiring access to webpage content or external information.

Among the evaluated models, Random Forest and XGBoost achieved the strongest overall results. XGBoost had the highest accuracy in the independent dataset, while Random Forest achieved the highest phishing recall. Considering both detection performance and computational efficiency, XGBoost offered the best overall balance with significantly shorter training time and smaller model size than Random Forest.

The feature importance analysis identified HTTPS usage as particularly influential for Logistic Regression, Random Forest, and XGBoost, whereas the Support Vector Machine relied more on URL length features.

Overall, the project demonstrates that even a relatively simple detection approach based only on URL characteristics can provide meaningful protection against phishing. Although it cannot identify every malicious URL, it offers a lightweight and practical first layer of defense. Future improvements could focus on increasing phishing recall across different datasets and combining URL-based features with additional detection methods to improve reliability.

## References

Aljofey, A., Jiang, Q., Qu, Q., Huang, M., & Niyigena, J.-P. (2020). An Effective Phishing Detection Model Based on Character Level Convolutional Neural Network from URL. Electronics, 9(9), 1514. [https://doi.org/10.3390/electronics9091514](https://doi.org/10.3390/electronics9091514)

Gupta, B. B., Arachchilage, N. A. G., & Psannis, K. E. (2018). Defending against phishing attacks: Taxonomy of methods, current issues and future directions. Telecommunication Systems [https://doi.org/10.1007/s11235-017-0334-z](https://doi.org/10.1007/s11235-017-0334-z)

Mustafavi, H. (2024). Phishing URLs Dataset (450K+ LINKS) [Data set]. Kaggle.

[https://www.kaggle.com/datasets/hassaanmustafavi/phishing-urls-dataset](https://www.kaggle.com/datasets/hassaanmustafavi/phishing-urls-dataset)

Prasad, A., & Chandra, S. (2024). PhiUSIIL Phishing URL (Website). UCI Machine Learning Repository. [https://archive.ics.uci.edu/dataset/967/phiusil-phishing-url-dataset](https://archive.ics.uci.edu/dataset/967/phiusil-phishing-url-dataset)

Varshney, G., Kumawat, R., Varadharajan, V., Tupakula, U., & Gupta, C. (2024). Anti-phishing: A comprehensive perspective. Expert Systems with Applications [https://doi.org/10.1016/j.eswa.2023.122199](https://doi.org/10.1016/j.eswa.2023.122199)

---

### Repository Architecture
```text
phishing-detection/
├── data/                        # Place raw CSV datasets here (.gitkeep preserved)
├── src/                         # Core Python modules
│   ├── __init__.py
│   ├── data_loader.py           # Data loading, splitting, and scaling
│   ├── feature_extractor.py     # Extracting features from URL
│   └── metrics.py               # Shared evaluation and export utility
├── saved_models/                # Trained model binaries (.pkl / .joblib)
├── notebooks/                   # Individual teammate workspaces
│   ├── 01_logistic_regression_model.ipynb
│   ├── 02_svm_model.ipynb
│   ├── 03_random_forest_model.ipynb
│   ├── 04_xgboost_model.ipynb
│   ├── dataset_comparison.ipynb # Comparison of two datasets used
│   └── final_evaluation.ipynb   # Final evaluation of 4 models
├── .gitignore                   # Ignores heavy data, model binaries, and system files
├── README.md                    # Project documentation and setup guide
├── requirements.txt             # Project dependencies
```
#
### Setup & Installation
1. **Clone the Repository**<br/> 
```bash
git clone https://gits-15.sys.kth.se/degismis/compsec-phishing-detection.git
cd compsec-phishing-detection
```
2. **Create and Activate Virtual Environment**<br/> 
* macOS / Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
* Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
3. **Install Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### How to run
1. Make sure the datasets are located in the data/ folder:
   - [url_dataset.csv](https://www.kaggle.com/datasets/hassaanmustafavi/phishing-urls-dataset)
   - [PhiUSIIL_Phishing_URL_Dataset.csv](https://archive.ics.uci.edu/dataset/967/phiusil-phishing-url-dataset)
2. Select the virtual environment (venv) as the Python kernel.
3. Open the notebooks/ folder.
4. Run the notebooks in the following order:
   - 01_logistic_regression.ipynb
   - 02_support_vector_machine.ipynb
   - 03_random_forest.ipynb
   - 04_xgboost.ipynb
   - dataset_comparison.ipynb (optional)
   - final_evaluation.ipynb
5. Run all cells in each notebook from top to bottom.
The trained models are saved in saved_models/, and the final evaluation notebook compares their performance.
