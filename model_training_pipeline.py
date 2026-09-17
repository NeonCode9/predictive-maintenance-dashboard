import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, classification_report
import xgboost as xgb
import mlflow
import mlflow.xgboost
import joblib
from datasets import load_dataset

def load_data():
    """
    Attempts to load data from Hugging Face.
    Falls back to a local CSV or generates synthetic data if the HF repo is unavailable.
    """
    print("Attempting to load dataset from Hugging Face (sudhakaryg/data)...")
    try:
        # Load from HF Hub
        dataset = load_dataset("sudhakaryg/data", split="train")
        df = dataset.to_pandas()
        print("Successfully loaded data from Hugging Face.")
    except Exception as e:
        print(f"Failed to load from HF: {e}. Falling back to synthetic generation for demonstration.")
        # Generates a synthetic dataset mimicking the described engine telemetry
        np.random.seed(42)
        n_samples = 5000
        df = pd.DataFrame({
            'Engine_RPM': np.random.randint(500, 2500, n_samples),
            'Lub_Oil_Pressure': np.random.uniform(1.5, 6.0, n_samples),
            'Fuel_Pressure': np.random.uniform(4.0, 8.0, n_samples),
            'Coolant_Pressure': np.random.uniform(1.0, 3.5, n_samples),
            'Lub_Oil_Temperature': np.random.uniform(60.0, 110.0, n_samples),
            'Coolant_Temperature': np.random.uniform(65.0, 105.0, n_samples),
            'Engine_Condition': np.random.choice([0, 1], n_samples, p=[0.4, 0.6]) # 60% faulty bias as per EDA
        })
    return df

def main():
    # 1. Load Data
    df = load_data()
    
    # 2. Prepare Features (X) and Target (y)
    feature_cols = ['Engine_RPM', 'Lub_Oil_Pressure', 'Fuel_Pressure', 
                    'Coolant_Pressure', 'Lub_Oil_Temperature', 'Coolant_Temperature']
    X = df[feature_cols]
    y = df['Engine_Condition']
    
    # 3. Stratified Split (80/20) to maintain the class balance
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 4. Initialize MLflow Experiment
    mlflow.set_experiment("Engine_Predictive_Maintenance")
    
    with mlflow.start_run(run_name="XGBoost_Champion_Model"):
        
        # Hyperparameters prioritizing recall (scale_pos_weight handles imbalance)
        params = {
            "n_estimators": 150,
            "max_depth": 5,
            "learning_rate": 0.1,
            "scale_pos_weight": 1.5, # Penalize False Negatives heavily (missing a failing engine)
            "random_state": 42
        }
        
        # Log parameters
        mlflow.log_params(params)
        
        # 5. Train the Model
        print("Training XGBoost Classifier...")
        model = xgb.XGBClassifier(**params)
        model.fit(X_train, y_train)
        
        # 6. Evaluate the Model
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred) # Primary metric for PdM
        
        print(f"Accuracy: {acc:.4f}")
        print(f"Recall (Sensitivity): {recall:.4f}")
        print("\nClassification Report:\n", classification_report(y_test, y_pred))
        
        # Log metrics to MLflow
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("recall", recall)
        
        # Log the model to MLflow registry
        mlflow.xgboost.log_model(model, "xgboost_model")
        
        # 7. Serialize and save the model locally for Streamlit deployment
        model_path = "xgboost_model.pkl"
        joblib.dump(model, model_path)
        print(f"\nChampion model successfully serialized and saved to {model_path}")

if __name__ == "__main__":
    main()