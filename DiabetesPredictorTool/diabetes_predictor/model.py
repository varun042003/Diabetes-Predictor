import numpy as np
import pickle
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Configure logging
logging.basicConfig(level=logging.INFO)

# Sample data from the Pima Indians Diabetes Dataset
def generate_sample_data():
    """Generate a sample dataset based on the Pima Indians Diabetes Dataset structure."""
    # Mean values and standard deviations based on real dataset statistics
    means = [3.8, 120.9, 69.1, 20.5, 79.8, 32.0, 0.47, 33.2]
    stds = [3.4, 32.0, 19.4, 16.0, 115.2, 7.9, 0.3, 11.8]
    
    # Generate 768 samples (same as original dataset size)
    n_samples = 768
    X = np.zeros((n_samples, 8))
    
    for i in range(8):
        X[:, i] = np.random.normal(means[i], stds[i], n_samples)
        
        # Ensure values are positive where it makes sense
        if i < 7:  # All features except age can't be negative
            X[:, i] = np.maximum(0, X[:, i])
    
    # Age should be at least 21
    X[:, 7] = np.maximum(21, X[:, 7])
    
    # Generate labels with realistic distribution (about 35% positive)
    y = np.random.choice([0, 1], size=n_samples, p=[0.65, 0.35])
    
    # Make some correlation between features and labels
    # High glucose tends to indicate diabetes
    for i in range(n_samples):
        if X[i, 1] > 140:  # High glucose
            if np.random.random() < 0.7:
                y[i] = 1
        if X[i, 5] > 35:  # High BMI
            if np.random.random() < 0.6:
                y[i] = 1
    
    return X, y

def create_and_save_model():
    """Create and save a diabetes prediction model."""
    logging.info("Creating a new diabetes prediction model...")
    
    # Generate sample data
    X, y = generate_sample_data()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train a Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    logging.info(f"Model accuracy: {accuracy:.4f}")
    
    # Save both the model and the scaler
    import os.path
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump((model, scaler), f)
    
    logging.info(f"Model saved to {model_path}")
    
    return (model, scaler)

def predict_diabetes(input_data, model_data):
    """
    Predict diabetes risk using the trained model.
    
    Args:
        input_data: List of 8 values [pregnancies, glucose, blood_pressure, skin_thickness, 
                                      insulin, bmi, diabetes_pedigree, age]
        model_data: Tuple of (model, scaler) loaded from the pickle file
    
    Returns:
        int: 0 for no diabetes risk, 1 for diabetes risk
    """
    try:
        # Unpack model and scaler
        model, scaler = model_data
        
        # Convert input to numpy array and reshape
        input_array = np.array(input_data).reshape(1, -1)
        
        # Scale the input data
        input_scaled = scaler.transform(input_array)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        
        logging.info(f"Prediction made: {prediction}")
        return int(prediction)
        
    except Exception as e:
        logging.error(f"Error making prediction: {e}")
        # Return 0 as a default if prediction fails
        return 0

if __name__ == "__main__":
    # If run directly, create and save the model
    create_and_save_model()
