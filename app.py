
#Jalankan program dengan menggunakan: python app.py pada terminal di direktori proyek.


from flask import Flask, render_template, render_template_string, request, jsonify, redirect, url_for
from datetime import datetime, date
import os
from personal_ml import PersonalNutritionML
from utils import calculate_nutrition, get_nutrient_percentage, get_progress_color, safe_round
from config import NUTRIENT_REQUIREMENTS, MEAL_TIMES

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.context_processor
def utility_processor():
    return dict(
        get_progress_color=get_progress_color,
        get_nutrient_percentage=get_nutrient_percentage,
        safe_round=safe_round,
    )


ml_engine = PersonalNutritionML()

@app.route('/')
def index():
    """Main page"""
    
    today_meals = ml_engine.get_today_meals()
    today_totals = ml_engine.get_today_totals()
    
    
    print("=" * 50)
    print("DEBUG DATA SENT TO TEMPLATE:")
    print(f"today_date: {date.today().strftime('%d %B %Y')}")
    print(f"meal_count_today: {len(today_meals)}")
    
   
    main_nutrients = ['kalori', 'protein', 'karbo', 'lemak']
    

    filtered_totals = {k: v for k, v in today_totals.items() if k in main_nutrients}
    
    
    filtered_requirements = {k: v for k, v in NUTRIENT_REQUIREMENTS.items() if k in main_nutrients}
    
   
    percentages = {}
    for nutrient, total in filtered_totals.items():
        requirement = filtered_requirements.get(nutrient, 1)
        percentages[nutrient] = get_nutrient_percentage(total, requirement)
    
    
    recommendations = ml_engine.get_food_recommendations(today_totals, NUTRIENT_REQUIREMENTS)
    
    
    next_meal_prediction = "Belum ada rekomendasi"
    if recommendations and len(recommendations) > 0:
        foods = recommendations[0].get('foods', [])
        if foods:
            next_meal_prediction = ", ".join(foods[:3])
    
    print(f"next_meal_prediction: {next_meal_prediction}")
    
    
    insights = ml_engine.get_personal_insights()
    
    print(f"insights count: {len(insights)}")
    print(f"recommendations count: {len(recommendations) if recommendations else 0}")
    print(f"today meals count: {len(today_meals)}")
    print(f"filtered totals: {filtered_totals}")
    print(f"filtered requirements: {filtered_requirements}")
    print("=" * 50)
    
    return render_template('index.html',
                         today_date=date.today().strftime('%d %B %Y'),
                         meal_times=MEAL_TIMES,
                         requirements=filtered_requirements,  
                         totals=filtered_totals,              
                         percentages=percentages,             
                         meals=today_meals,
                         recommendations=recommendations,
                         insights=insights,
                         next_meal_prediction=next_meal_prediction,
                         meal_count_today=len(today_meals))

@app.route('/add_meal', methods=['POST'])
def add_meal():
    """Add a new meal"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'})
        
        meal_time = data.get('meal_time', '').strip()
        food_name = data.get('food_name', '').strip()
        portion = data.get('portion', '0.5')
        
        if not meal_time or not food_name:
            return jsonify({'success': False, 'error': 'Waktu dan nama makanan harus diisi'})
        
        
        nutrition = calculate_nutrition(food_name, portion)
        
       
        meal_data = {
            'meal_time': meal_time,
            'food_name': food_name,
            'portion': portion,
            'nutrition': nutrition
        }
        
       
        meal_entry = ml_engine.add_meal(meal_data)
        
        return jsonify({
            'success': True,
            'message': 'Makanan berhasil ditambahkan',
            'meal': meal_entry
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/remove_meal/<meal_id>', methods=['POST'])
def remove_meal(meal_id):
    """Remove a meal by ID"""
    try:
        history = ml_engine.load_history()
        original_count = len(history)
        
        
        history = [meal for meal in history if meal.get('id') != meal_id]
        
        if len(history) < original_count:
            ml_engine.save_history(history)
            
            ml_engine.update_patterns()
            
            return jsonify({
                'success': True,
                'message': 'Makanan berhasil dihapus'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Makanan tidak ditemukan'
            })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/reset_today', methods=['POST'])
def reset_today():
    """Reset today's meals"""
    try:
        history = ml_engine.load_history()
        today = date.today().strftime('%Y-%m-%d')
        
        
        filtered_history = [meal for meal in history if meal.get('date') != today]
        
        ml_engine.save_history(filtered_history)
        ml_engine.update_patterns()
        
        return jsonify({
            'success': True,
            'message': 'Data hari ini telah direset'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/reset_all', methods=['POST'])
def reset_all():
    """Reset all data"""
    try:
        success = ml_engine.reset_data()
        if success:
            return jsonify({
                'success': True,
                'message': 'Semua data telah direset'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Gagal mereset data'
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_stats')
def get_stats():
    """Get statistics for AJAX updates"""
    today_meals = ml_engine.get_today_meals()
    today_totals = ml_engine.get_today_totals()
    
    
    main_nutrients = ['kalori', 'protein', 'karbo', 'lemak']
    filtered_totals = {k: v for k, v in today_totals.items() if k in main_nutrients}
    filtered_requirements = {k: v for k, v in NUTRIENT_REQUIREMENTS.items() if k in main_nutrients}
    
    
    percentages = {}
    for nutrient, total in filtered_totals.items():
        requirement = filtered_requirements.get(nutrient, 1)
        percentages[nutrient] = get_nutrient_percentage(total, requirement)
    
    
    insights = ml_engine.get_personal_insights()
    
    return jsonify({
        'success': True,
        'totals': filtered_totals,
        'percentages': percentages,
        'meal_count': len(today_meals),
        'insights': insights[:3] 
    })

@app.route('/test')
def test():
    """Test route untuk debugging template"""
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head><title>Test Template</title></head>
        <body>
            <h1>Test Flask Template Engine</h1>
            <p>Date: {{ test_date }}</p>
            <p>Meal Count: {{ test_count }}</p>
            <p>Next Meal: {{ test_prediction }}</p>
        </body>
        </html>
    """, 
    test_date="10 Desember 2024",
    test_count=5,
    test_prediction="nasi, ayam, sayur")

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint tidak ditemukan'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'success': False, 'error': 'Kesalahan server'}), 500

if __name__ == '__main__':
    
    os.makedirs('data', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
  
    app.jinja_env.autoescape = True
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    
    print("=" * 50)
    print("NutriTrack Personal ML")
    print("=" * 50)
    print(f"Server running at: http://localhost:5000")
    print(f"Test route: http://localhost:5000/test")
    print(f"Data directory: {os.path.abspath('data')}")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)