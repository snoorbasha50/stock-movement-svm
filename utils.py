def load_model_and_scaler(model_path='backend/model.pkl', scaler_path='backend/scaler.pkl'):
    import joblib
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler


def predict_direction(features, model, scaler):
    scaled_features = scaler.transform(features)
    prediction = model.predict(scaled_features)
    return '📈 Buy' if prediction[0] == 1 else '📉 Sell'