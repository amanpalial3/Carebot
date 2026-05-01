import joblib

def check(data):
    # Load the saved liver disease model
    model = joblib.load('liver.pkl')
    
    # Predict the class (0 = no disease, 1 = disease)
    result = model.predict([data])[0]
    
    # Predict the probability for both classes
    probabilities = model.predict_proba([data])[0]  # [prob_no_disease, prob_disease]
    
    # Convert the "disease" probability to a percentage
    risk_percentage = probabilities[1] * 100
    
    return result, risk_percentage
