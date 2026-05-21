import json
from datetime import datetime
from config import FOOD_DATABASE

def calculate_nutrition(food_name, portion):
    """
    Calculate nutrition for a food item
    Returns: dict with kalori, protein, karbo, lemak
    
    PORTION to GRAMS conversion:
    0.25 porsi = 50g
    0.5 porsi  = 100g  
    0.75 porsi = 150g
    1.0 porsi  = 200g
    
    FOOD_DATABASE values are PER 100 GRAM
    """
    food_lower = food_name.lower().strip()
    portion_float = float(portion)
    
    
    grams = portion_float * 200
    
    
    matched_food = None
    
    
    for db_key, nutrients in FOOD_DATABASE.items():
        db_key_lower = db_key.lower()
        if db_key_lower == food_lower or food_lower in db_key_lower or db_key_lower in food_lower:
            matched_food = nutrients
            break
    
    
    if not matched_food:
        
        food_words = set(food_lower.split())
        
        best_match_score = 0
        best_match_nutrients = None
        
        for db_key, nutrients in FOOD_DATABASE.items():
            db_words = set(db_key.lower().split())
            
            
            common_words = food_words.intersection(db_words)
            match_score = len(common_words)
            
            if match_score > best_match_score:
                best_match_score = match_score
                best_match_nutrients = nutrients
        
        if best_match_score >= 1:  
            matched_food = best_match_nutrients
    
    
    if not matched_food:
       
        if any(word in food_lower for word in ['ayam', 'daging', 'ikan', 'sapi', 'babi', 'udang', 'cumi']):
            matched_food = {'kalori': 150, 'protein': 25, 'karbo': 0, 'lemak': 8}
        elif any(word in food_lower for word in ['nasi', 'roti', 'mie', 'pasta', 'kentang', 'bubur', 'lontong']):
            matched_food = {'kalori': 130, 'protein': 3, 'karbo': 28, 'lemak': 1}
        elif any(word in food_lower for word in ['tempe', 'tahu', 'kedelai']):
            matched_food = {'kalori': 150, 'protein': 16, 'karbo': 9, 'lemak': 8}
        elif any(word in food_lower for word in ['sayur', 'brokoli', 'wortel', 'bayam', 'kangkung', 'kol', 'selada', 'kacang panjang']):
            matched_food = {'kalori': 35, 'protein': 2, 'karbo': 7, 'lemak': 0.3}
        elif any(word in food_lower for word in ['buah', 'apel', 'pisang', 'jeruk', 'mangga', 'semangka', 'anggur', 'pepaya']):
            matched_food = {'kalori': 60, 'protein': 1, 'karbo': 15, 'lemak': 0.3}
        elif any(word in food_lower for word in ['susu', 'yogurt', 'keju', 'mentega']):
            matched_food = {'kalori': 60, 'protein': 3, 'karbo': 5, 'lemak': 3.2}
        elif any(word in food_lower for word in ['goreng', 'gorengan', 'fried']):
            matched_food = {'kalori': 250, 'protein': 8, 'karbo': 20, 'lemak': 15}
        elif any(word in food_lower for word in ['bakar', 'panggang', 'grilled']):
            matched_food = {'kalori': 180, 'protein': 25, 'karbo': 2, 'lemak': 8}
        elif any(word in food_lower for word in ['rebus', 'kukus', 'steamed', 'boiled']):
            matched_food = {'kalori': 120, 'protein': 15, 'karbo': 10, 'lemak': 4}
        else:
           
            matched_food = {'kalori': 100, 'protein': 8, 'karbo': 12, 'lemak': 4}
    
    
    nutrition = {}
    for nutrient, value_per_100g in matched_food.items():
        
        nutrition[nutrient] = round((value_per_100g / 100) * grams, 1)
    
    return nutrition

def get_nutrient_percentage(current, required):
    """Calculate percentage of requirement met"""
    if required > 0:
        percentage = (current / required) * 100
        
        return round(percentage, 1)
    return 0

def get_progress_color(percentage):
    """Get color for progress bar based on percentage"""
    if percentage >= 100:
        return '#2196F3'  
    elif percentage >= 80:
        return '#4CAF50'  
    elif percentage >= 50:
        return '#FF9800'  
    else:
        return '#F44336'  

def format_date(date_string):
    """Format date for display"""
    try:
        dt = datetime.strptime(date_string, '%Y-%m-%d')
        return dt.strftime('%d %b %Y')
    except:
        return date_string

def safe_round(value, decimals=1):
    """Safely round a value"""
    try:
        return round(float(value), decimals)
    except:
        return 0.0

def get_portion_in_grams(portion):
    """Convert portion to grams"""
    try:
        portion_float = float(portion)
        return int(portion_float * 200)
    except:
        return 100  

def estimate_food_weight(food_name):
    """Estimate typical weight of food for better accuracy"""
    food_lower = food_name.lower()
    
    
    weight_estimates = {
        'telur': 50,           
        'pisang': 120,         
        'apel': 150,           
        'jeruk': 130,          
        'mangga': 200,         
        'tahu': 150,           
        'tempe': 100,          
        'ayam': 100,           
        'ikan': 150,           
        'nasi': 100,           
        'roti': 50,            
    }
    
    for food, weight in weight_estimates.items():
        if food in food_lower:
            return weight
    
    return 100  