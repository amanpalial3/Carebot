import joblib




def check(data):
    model = joblib.load('heart_disease_model.pkl')
    probabilities = model.predict_proba([data])
    result = model.predict([data])
    risk_percentage = probabilities[0][1] * 100  # Risk of heart disease (class 1)
    return result, risk_percentage
