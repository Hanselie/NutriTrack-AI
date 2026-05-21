import json
import os
import math
from datetime import datetime, timedelta
from collections import defaultdict

class PersonalNutritionML:
    def __init__(self):
        self.history_file = 'data/personal_history.json'
        self.patterns_file = 'data/eating_patterns.json'
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Create data directory if not exists"""
        os.makedirs('data', exist_ok=True)
    
    def add_meal(self, meal_data):
        """Add a meal to history and update ML patterns"""
        history = self.load_history()
        
        meal_entry = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': meal_data.get('meal_time'),
            'food': meal_data.get('food_name'),
            'portion': float(meal_data.get('portion', 0.5)),
            'nutrition': meal_data.get('nutrition', {}),
            'category': self.categorize_food(meal_data.get('food_name', ''))
        }
        
        history.append(meal_entry)
        self.save_history(history)
        
       
        if len(history) >= 3:
            self.update_patterns()
        
        return meal_entry
    
    def categorize_food(self, food_name):
        """Categorize food into basic categories"""
        food_lower = food_name.lower()
        
        
        categories = {
            'protein': ['ayam', 'ikan', 'telur', 'tempe', 'tahu', 'daging', 'sapi', 'sosis'],
            'karbo': ['nasi', 'roti', 'mie', 'kentang', 'singkong', 'pasta', 'bihun'],
            'sayur': ['brokoli', 'wortel', 'bayam', 'kangkung', 'kol', 'buncis', 'selada'],
            'buah': ['apel', 'pisang', 'jeruk', 'mangga', 'semangka', 'anggur', 'melon'],
            'susu': ['susu', 'yogurt', 'keju', 'susu kedelai']
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in food_lower:
                    return category
        
        
        if any(word in food_lower for word in ['goreng', 'gorengan', 'digoreng']):
            return 'protein' if any(p in food_lower for p in ['ayam', 'ikan', 'daging', 'telur', 'tempe', 'tahu']) else 'karbo'
        
        return 'lainnya'
    
    def load_history(self):
        """Load meal history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self, history):
        """Save meal history to file"""
        
        cutoff_date = datetime.now() - timedelta(days=30)
        
        filtered_history = []
        for meal in history:
            try:
                meal_date = datetime.fromisoformat(meal['timestamp'])
                if meal_date > cutoff_date:
                    filtered_history.append(meal)
            except:
                continue
        
       
        with open(self.history_file, 'w') as f:
            json.dump(filtered_history[-500:], f, indent=2)  
    
    def load_patterns(self):
        """Load ML patterns from file"""
        if os.path.exists(self.patterns_file):
            try:
                with open(self.patterns_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_patterns(self, patterns):
        """Save ML patterns to file"""
        with open(self.patterns_file, 'w') as f:
            json.dump(patterns, f, indent=2)
    
    def calculate_mean(self, numbers):
        """Calculate mean without numpy"""
        if not numbers:
            return 0
        return sum(numbers) / len(numbers)
    
    def calculate_std(self, numbers):
        """Calculate standard deviation without numpy"""
        if len(numbers) < 2:
            return 0
        
        mean = self.calculate_mean(numbers)
        variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
        return math.sqrt(variance)
    
    def update_patterns(self):
        """Update ML patterns based on recent history"""
        history = self.load_history()
        
        if len(history) < 3:
            return
        
        patterns = {
            'favorite_times': {},
            'favorite_categories': {},
            'common_foods': {},
            'meal_intervals': [],
            'daily_totals': {},
            'last_updated': datetime.now().isoformat()
        }
        
        
        cutoff_date = datetime.now() - timedelta(days=30)
        recent_meals = []
        
        for meal in history:
            try:
                meal_date = datetime.fromisoformat(meal['timestamp'])
                if meal_date > cutoff_date:
                    recent_meals.append(meal)
            except:
                continue
        
        if len(recent_meals) < 3:
            return
        
        
        time_counts = defaultdict(int)
        category_counts = defaultdict(int)
        food_counts = defaultdict(int)
        intervals = []
        
        
        recent_meals.sort(key=lambda x: x.get('timestamp', ''))
        
        prev_time = None
        for i, meal in enumerate(recent_meals):
            
            time_counts[meal.get('time', 'unknown')] += 1
            
            
            category = meal.get('category', 'unknown')
            category_counts[category] += 1
            
           
            food = meal.get('food', 'unknown')
            food_counts[food] += 1
            
            
            if prev_time:
                try:
                    curr_time = datetime.fromisoformat(meal['timestamp'])
                    prev_time_obj = datetime.fromisoformat(prev_time)
                    interval_hours = (curr_time - prev_time_obj).seconds / 3600
                    if 1 <= interval_hours <= 24:  
                        intervals.append(interval_hours)
                except:
                    pass
            
            prev_time = meal.get('timestamp')
            
            
            date = meal.get('date', '')
            if date:
                if date not in patterns['daily_totals']:
                    patterns['daily_totals'][date] = {
                        'meals': 0,
                        'total_calories': 0,
                        'total_protein': 0,
                        'total_karbo': 0,
                        'total_lemak': 0
                    }
                
                patterns['daily_totals'][date]['meals'] += 1
                nutrition = meal.get('nutrition', {})
                patterns['daily_totals'][date]['total_calories'] += nutrition.get('kalori', 0)
                patterns['daily_totals'][date]['total_protein'] += nutrition.get('protein', 0)
                patterns['daily_totals'][date]['total_karbo'] += nutrition.get('karbo', 0)
                patterns['daily_totals'][date]['total_lemak'] += nutrition.get('lemak', 0)
        
        
        patterns['favorite_times'] = dict(sorted(time_counts.items(), key=lambda x: x[1], reverse=True))
        patterns['favorite_categories'] = dict(sorted(category_counts.items(), key=lambda x: x[1], reverse=True))
        patterns['common_foods'] = dict(sorted(food_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        
        if intervals:
            patterns['meal_intervals'] = intervals
            patterns['avg_interval_hours'] = round(self.calculate_mean(intervals), 1)
            mean_interval = self.calculate_mean(intervals)
            if mean_interval > 0:
                std_interval = self.calculate_std(intervals)
                patterns['interval_consistency'] = round(100 - (std_interval / mean_interval * 100), 1)
            else:
                patterns['interval_consistency'] = 0
        else:
            patterns['avg_interval_hours'] = 4.0
            patterns['interval_consistency'] = 0
        
        
        patterns['most_common_time'] = max(time_counts.items(), key=lambda x: x[1])[0] if time_counts else 'makan_siang'
        patterns['most_common_category'] = max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else 'protein'
        
        
        if patterns['daily_totals']:
            total_days = len(patterns['daily_totals'])
            avg_calories = sum(d['total_calories'] for d in patterns['daily_totals'].values()) / total_days
            avg_protein = sum(d['total_protein'] for d in patterns['daily_totals'].values()) / total_days
            patterns['daily_averages'] = {
                'kalori': round(avg_calories, 1),
                'protein': round(avg_protein, 1),
                'days_analyzed': total_days
            }
        
        self.save_patterns(patterns)
        return patterns
    
    def get_today_meals(self):
        """Get meals for today"""
        history = self.load_history()
        today = datetime.now().strftime('%Y-%m-%d')
        return [meal for meal in history if meal.get('date') == today]
    
    def get_today_totals(self):
        """Calculate today's nutrient totals"""
        today_meals = self.get_today_meals()
        
        totals = {
            'kalori': 0,
            'protein': 0,
            'karbo': 0,
            'lemak': 0,
        }
        
        for meal in today_meals:
            nutrition = meal.get('nutrition', {})
            for nutrient in totals.keys():
                totals[nutrient] += nutrition.get(nutrient, 0)
        
        return totals
    
    def get_food_recommendations(self, current_totals, requirements):
        """Generate personalized food recommendations"""
        
        FOOD_CATEGORIES = {
            'protein': ['ayam', 'ikan', 'telur', 'tempe', 'tahu'],
            'karbo': ['nasi', 'roti', 'mie', 'kentang'],
            'sayur': ['brokoli', 'wortel', 'bayam', 'kangkung'],
            'buah': ['apel', 'pisang', 'jeruk', 'mangga'],
            'susu': ['susu', 'yogurt', 'keju']
        }
        
        recommendations = []
        today_meals = self.get_today_meals()
        patterns = self.load_patterns()
        
        
        if len(today_meals) == 0:
            current_hour = datetime.now().hour
            
            if 5 <= current_hour <= 10: 
                return [{
                    'type': 'starter',
                    'foods': ['nasi', 'telur', 'sayur'],
                    'reason': 'Mulai hari dengan sarapan sehat',
                    'icon': '🌅'
                }]
            elif 11 <= current_hour <= 14:  
                return [{
                    'type': 'starter',
                    'foods': ['nasi', 'ayam', 'brokoli'],
                    'reason': 'Waktunya makan siang bergizi',
                    'icon': '☀️'
                }]
            elif 17 <= current_hour <= 20: 
                return [{
                    'type': 'starter',
                    'foods': ['ikan', 'tahu', 'sayur'],
                    'reason': 'Saatnya makan malam sehat',
                    'icon': '🌙'
                }]
            else:
                return [{
                    'type': 'starter',
                    'foods': ['buah', 'roti', 'susu'],
                    'reason': 'Mulai catat makanan pertama Anda',
                    'icon': '➕'
                }]
        
       
        deficiencies = []
        for nutrient, required in requirements.items():
            current = current_totals.get(nutrient, 0)
            percentage = (current / required * 100) if required > 0 else 0
            
            if percentage < 70: 
                deficit = required - current
                deficiencies.append({
                    'nutrient': nutrient,
                    'deficit': deficit,
                    'percentage': percentage
                })
        
        if deficiencies:
            deficiencies.sort(key=lambda x: x['deficit'], reverse=True)
            top_deficiency = deficiencies[0]
            
            nutrient_to_category = {
                'protein': 'protein',
                'kalori': 'karbo',
                'karbo': 'karbo',
                'lemak': 'protein',
                'kalsium': 'susu',
                'zat_besi': 'protein',
                'vitamin_c': 'buah'
            }
            
            category = nutrient_to_category.get(top_deficiency['nutrient'], 'protein')
            
            if category in FOOD_CATEGORIES:
                foods = FOOD_CATEGORIES[category]
                
                today_foods = [m['food'].lower() for m in today_meals]
                suggested_foods = [f for f in foods if f not in today_foods][:3]
                
                if suggested_foods:
                    recommendations.append({
                        'type': 'deficiency',
                        'foods': suggested_foods,
                        'reason': f'Kekurangan {top_deficiency["nutrient"]} ({top_deficiency["deficit"]:.1f}g)',
                        'icon': '⚠️'
                    })
        
       
        if patterns and 'favorite_categories' in patterns:
            favorite_cats = list(patterns['favorite_categories'].keys())[:3]
            
            for cat in favorite_cats:
                if cat in FOOD_CATEGORIES:
                    
                    today_categories = [m.get('category', '') for m in today_meals]
                    
                    if cat not in today_categories:
                        foods = FOOD_CATEGORIES[cat]
                        today_foods = [m['food'].lower() for m in today_meals]
                        suggested_foods = [f for f in foods if f not in today_foods][:2]
                        
                        if suggested_foods:
                            recommendations.append({
                                'type': 'habit',
                                'foods': suggested_foods,
                                'reason': f'Biasanya suka {cat}, belum makan hari ini',
                                'icon': '📊'
                            })
                            break
        
        
        if len(today_meals) >= 1:  
            today_categories = set([m.get('category', '') for m in today_meals])
            all_categories = set(FOOD_CATEGORIES.keys())
            missing_categories = all_categories - today_categories
            
            if missing_categories:
                for cat in missing_categories:
                    if cat in FOOD_CATEGORIES:
                        foods = FOOD_CATEGORIES[cat][:2]
                        
                        today_foods = [m['food'].lower() for m in today_meals]
                        suggested_foods = [f for f in foods if f not in today_foods]
                        
                        if suggested_foods:
                            recommendations.append({
                                'type': 'variety',
                                'foods': suggested_foods[:2],
                                'reason': f'Coba {cat} untuk variasi',
                                'icon': '🔄'
                            })
                            break
        
      
        current_hour = datetime.now().hour
        
        if 5 <= current_hour <= 10:
            time_rec = {
                'type': 'time',
                'foods': ['roti', 'telur', 'pisang'],
                'reason': 'Waktu sarapan yang tepat',
                'icon': '🌅'
            }
        elif 11 <= current_hour <= 14:
            time_rec = {
                'type': 'time',
                'foods': ['nasi', 'ayam', 'sayur'],
                'reason': 'Waktu makan siang ideal',
                'icon': '☀️'
            }
        elif 17 <= current_hour <= 20: 
            time_rec = {
                'type': 'time',
                'foods': ['ikan', 'tahu', 'sayur'],
                'reason': 'Makan malam sehat',
                'icon': '🌙'
            }
        else: 
            time_rec = {
                'type': 'time',
                'foods': ['buah', 'yogurt', 'kacang'],
                'reason': 'Waktu camilan sehat',
                'icon': '🍎'
            }
        
        recommendations.append(time_rec)
        
        
        all_nutrients_sufficient = True
        for nutrient, required in requirements.items():
            current = current_totals.get(nutrient, 0)
            percentage = (current / required * 100) if required > 0 else 0
            if percentage < 90: 
                all_nutrients_sufficient = False
                break
        
        if all_nutrients_sufficient and len(today_meals) > 0:
            
            today_foods = [m['food'].lower() for m in today_meals]
            maintenance_foods = []
            
            for category in ['buah', 'sayur', 'susu']:
                if category in FOOD_CATEGORIES:
                    foods = [f for f in FOOD_CATEGORIES[category] if f not in today_foods]
                    if foods:
                        maintenance_foods.append(foods[0])
                        if len(maintenance_foods) >= 3:
                            break
            
            if maintenance_foods:
                recommendations = [{
                    'type': 'maintenance',
                    'foods': maintenance_foods,
                    'reason': 'Nutrisi sudah cukup, pertahankan dengan makanan sehat',
                    'icon': '✅'
                }]
        
        
        seen = set()
        unique_recs = []
        for rec in recommendations:
            rec_key = ','.join(rec['foods'])
            if rec_key not in seen and len(unique_recs) < 3:
                seen.add(rec_key)
                unique_recs.append(rec)
        
        
        if not unique_recs:
            unique_recs.append(time_rec)
        
        return unique_recs
    
    def get_personal_insights(self):
        """Generate personal insights from ML patterns"""
        patterns = self.load_patterns()
        today_meals = self.get_today_meals()
        
        insights = []
        
        if not patterns or len(patterns) <= 1:  
            if len(today_meals) == 0:
                insights.append({
                    'text': 'Mulai tambahkan makanan pertama untuk mendapatkan insight personal',
                    'icon': '📝',
                    'type': 'info'
                })
            else:
                insights.append({
                    'text': 'Tambahkan lebih banyak makanan untuk analisis pola yang akurat',
                    'icon': '📊',
                    'type': 'info'
                })
            return insights
        
      
        if 'interval_consistency' in patterns:
            consistency = patterns['interval_consistency']
            if consistency > 80:
                insights.append({
                    'text': f'Pola makan sangat teratur ({consistency}% konsisten)',
                    'icon': '✅',
                    'type': 'positive'
                })
            elif consistency > 60:
                insights.append({
                    'text': f'Pola makan cukup teratur ({consistency}% konsisten)',
                    'icon': '⚠️',
                    'type': 'neutral'
                })
            else:
                insights.append({
                    'text': 'Pola makan bisa lebih teratur',
                    'icon': '📅',
                    'type': 'suggestion'
                })
        
       
        if 'favorite_categories' in patterns:
            cat_counts = len(patterns['favorite_categories'])
            if cat_counts >= 4:
                insights.append({
                    'text': 'Variasi makanan sangat baik',
                    'icon': '🌈',
                    'type': 'positive'
                })
            elif cat_counts >= 3:
                insights.append({
                    'text': 'Variasi makanan cukup baik',
                    'icon': '👍',
                    'type': 'neutral'
                })
            else:
                insights.append({
                    'text': 'Coba tambah variasi jenis makanan',
                    'icon': '🔄',
                    'type': 'suggestion'
                })
        
        
        if 'daily_averages' in patterns:
            avg_meals = patterns.get('daily_averages', {}).get('meals_per_day', 0)
            if not avg_meals and 'daily_totals' in patterns:
                
                daily_counts = [d['meals'] for d in patterns['daily_totals'].values()]
                avg_meals = self.calculate_mean(daily_counts) if daily_counts else 0
            
            if avg_meals >= 3:
                insights.append({
                    'text': 'Frekuensi makan sudah baik',
                    'icon': '🍽️',
                    'type': 'positive'
                })
            elif avg_meals >= 2:
                insights.append({
                    'text': 'Pertimbangkan untuk makan lebih teratur',
                    'icon': '⏰',
                    'type': 'suggestion'
                })
        
       
        meal_count = len(today_meals)
        if meal_count == 0:
            insights.append({
                'text': 'Belum ada makanan hari ini',
                'icon': '➕',
                'type': 'reminder'
            })
        elif meal_count == 1:
            insights.append({
                'text': 'Baru 1 makanan hari ini',
                'icon': '1️⃣',
                'type': 'reminder'
            })
        elif meal_count >= 3:
            insights.append({
                'text': f'Sudah {meal_count} makanan hari ini',
                'icon': '✅',
                'type': 'positive'
            })
        
        
        if 'most_common_time' in patterns:
            fav_time = patterns['most_common_time']
            insights.append({
                'text': f'Waktu makan favorit: {fav_time.replace("_", " ")}',
                'icon': '❤️',
                'type': 'info'
            })
        
        return insights[:5] 
    
    def predict_next_meal_time(self):
        """Predict next meal TIME (not food) based on patterns"""
        patterns = self.load_patterns()
        today_meals = self.get_today_meals()
        
        if not today_meals:
            return "Segera (belum ada makanan hari ini)"
        
      
        today_meals.sort(key=lambda x: x.get('timestamp', ''))
        last_meal = today_meals[-1]
        
        try:
            last_time = datetime.fromisoformat(last_meal['timestamp'])
            
            
            avg_interval = patterns.get('avg_interval_hours', 4.0)
            next_time = last_time + timedelta(hours=avg_interval)
            
            
            now = datetime.now()
            time_diff = next_time - now
            
            if time_diff.total_seconds() <= 0:
                return "Sekarang"
            elif time_diff.total_seconds() < 3600:  
                minutes = int(time_diff.total_seconds() / 60)
                return f"{minutes} menit lagi"
            else:
                hours = int(time_diff.total_seconds() / 3600)
                return f"{hours} jam lagi"
                
        except:
            return "3-4 jam lagi"
    
    def get_daily_starter_recommendation(self):
        """Get recommendation for starting a new day"""
        today_meals = self.get_today_meals()
        current_hour = datetime.now().hour
        
        
        if len(today_meals) == 0:
            patterns = self.load_patterns()
            
            
            if patterns and 'most_common_time' in patterns and len(patterns) > 1:
                fav_time = patterns['most_common_time']
                if fav_time == 'sarapan' and current_hour < 11:
                    return {
                        'foods': ['roti', 'telur', 'susu'],
                        'reason': f'Biasanya sarapan di waktu ini',
                        'icon': '🍳'
                    }
            
            
            if 5 <= current_hour <= 9:
                return {
                    'foods': ['nasi', 'telur', 'sayur'],
                    'reason': 'Waktu sarapan optimal',
                    'icon': '🌅'
                }
        
        return None
    
    def reset_data(self):
        """Reset all data (for testing)"""
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
        if os.path.exists(self.patterns_file):
            os.remove(self.patterns_file)
        return True