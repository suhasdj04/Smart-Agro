"""
Smart Agro - Crop Recommendation Engine
=========================================
Recommends the best crop based on soil and climate conditions.

Approach:
  1. First tries to load a pre-trained scikit-learn model from ml/models/crop_model.pkl
  2. Falls back to a rule-based scoring system using empirical crop condition tables

Input parameters:
  - soil_type:   Sandy / Loamy / Clay / Silt / Peaty / Chalky
  - temperature: °C
  - rainfall:    mm (annual)
  - humidity:    % (0–100)
  - nitrogen:    kg/ha
  - phosphorus:  kg/ha
  - potassium:   kg/ha
"""

import os
import math
import pickle
import logging

import numpy as np

logger = logging.getLogger(__name__)

# ── Comprehensive crop condition database ──────────────────────────────────────
# Each entry defines the IDEAL conditions for that crop.
# Ranges use (min, ideal_low, ideal_high, max) for scoring.
CROP_DATABASE = {
    'Rice': {
        'soil_types': ['Loamy', 'Clay', 'Silt'],
        'temperature': (18, 22, 30, 38),
        'rainfall': (1000, 1200, 2000, 3000),
        'humidity': (60, 75, 85, 95),
        'nitrogen': (60, 80, 120, 160),
        'phosphorus': (20, 30, 50, 70),
        'potassium': (20, 30, 50, 70),
        'description': 'Staple crop, thrives in warm, wet conditions.',
        'season': 'Kharif',
        'harvest_days': 120,
    },
    'Wheat': {
        'soil_types': ['Loamy', 'Clay', 'Silt'],
        'temperature': (5, 12, 18, 25),
        'rainfall': (300, 450, 650, 900),
        'humidity': (40, 50, 65, 80),
        'nitrogen': (60, 80, 120, 150),
        'phosphorus': (30, 40, 60, 80),
        'potassium': (25, 35, 55, 75),
        'description': 'Cool-season crop, ideal for North Indian plains.',
        'season': 'Rabi',
        'harvest_days': 150,
    },
    'Corn': {
        'soil_types': ['Loamy', 'Sandy', 'Silt'],
        'temperature': (18, 21, 27, 35),
        'rainfall': (500, 600, 900, 1200),
        'humidity': (50, 60, 75, 85),
        'nitrogen': (70, 100, 150, 200),
        'phosphorus': (30, 40, 60, 80),
        'potassium': (30, 40, 60, 80),
        'description': 'High-yielding versatile crop for food and feed.',
        'season': 'Kharif',
        'harvest_days': 90,
    },
    'Cotton': {
        'soil_types': ['Loamy', 'Clay', 'Silt'],
        'temperature': (21, 25, 30, 38),
        'rainfall': (500, 600, 1000, 1400),
        'humidity': (40, 50, 65, 80),
        'nitrogen': (60, 80, 120, 150),
        'phosphorus': (25, 35, 55, 75),
        'potassium': (30, 40, 60, 80),
        'description': 'Cash crop, requires warm climate and well-drained soil.',
        'season': 'Kharif',
        'harvest_days': 180,
    },
    'Sugarcane': {
        'soil_types': ['Loamy', 'Clay', 'Silt'],
        'temperature': (20, 25, 32, 38),
        'rainfall': (1000, 1200, 1800, 2500),
        'humidity': (60, 70, 80, 90),
        'nitrogen': (100, 120, 180, 250),
        'phosphorus': (30, 40, 60, 80),
        'potassium': (60, 80, 120, 160),
        'description': 'Long-duration crop for sugar and ethanol production.',
        'season': 'Annual',
        'harvest_days': 365,
    },
    'Jute': {
        'soil_types': ['Loamy', 'Silt', 'Clay'],
        'temperature': (24, 27, 32, 38),
        'rainfall': (1200, 1500, 2000, 2500),
        'humidity': (70, 80, 90, 95),
        'nitrogen': (60, 80, 100, 130),
        'phosphorus': (20, 30, 45, 60),
        'potassium': (25, 35, 50, 70),
        'description': 'Natural fibre crop, grows in high humidity regions.',
        'season': 'Kharif',
        'harvest_days': 120,
    },
    'Coffee': {
        'soil_types': ['Loamy', 'Sandy', 'Peaty'],
        'temperature': (15, 18, 24, 28),
        'rainfall': (1500, 1800, 2500, 3000),
        'humidity': (70, 75, 85, 95),
        'nitrogen': (40, 60, 90, 120),
        'phosphorus': (20, 30, 50, 70),
        'potassium': (25, 35, 55, 75),
        'description': 'Shade-loving crop grown in high-altitude regions.',
        'season': 'Perennial',
        'harvest_days': 365,
    },
    'Tea': {
        'soil_types': ['Sandy', 'Loamy', 'Peaty'],
        'temperature': (13, 18, 25, 30),
        'rainfall': (1500, 2000, 2500, 3500),
        'humidity': (70, 80, 90, 95),
        'nitrogen': (50, 70, 100, 130),
        'phosphorus': (15, 25, 40, 55),
        'potassium': (20, 30, 50, 70),
        'description': 'Grown in hilly areas with high rainfall and humidity.',
        'season': 'Perennial',
        'harvest_days': 365,
    },
    'Coconut': {
        'soil_types': ['Sandy', 'Loamy'],
        'temperature': (22, 25, 32, 38),
        'rainfall': (1000, 1500, 2000, 2500),
        'humidity': (60, 70, 80, 90),
        'nitrogen': (30, 50, 80, 100),
        'phosphorus': (20, 30, 50, 70),
        'potassium': (60, 100, 150, 200),
        'description': 'Tropical tree crop, tolerates coastal sandy soils.',
        'season': 'Perennial',
        'harvest_days': 365,
    },
    'Mango': {
        'soil_types': ['Loamy', 'Sandy', 'Clay'],
        'temperature': (21, 24, 30, 38),
        'rainfall': (600, 800, 1200, 1800),
        'humidity': (40, 55, 70, 85),
        'nitrogen': (40, 60, 90, 120),
        'phosphorus': (20, 30, 50, 70),
        'potassium': (30, 50, 80, 120),
        'description': 'King of fruits, thrives in tropical and subtropical zones.',
        'season': 'Summer',
        'harvest_days': 100,
    },
    'Banana': {
        'soil_types': ['Loamy', 'Silt', 'Clay'],
        'temperature': (20, 25, 30, 35),
        'rainfall': (1000, 1200, 2000, 2500),
        'humidity': (60, 75, 85, 95),
        'nitrogen': (80, 100, 150, 200),
        'phosphorus': (25, 35, 55, 80),
        'potassium': (80, 120, 180, 250),
        'description': 'High-potassium crop, year-round production possible.',
        'season': 'Perennial',
        'harvest_days': 365,
    },
    'Grapes': {
        'soil_types': ['Sandy', 'Loamy', 'Chalky'],
        'temperature': (15, 18, 24, 30),
        'rainfall': (400, 500, 800, 1200),
        'humidity': (30, 45, 60, 75),
        'nitrogen': (30, 50, 80, 110),
        'phosphorus': (25, 35, 55, 75),
        'potassium': (40, 60, 90, 120),
        'description': 'Vine crop for wine and table use, prefers dry summers.',
        'season': 'Summer',
        'harvest_days': 180,
    },
    'Orange': {
        'soil_types': ['Loamy', 'Sandy', 'Silt'],
        'temperature': (15, 20, 28, 35),
        'rainfall': (600, 800, 1200, 1600),
        'humidity': (50, 60, 75, 85),
        'nitrogen': (40, 60, 90, 120),
        'phosphorus': (20, 30, 50, 70),
        'potassium': (30, 50, 80, 110),
        'description': 'Citrus crop, likes mild winters and warm summers.',
        'season': 'Winter',
        'harvest_days': 180,
    },
    'Apple': {
        'soil_types': ['Loamy', 'Sandy', 'Chalky'],
        'temperature': (5, 10, 18, 24),
        'rainfall': (600, 800, 1000, 1400),
        'humidity': (40, 55, 70, 80),
        'nitrogen': (30, 50, 80, 110),
        'phosphorus': (20, 30, 50, 70),
        'potassium': (30, 50, 80, 110),
        'description': 'Temperate fruit crop, requires cold winters for fruit setting.',
        'season': 'Summer',
        'harvest_days': 150,
    },
    'Watermelon': {
        'soil_types': ['Sandy', 'Loamy'],
        'temperature': (21, 25, 30, 38),
        'rainfall': (400, 500, 800, 1200),
        'humidity': (40, 55, 70, 80),
        'nitrogen': (30, 50, 80, 110),
        'phosphorus': (25, 35, 55, 75),
        'potassium': (25, 35, 55, 75),
        'description': 'Warm season fruit, grows best in sandy loam soils.',
        'season': 'Summer',
        'harvest_days': 85,
    },
    'Muskmelon': {
        'soil_types': ['Sandy', 'Loamy'],
        'temperature': (20, 24, 30, 37),
        'rainfall': (300, 400, 700, 1000),
        'humidity': (35, 50, 65, 75),
        'nitrogen': (30, 50, 80, 110),
        'phosphorus': (25, 35, 55, 75),
        'potassium': (25, 35, 55, 75),
        'description': 'Sweet melon, prefers hot dry weather and well-drained soil.',
        'season': 'Summer',
        'harvest_days': 90,
    },
    'Papaya': {
        'soil_types': ['Sandy', 'Loamy'],
        'temperature': (22, 25, 32, 38),
        'rainfall': (1000, 1200, 1700, 2200),
        'humidity': (60, 70, 80, 90),
        'nitrogen': (60, 80, 120, 160),
        'phosphorus': (30, 40, 60, 80),
        'potassium': (40, 60, 90, 120),
        'description': 'Fast-growing tropical fruit with year-round production.',
        'season': 'Perennial',
        'harvest_days': 240,
    },
    'Pomegranate': {
        'soil_types': ['Loamy', 'Sandy', 'Chalky'],
        'temperature': (18, 22, 28, 38),
        'rainfall': (300, 500, 800, 1200),
        'humidity': (30, 45, 60, 75),
        'nitrogen': (30, 50, 80, 110),
        'phosphorus': (20, 30, 50, 70),
        'potassium': (30, 50, 80, 110),
        'description': 'Drought-tolerant crop suitable for semi-arid regions.',
        'season': 'Summer',
        'harvest_days': 180,
    },
    'Lentil': {
        'soil_types': ['Sandy', 'Loamy', 'Silt'],
        'temperature': (5, 10, 18, 25),
        'rainfall': (200, 300, 500, 700),
        'humidity': (30, 40, 55, 70),
        'nitrogen': (10, 20, 40, 60),
        'phosphorus': (30, 40, 60, 80),
        'potassium': (20, 30, 50, 70),
        'description': 'Cool-season legume, fixes nitrogen in soil.',
        'season': 'Rabi',
        'harvest_days': 110,
    },
    'Chickpea': {
        'soil_types': ['Sandy', 'Loamy', 'Silt'],
        'temperature': (10, 15, 22, 29),
        'rainfall': (300, 400, 600, 900),
        'humidity': (30, 40, 55, 70),
        'nitrogen': (15, 25, 45, 65),
        'phosphorus': (30, 45, 65, 85),
        'potassium': (20, 30, 50, 70),
        'description': 'Protein-rich legume, grows in cool dry conditions.',
        'season': 'Rabi',
        'harvest_days': 100,
    },
    'Mungbean': {
        'soil_types': ['Sandy', 'Loamy'],
        'temperature': (25, 28, 32, 38),
        'rainfall': (600, 700, 1000, 1300),
        'humidity': (50, 60, 75, 85),
        'nitrogen': (15, 25, 45, 65),
        'phosphorus': (25, 35, 55, 75),
        'potassium': (20, 30, 50, 70),
        'description': 'Short-duration warm-season pulse crop.',
        'season': 'Kharif',
        'harvest_days': 70,
    },
    'Blackgram': {
        'soil_types': ['Loamy', 'Clay', 'Silt'],
        'temperature': (25, 28, 32, 38),
        'rainfall': (600, 700, 1000, 1500),
        'humidity': (55, 65, 80, 90),
        'nitrogen': (15, 25, 45, 65),
        'phosphorus': (25, 35, 55, 75),
        'potassium': (20, 30, 50, 70),
        'description': 'High-protein pulse, grows in warm humid conditions.',
        'season': 'Kharif',
        'harvest_days': 75,
    },
    'Pigeonpeas': {
        'soil_types': ['Sandy', 'Loamy', 'Clay'],
        'temperature': (18, 25, 30, 38),
        'rainfall': (600, 800, 1200, 1600),
        'humidity': (50, 60, 75, 85),
        'nitrogen': (15, 25, 45, 65),
        'phosphorus': (30, 40, 60, 80),
        'potassium': (25, 35, 55, 75),
        'description': 'Hardy legume, tolerates drought and poor soils.',
        'season': 'Kharif',
        'harvest_days': 150,
    },
    'Kidneybeans': {
        'soil_types': ['Loamy', 'Sandy', 'Silt'],
        'temperature': (15, 18, 24, 30),
        'rainfall': (600, 800, 1200, 1600),
        'humidity': (50, 60, 75, 85),
        'nitrogen': (15, 25, 45, 65),
        'phosphorus': (30, 40, 60, 80),
        'potassium': (25, 35, 55, 75),
        'description': 'Nutritious legume, prefers moderate temperature.',
        'season': 'Mixed',
        'harvest_days': 100,
    },
    'Mothbeans': {
        'soil_types': ['Sandy', 'Loamy'],
        'temperature': (24, 28, 33, 40),
        'rainfall': (200, 300, 500, 800),
        'humidity': (30, 40, 60, 75),
        'nitrogen': (10, 20, 40, 60),
        'phosphorus': (20, 30, 50, 70),
        'potassium': (20, 30, 50, 70),
        'description': 'Extremely drought-tolerant pulse for arid regions.',
        'season': 'Kharif',
        'harvest_days': 80,
    },
    'Rubber': {
        'soil_types': ['Loamy', 'Sandy', 'Peaty'],
        'temperature': (22, 25, 30, 35),
        'rainfall': (1500, 2000, 2500, 3500),
        'humidity': (70, 80, 90, 95),
        'nitrogen': (40, 60, 90, 120),
        'phosphorus': (15, 25, 40, 60),
        'potassium': (30, 50, 80, 110),
        'description': 'Tropical tree crop for latex production, needs high rainfall.',
        'season': 'Perennial',
        'harvest_days': 365,
    },
}


