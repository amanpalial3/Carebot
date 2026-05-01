import joblib

# def check(data):
#     model= joblib.load('diabetes.pkl')
#     result= model.predict([data])
#     probabilities = model.predict_proba([data])
#     return probabilities, result
    
    # return result
def check(data):
    model = joblib.load('diabetes.pkl')
    probabilities = model.predict_proba([data])[0]
    result = model.predict([data])[0]
    risk_percentage = round(probabilities[1] * 100, 2)  # Assuming class 1 is "Diabetes"
    return risk_percentage, result
