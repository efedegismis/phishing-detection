# CompSec-Phishing-Detection

### Repository Architecture
```text
phishing-detection/
├── data/                    # Place raw CSV datasets here (.gitkeep preserved)
├── src/                     # Core Python modules
│   ├── __init__.py
│   ├── data_loader.py       # Data loading, splitting, and scaling
│   └── metrics.py           # Shared evaluation and export utility
├── saved_models/            # Trained model binaries (.pkl / .joblib)
├── notebooks/               # Individual teammate workspaces
│   ├── 01_logistic_regression_model.ipynb
│   ├── 02_svm_model.ipynb
│   ├── 03_random_forest_model.ipynb
│   └── 04_xgboost_model.ipynb
├── .gitignore               # Ignores heavy data, model binaries, and system files
├── README.md                # Project documentation and setup guide
├── requirements.txt         # Project dependencies
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
