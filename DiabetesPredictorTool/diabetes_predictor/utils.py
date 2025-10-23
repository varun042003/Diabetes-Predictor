import re

def is_valid_email(email):
    """
    Validate if the provided string is a valid email address.
    
    Args:
        email: String to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Simple regex for email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))

def is_strong_password(password):
    """
    Validate if the provided password is strong.
    Requires at least 8 characters, one uppercase, one lowercase, and one number.
    
    Args:
        password: String to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if len(password) < 8:
        return False
    
    # Check for at least one uppercase letter
    if not any(char.isupper() for char in password):
        return False
    
    # Check for at least one lowercase letter
    if not any(char.islower() for char in password):
        return False
    
    # Check for at least one digit
    if not any(char.isdigit() for char in password):
        return False
    
    return True

def normalize_input_data(data):
    """
    Normalize input data to ensure it's in the correct format.
    
    Args:
        data: Dictionary containing form data
        
    Returns:
        dict: Normalized data
    """
    normalized = {}
    
    # Convert string values to appropriate types
    for key, value in data.items():
        if key in ['pregnancies', 'age']:
            normalized[key] = int(value) if value else 0
        elif key in ['glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi', 'diabetes_pedigree']:
            normalized[key] = float(value) if value else 0.0
        else:
            normalized[key] = value
    
    return normalized
