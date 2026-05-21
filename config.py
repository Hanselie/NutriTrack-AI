"""
Configuration for NutriTrack Personal ML
"""


NUTRIENT_REQUIREMENTS = {
    'kalori': 1200,      
    'protein': 19,       
    'karbo': 130,        
    'lemak': 39,         
    
}


MEAL_TIMES = ['sarapan', 'makan_siang', 'makan_malam', 'camilan']


FOOD_DATABASE = {
    'nasi': {'kalori': 130, 'protein': 2.7, 'karbo': 28, 'lemak': 0.3},
    'nasi goreng': {'kalori': 300, 'protein': 8, 'karbo': 45, 'lemak': 10},
    'ayam': {'kalori': 165, 'protein': 31, 'karbo': 0, 'lemak': 3.6},
    'ayam bakar': {'kalori': 200, 'protein': 30, 'karbo': 0, 'lemak': 8},
    'ayam goreng': {'kalori': 250, 'protein': 25, 'karbo': 10, 'lemak': 15},
    'ikan': {'kalori': 140, 'protein': 20, 'karbo': 0, 'lemak': 6},
    'ikan bakar': {'kalori': 180, 'protein': 22, 'karbo': 0, 'lemak': 9},
    'telur': {'kalori': 155, 'protein': 13, 'karbo': 1.1, 'lemak': 11},
    'telur rebus': {'kalori': 155, 'protein': 13, 'karbo': 1.1, 'lemak': 11},
    'telur goreng': {'kalori': 200, 'protein': 14, 'karbo': 1.5, 'lemak': 15},
    'tempe': {'kalori': 150, 'protein': 20, 'karbo': 8, 'lemak': 8},
    'tempe goreng': {'kalori': 200, 'protein': 19, 'karbo': 10, 'lemak': 12},
    'tahu': {'kalori': 80, 'protein': 10, 'karbo': 2, 'lemak': 5},
    'tahu goreng': {'kalori': 120, 'protein': 11, 'karbo': 3, 'lemak': 8},
    'brokoli': {'kalori': 55, 'protein': 3.7, 'karbo': 11, 'lemak': 0.6},
    'wortel': {'kalori': 41, 'protein': 0.9, 'karbo': 10, 'lemak': 0.2},
    'bayam': {'kalori': 23, 'protein': 2.9, 'karbo': 3.6, 'lemak': 0.4},
    'kangkung': {'kalori': 20, 'protein': 2.6, 'karbo': 3.1, 'lemak': 0.3},
    'apel': {'kalori': 52, 'protein': 0.3, 'karbo': 14, 'lemak': 0.2},
    'pisang': {'kalori': 105, 'protein': 1.3, 'karbo': 27, 'lemak': 0.4},
    'jeruk': {'kalori': 47, 'protein': 0.9, 'karbo': 12, 'lemak': 0.1},
    'mangga': {'kalori': 60, 'protein': 0.8, 'karbo': 15, 'lemak': 0.4},
    'susu': {'kalori': 61, 'protein': 3.3, 'karbo': 4.7, 'lemak': 3.3},
    'yogurt': {'kalori': 59, 'protein': 10, 'karbo': 3.6, 'lemak': 0.4},
    'keju': {'kalori': 402, 'protein': 25, 'karbo': 1.3, 'lemak': 33},
    'roti': {'kalori': 265, 'protein': 9, 'karbo': 49, 'lemak': 3.2},
    'roti gandum': {'kalori': 247, 'protein': 13, 'karbo': 41, 'lemak': 3.4},
    'mie': {'kalori': 150, 'protein': 4, 'karbo': 30, 'lemak': 1},
    'mie goreng': {'kalori': 300, 'protein': 8, 'karbo': 50, 'lemak': 10},
    'kentang': {'kalori': 77, 'protein': 2, 'karbo': 17, 'lemak': 0.1},
    'kentang goreng': {'kalori': 312, 'protein': 3.4, 'karbo': 41, 'lemak': 15},
    'alpukat': {'kalori': 160, 'protein': 2, 'karbo': 9, 'lemak': 15},
    'kacang': {'kalori': 567, 'protein': 26, 'karbo': 16, 'lemak': 49},
    'sosis': {'kalori': 300, 'protein': 12, 'karbo': 2, 'lemak': 27},
    'ubi jalar': {'kalori': 79, 'protein': 1.58, 'karbo': 17.3, 'lemak': 0.38},
    'salmon': {'kalori': 130, 'protein': 22.3, 'karbo': 0, 'lemak': 4.94},
    'kacang rebus': {'kalori': 318, 'protein': 13.5, 'karbo': 21.3, 'lemak': 22},
    'jagung manis': {'kalori': 85, 'protein': 2.79, 'karbo': 14.7, 'lemak': 1.63},
    'buncis': {'kalori': 345, 'protein': 21.6, 'karbo': 59.8, 'lemak': 2.2},
    'labu kuning': {'kalori': 22, 'protein': 0.89, 'karbo': 4.39, 'lemak': 0.14},
    'tomat': {'kalori': 31, 'protein': 0.83, 'karbo': 5.51, 'lemak': 0.63},
    'timun': {'kalori': 16, 'protein': 0.62, 'karbo': 2.95, 'lemak': 0.18},
    'sawi hijau': {'kalori': 27, 'protein': 2.86, 'karbo': 4.67, 'lemak': 0.42},
    'anggur': {'kalori': 93, 'protein': 5.6, 'karbo': 17.3, 'lemak': 2.12},
    'pir': {'kalori': 57, 'protein': 0.36, 'karbo': 15.2, 'lemak': 0.14},
    'semangka': {'kalori': 30, 'protein': 0.61, 'karbo': 7.55, 'lemak': 0.15},
    'pepaya': {'kalori': 43, 'protein': 0.47, 'karbo': 10.8, 'lemak': 0.26},
    'melon': {'kalori': 38, 'protein': 0.82, 'karbo': 8.16, 'lemak': 0.18},
    'kiwi': {'kalori': 65, 'protein': 1.01, 'karbo': 13.8, 'lemak': 0.64},
    'stroberi': {'kalori': 36, 'protein': 0.64, 'karbo': 7.96, 'lemak': 0.22},
    'bakso': {'kalori': 197, 'protein': 21, 'karbo': 8, 'lemak': 9},
    'biskuit': {'kalori': 384, 'protein': 7.14, 'karbo': 72.8, 'lemak': 7.14},
    'sop ayam': {'kalori': 50, 'protein': 1.6, 'karbo': 7.2, 'lemak': 1.7},
    'sayur sop': {'kalori': 51, 'protein': 2.13, 'karbo': 10, 'lemak': 0.21},
    'sapi': {'kalori': 288, 'protein': 26.33, 'karbo': 0, 'lemak': 19.54},
    'bubur': {'kalori': 72, 'protein': 1.5, 'karbo': 15.26, 'lemak': 0.54},
    'bubur kacang hjau': {'kalori': 108, 'protein': 3.54, 'karbo': 17.76, 'lemak': 3.06},
    'bubur ayam': {'kalori': 155, 'protein': 11.48, 'karbo': 15.05, 'lemak': 5.16},
    'mie ayam': {'kalori': 175, 'protein': 6.96, 'karbo': 19.25, 'lemak': 7.81},
    'pisang': {'kalori': 89, 'protein': 1.09, 'karbo': 22.84, 'lemak': 0.33},
    'jeruk': {'kalori': 47, 'protein': 0.94, 'karbo': 11.75, 'lemak': 0.12},
    'oatmeal': {'kalori': 140, 'protein': 5, 'karbo': 24, 'lemak': 3.5},

    
}