def _score_range(value: float, range_tuple: tuple) -> float:
    """
    Score a numeric value against an ideal range tuple (min, ideal_low, ideal_high, max).
    Returns a score from 0.0 to 1.0.

    Scoring logic:
      - Inside ideal range → 1.0
      - Between min and ideal_low OR ideal_high and max → linear interpolation
      - Outside min/max → 0.0
    """
    min_val, ideal_low, ideal_high, max_val = range_tuple

    if ideal_low <= value <= ideal_high:
        return 1.0
    elif min_val <= value < ideal_low:
        # Linear scale from 0 at min to 1 at ideal_low
        if ideal_low == min_val:
            return 0.5
        return (value - min_val) / (ideal_low - min_val)
    elif ideal_high < value <= max_val:
        # Linear scale from 1 at ideal_high to 0 at max
        if max_val == ideal_high:
            return 0.5
        return 1.0 - (value - ideal_high) / (max_val - ideal_high)
    else:
        return 0.0  # Completely out of range


def _score_crop(
    crop_name: str,
    crop_data: dict,
    soil_type: str,
    temperature: float,
    rainfall: float,
    humidity: float,
    nitrogen: float,
    phosphorus: float,
    potassium: float
) -> float:
    """
    Calculate an overall suitability score (0–100) for a crop given conditions.
    """
    # Weights for each factor (must sum to 1.0)
    weights = {
        'soil': 0.20,
        'temperature': 0.20,
        'rainfall': 0.20,
        'humidity': 0.15,
        'nitrogen': 0.10,
        'phosphorus': 0.075,
        'potassium': 0.075,
    }

    # Soil type score: 1.0 if compatible, 0.3 if not (can still grow with management)
    soil_score = 1.0 if soil_type in crop_data['soil_types'] else 0.3

    # Numeric factor scores
    temp_score = _score_range(temperature, crop_data['temperature'])
    rain_score = _score_range(rainfall, crop_data['rainfall'])
    hum_score = _score_range(humidity, crop_data['humidity'])
    n_score = _score_range(nitrogen, crop_data['nitrogen'])
    p_score = _score_range(phosphorus, crop_data['phosphorus'])
    k_score = _score_range(potassium, crop_data['potassium'])

    total = (
        soil_score * weights['soil'] +
        temp_score * weights['temperature'] +
        rain_score * weights['rainfall'] +
        hum_score * weights['humidity'] +
        n_score * weights['nitrogen'] +
        p_score * weights['phosphorus'] +
        k_score * weights['potassium']
    )

    return round(total * 100, 2)


