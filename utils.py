
import joblib
import numpy as np
import pandas as pd
import shap
from sklearn.preprocessing import StandardScaler
import os

# Load model and associated data using absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model", "model_data.pkl")

print(f"DEBUG: Attempting to load model from {model_path}")

try:
    if not os.path.exists(model_path):
        # Alternative path for different container structures
        model_path = os.path.join(BASE_DIR, "backend", "model", "model_data.pkl")
        print(f"DEBUG: Trying alternative path: {model_path}")
        
    model_data = joblib.load(model_path)
    model = model_data['model']
    scaler = model_data['scaler']
    features = model_data['features']
    columns_to_scale = model_data['cols_to_scale']
    print("DEBUG: Model loaded successfully.")
except Exception as e:
    print(f"CRITICAL ERROR loading model: {str(e)}")
    # Provide dummy variables to prevent immediate crash on import
    model = scaler = features = columns_to_scale = None

# Initialize SHAP explainer lazily
explainer = None

def get_explainer():
    global explainer
    if explainer is None and model is not None:
        try:
            print("DEBUG: Initializing SHAP explainer...")
            explainer = shap.Explainer(model)
            print("DEBUG: SHAP explainer initialized.")
        except Exception as e:
            print(f"ERROR initializing SHAP explainer: {str(e)}")
    return explainer

def data_preparation(age, avg_dpd_per_dm, credit_utilization_ratio, dmtlm, income, 
                     loan_amount, loan_tenure_months, total_loan_months, 
                     loan_purpose, loan_type, residence_type):
    data_input = {
        'age': age,
        'avg_dpd_per_dm': avg_dpd_per_dm,
        'credit_utilization_ratio': credit_utilization_ratio,
        'dmtlm': dmtlm,
        'income': income,
        'loan_amount': loan_amount,
        'lti': loan_amount / income if income > 0 else 0,
        'total_loan_months': total_loan_months,
        'loan_tenure_months': loan_tenure_months,
        'loan_purpose_Education': 1 if loan_purpose == 'Education' else 0,
        'loan_purpose_Home': 1 if loan_purpose == 'Home' else 0,
        'loan_purpose_Personal': 1 if loan_purpose == 'Personal' else 0,
        'loan_type_Unsecured': 1 if loan_type == 'Unsecured' else 0,
        'residence_type_Owned': 1 if residence_type == 'Owned' else 0,
        'residence_type_Rented': 1 if residence_type == 'Rented' else 0
    }
    
    df = pd.DataFrame([data_input])
    for feat in features:
        if feat not in df.columns:
            df[feat] = 0
            
    df[columns_to_scale] = scaler.transform(df[columns_to_scale])
    df = df[features]
    return df

def get_rating(score):
    if 300 <= score < 500: return 'Poor'
    elif 500 <= score < 650: return 'Average'
    elif 650 <= score < 750: return 'Good'
    elif 750 <= score <= 900: return 'Excellent'
    return 'Undefined'

def calculate_credit_score(input_df, base_score=300, scale_length=600):
    default_probability = model.predict_proba(input_df)[:, 1][0]
    non_default_probability = 1 - default_probability
    credit_score = base_score + non_default_probability * scale_length
    rating = get_rating(credit_score)
    return float(default_probability), int(credit_score), rating

def get_shap_explanations(input_df):
    exp = get_explainer()
    if exp is None:
        return [("Error", "Model not loaded")]
    shap_values = exp(input_df)
    vals = shap_values.values[0]
    explanations = dict(zip(features, vals))
    sorted_explanations = sorted(explanations.items(), key=lambda x: abs(x[1]), reverse=True)
    return sorted_explanations

def _predict_core(age, avg_dpd_per_dm, credit_utilization_ratio, dmtlm, income, 
                  loan_amount, loan_tenure_months, total_loan_months, 
                  loan_purpose, loan_type, residence_type):
    input_df = data_preparation(age, avg_dpd_per_dm, credit_utilization_ratio, dmtlm, income, 
                                loan_amount, loan_tenure_months, total_loan_months, 
                                loan_purpose, loan_type, residence_type)
    return calculate_credit_score(input_df)

