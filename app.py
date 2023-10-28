from flask import Flask, render_template, request
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler


app = Flask(__name__)

# Load all the models
models = {
    "LogisticRegression": joblib.load("LogisticRegression.pkl"),
    "RandomForest": joblib.load("RandomForest.pkl"),
    "XGBoost": joblib.load("XGBoost.pkl"),
    "SupportVectorMachine": joblib.load("SupportVectorMachine.pkl"),
    "EnsembleModel": joblib.load("EnsembleModel.pkl")
}

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/predict', methods=['POST'])
def predict():
    data = [request.form.get(column) for column in [
        "CreditScore", "GeographyID", "GenderID", "Age", "Tenure", 
        "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember", 
        "EstimatedSalary"
    ]]
    data_array = np.array(data, dtype=object).reshape(1, -1)
    print(data)
    
    predictions = {}
    for model_name, model in models.items():
        predictions[model_name] = model.predict(data_array)[0]
    
    # You can process the predictions dictionary as needed.
    # For simplicity, let's take a majority vote approach:
    exited = sum(predictions.values())
    if exited > len(models)/2:
        result = "Customer Exited"
    else:
        result = "Customer Stayed"
    
    return render_template("home.html", prediction=result)

if __name__ == "__main__":
    app.run(debug=True)