def recommend_crop(
    soil_type: str,
    temperature: float,
    rainfall: float,
    humidity: float,
    nitrogen: float,
    phosphorus: float,
    potassium: float
) -> dict:
    """
    Return the best crop recommendation with confidence scores.

    First attempts to use a pre-trained sklearn model if available.
    Falls back to rule-based scoring.

    Args:
        soil_type:   One of Sandy/Loamy/Clay/Silt/Peaty/Chalky
        temperature: In °C
        rainfall:    Annual mm
        humidity:    Percentage 0–100
        nitrogen:    kg/ha
        phosphorus:  kg/ha
        potassium:   kg/ha

    Returns:
        dict with keys: recommended_crop, confidence, season, harvest_days,
                        description, alternatives, method_used
    """
    # ── Try pre-trained model first ────────────────────────────────────────────
    model_path = os.path.join(
        os.path.dirname(__file__), 'models', 'crop_model.pkl'
    )
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            features = np.array([[nitrogen, phosphorus, potassium,
                                   temperature, humidity, 7.0, rainfall]])
            prediction = model.predict(features)[0]
            proba = model.predict_proba(features)[0]
            confidence = float(max(proba) * 100)

            return {
                'recommended_crop': prediction,
                'confidence': round(confidence, 1),
                'method_used': 'ml_model',
                'season': CROP_DATABASE.get(prediction, {}).get('season', 'Mixed'),
                'harvest_days': CROP_DATABASE.get(prediction, {}).get('harvest_days', 120),
                'description': CROP_DATABASE.get(prediction, {}).get(
                    'description', 'AI-recommended crop.'
                ),
                'alternatives': [],
            }
        except Exception as e:
            logger.warning(f'ML model prediction failed, using rule-based: {e}')

    # ── Rule-based scoring ─────────────────────────────────────────────────────
    scores = {}
    for crop_name, crop_data in CROP_DATABASE.items():
        score = _score_crop(
            crop_name, crop_data, soil_type,
            temperature, rainfall, humidity,
            nitrogen, phosphorus, potassium
        )
        scores[crop_name] = score

    # Sort by score descending
    sorted_crops = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_crop_name, top_score = sorted_crops[0]
    top_crop_data = CROP_DATABASE[top_crop_name]

    # Normalize confidence to 0–100% range based on score vs max possible (100)
    # Add a baseline so that even 60-point crops show as "moderate confidence"
    confidence = min(99.5, max(50.0, top_score))

    alternatives = []
    for crop_name, score in sorted_crops[1:4]:
        alt_data = CROP_DATABASE[crop_name]
        alternatives.append({
            'crop': crop_name,
            'confidence': round(min(99.5, max(40.0, score)), 1),
            'season': alt_data['season'],
            'description': alt_data['description'],
        })

    return {
        'recommended_crop': top_crop_name,
        'confidence': round(confidence, 1),
        'method_used': 'rule_based',
        'season': top_crop_data['season'],
        'harvest_days': top_crop_data['harvest_days'],
        'description': top_crop_data['description'],
        'alternatives': alternatives,
    }