def generate_recourse(current_params):
    _, _, current_rating = _predict_core(**current_params)
    ratings_order = ['Poor', 'Average', 'Good', 'Excellent']
    if current_rating == 'Excellent': return None
    
    target_rating_idx = ratings_order.index(current_rating) + 1
    actionable = {'loan_amount': -20000, 'income': 20000, 'loan_tenure_months': -12, 'credit_utilization_ratio': -10}
    
    advice = []
    for feat, step in actionable.items():
        temp_params = current_params.copy()
        for i in range(1, 6):
            temp_params[feat] = max(0, current_params[feat] + step * i)
            _, _, new_rating = _predict_core(**temp_params)
            if ratings_order.index(new_rating) >= target_rating_idx:
                diff = temp_params[feat] - current_params[feat]
                direction = "Decrease" if diff < 0 else "Increase"
                advice.append({
                    'feature': feat.replace('_', ' ').title(),
                    'advice': f"{direction} your {feat.replace('_', ' ')} by ₹{abs(int(diff))}" if 'amount' in feat or 'income' in feat else f"{direction} your {feat.replace('_', ' ')} by {abs(int(diff))} units",
                    'target_rating': new_rating
                })
                break
    return advice[:2]

def bulk_predict(df_input):
    """
    Optimized prediction for a batch of inputs (DataFrame).
    """
    # Calculate derived features
    df_input['lti'] = df_input['loan_amount'] / df_input['income']
    df_input['lti'] = df_input['lti'].fillna(0)
    
    # Handle categorical encoding (one-hot)
    df_input['loan_purpose_Education'] = (df_input['loan_purpose'] == 'Education').astype(int)
    df_input['loan_purpose_Home'] = (df_input['loan_purpose'] == 'Home').astype(int)
    df_input['loan_purpose_Personal'] = (df_input['loan_purpose'] == 'Personal').astype(int)
    df_input['loan_type_Unsecured'] = (df_input['loan_type'] == 'Unsecured').astype(int)
    df_input['residence_type_Owned'] = (df_input['residence_type'] == 'Owned').astype(int)
    df_input['residence_type_Rented'] = (df_input['residence_type'] == 'Rented').astype(int)
    
    # Ensure all features exist
    for feat in features:
        if feat not in df_input.columns:
            df_input[feat] = 0
            
    # Scale numerical columns
    df_input[columns_to_scale] = scaler.transform(df_input[columns_to_scale])
    df_input = df_input[features] # Reorder
    
    # Batch predict
    probs = model.predict_proba(df_input)[:, 1]
    scores = 300 + (1 - probs) * 600
    ratings = [get_rating(s) for s in scores]
    
    results = []
    for i in range(len(df_input)):
        results.append({
            'probability': float(probs[i]),
            'credit_score': int(scores[i]),
            'rating': ratings[i]
        })
    return results

def predict(age, avg_dpd_per_dm, credit_utilization_ratio, dmtlm, income, 
            loan_amount, loan_tenure_months, total_loan_months, 
            loan_purpose, loan_type, residence_type):
    input_df = data_preparation(age, avg_dpd_per_dm, credit_utilization_ratio, dmtlm, income, 
                                loan_amount, loan_tenure_months, total_loan_months, 
                                loan_purpose, loan_type, residence_type)
    prob, score, rating = calculate_credit_score(input_df)
    shap_data = get_shap_explanations(input_df)
    
    params = locals()
    params.pop('input_df', None)
    params.pop('prob', None); params.pop('score', None); params.pop('rating', None); params.pop('shap_data', None)
    
    recourse = generate_recourse(params)
    
    return {
        'probability': prob,
        'credit_score': score,
        'rating': rating,
        'shap_explanations': shap_data,
        'recourse_advice': recourse,
        'input_data': input_df.to_dict(orient='records')[0]
    }
