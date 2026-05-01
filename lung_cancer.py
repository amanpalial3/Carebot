import joblib

# def check(data):
#     model= joblib.load('lung.pkl')
#     result= model.predict([data])
    
#     return result


def check(data):
    # Load the trained model
    model = joblib.load('lung.pkl')
    
    # Get the predicted class (0 or 1) and the probability for each class
    probabilities = model.predict_proba([data])
    
    # For binary classification, probabilities[0][1] gives the probability of class 1 (positive class, lung cancer)
    risk_percentage = probabilities[0][1] * 100  # Multiply by 100 to get percentage
    
    # Predict the class (0 or 1)
    result = model.predict([data])
    
    return result, risk_percentage

