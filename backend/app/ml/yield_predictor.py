"""
Smart Agro - Yield Prediction Engine
=======================================
Predicts expected crop yield based on environmental and management inputs.

Uses a formula-based approach with crop-specific base yields and
environmental modifier functions.

Input parameters:
  - crop_name:         Name of the crop (must match CROP_BASE_YIELDS keys)
  - area:              Cultivated area in acres
  - rainfall:          Annual rainfall in mm
  - fertilizer_amount: Fertilizer applied in kg/ha
  - temperature:       Average temperature in °C
  - season:            'kharif', 'rabi', 'summer', 'perennial'
"""

import math
import logging

logger = logging.getLogger(__name__)

# ── Base yield table (tonnes per acre under optimal conditions) ────────────────
CROP_BASE_YIELDS = {
    'Rice':        1.8,
    'Wheat':       1.6,
    'Corn':        2.5,
    'Cotton':      0.5,   # lint only
    'Sugarcane':   35.0,
    'Jute':        1.2,
    'Coffee':      0.3,
    'Tea':         0.8,
    'Rubber':      0.6,
    'Coconut':     0.7,
    'Papaya':      8.0,
    'Orange':      4.0,
    'Apple':       3.5,
    'Muskmelon':   5.0,
    'Watermelon':  10.0,
    'Grapes':      3.0,
    'Mango':       2.5,
    'Banana':      9.0,
    'Pomegranate': 4.0,
    'Lentil':      0.4,
    'Blackgram':   0.4,
    'Mungbean':    0.4,
    'Mothbeans':   0.3,
    'Pigeonpeas':  0.5,
    'Kidneybeans': 0.6,
    'Chickpea':    0.5,
}

# ── Ideal conditions for modifiers ────────────────────────────────────────────
CROP_IDEAL_CONDITIONS = {
    'Rice':        {'rainfall': (1200, 2000), 'temp': (22, 30), 'fertilizer': 200},
    'Wheat':       {'rainfall': (450, 650),   'temp': (12, 18), 'fertilizer': 180},
    'Corn':        {'rainfall': (600, 900),   'temp': (21, 27), 'fertilizer': 220},
    'Cotton':      {'rainfall': (600, 1000),  'temp': (25, 30), 'fertilizer': 150},
    'Sugarcane':   {'rainfall': (1200, 1800), 'temp': (25, 32), 'fertilizer': 300},
    'Jute':        {'rainfall': (1500, 2000), 'temp': (27, 32), 'fertilizer': 120},
    'Coffee':      {'rainfall': (1800, 2500), 'temp': (18, 24), 'fertilizer': 100},
    'Tea':         {'rainfall': (2000, 2500), 'temp': (18, 25), 'fertilizer': 120},
    'Rubber':      {'rainfall': (2000, 2500), 'temp': (25, 30), 'fertilizer': 100},
    'Coconut':     {'rainfall': (1500, 2000), 'temp': (25, 32), 'fertilizer': 100},
    'Papaya':      {'rainfall': (1200, 1700), 'temp': (25, 32), 'fertilizer': 200},
    'Orange':      {'rainfall': (800, 1200),  'temp': (20, 28), 'fertilizer': 150},
    'Apple':       {'rainfall': (800, 1000),  'temp': (10, 18), 'fertilizer': 120},
    'Muskmelon':   {'rainfall': (400, 700),   'temp': (24, 30), 'fertilizer': 120},
    'Watermelon':  {'rainfall': (500, 800),   'temp': (25, 30), 'fertilizer': 120},
    'Grapes':      {'rainfall': (500, 800),   'temp': (18, 24), 'fertilizer': 140},
    'Mango':       {'rainfall': (800, 1200),  'temp': (24, 30), 'fertilizer': 120},
    'Banana':      {'rainfall': (1200, 2000), 'temp': (25, 30), 'fertilizer': 250},
    'Pomegranate': {'rainfall': (500, 800),   'temp': (22, 28), 'fertilizer': 120},
    'Lentil':      {'rainfall': (300, 500),   'temp': (10, 18), 'fertilizer':  80},
    'Blackgram':   {'rainfall': (700, 1000),  'temp': (28, 32), 'fertilizer':  80},
    'Mungbean':    {'rainfall': (700, 1000),  'temp': (28, 32), 'fertilizer':  80},
    'Mothbeans':   {'rainfall': (300, 500),   'temp': (28, 33), 'fertilizer':  60},
    'Pigeonpeas':  {'rainfall': (800, 1200),  'temp': (25, 30), 'fertilizer':  80},
    'Kidneybeans': {'rainfall': (800, 1200),  'temp': (18, 24), 'fertilizer':  80},
    'Chickpea':    {'rainfall': (400, 600),   'temp': (15, 22), 'fertilizer':  80},
}

# Season suitability multipliers
SEASON_MULTIPLIERS = {
    'kharif':    1.00,
    'rabi':      1.00,
    'summer':    0.90,
    'perennial': 0.95,
    'zaid':      0.85,
    'mixed':     0.95,
}


def _rainfall_modifier(rainfall: float, ideal_range: tuple) -> float:
    """
    Calculate rainfall suitability modifier (0.5 – 1.0).
    """
    low, high = ideal_range
    if low <= rainfall <= high:
        return 1.0
    elif rainfall < low:
        # Penalize shortage
        ratio = rainfall / low
        return max(0.5, ratio)
    else:
        # Penalize excess (waterlogging)
        excess_ratio = (rainfall - high) / high
        return max(0.5, 1.0 - excess_ratio * 0.3)


def _temperature_modifier(temperature: float, ideal_range: tuple) -> float:
    """
    Calculate temperature suitability modifier (0.5 – 1.0).
    """
    low, high = ideal_range
    if low <= temperature <= high:
        return 1.0
    elif temperature < low:
        diff = low - temperature
        return max(0.5, 1.0 - diff * 0.04)
    else:
        diff = temperature - high
        return max(0.5, 1.0 - diff * 0.04)


def _fertilizer_modifier(fertilizer_amount: float, ideal_amount: float) -> float:
    """
    Calculate fertilizer efficiency modifier (0.5 – 1.1).
    More fertilizer than ideal has diminishing returns.
    """
    if ideal_amount == 0:
        return 1.0
    ratio = fertilizer_amount / ideal_amount
    if ratio <= 0:
        return 0.5
    elif ratio <= 1.0:
        # Under-fertilization: linear penalty
        return max(0.5, 0.5 + ratio * 0.5)
    elif ratio <= 1.5:
        # Slight excess → small bonus then plateau
        return min(1.1, 1.0 + (ratio - 1.0) * 0.1)
    else:
        # Heavy excess → diminishing returns, slight decline
        return max(0.7, 1.1 - (ratio - 1.5) * 0.1)


def predict_yield(
    crop_name: str,
    area: float,
    rainfall: float,
    fertilizer_amount: float,
    temperature: float,
    season: str = 'kharif'
) -> dict:
    """
    Predict crop yield based on input parameters.

    Args:
        crop_name:         Name of the crop.
        area:              Area under cultivation in acres.
        rainfall:          Annual rainfall in mm.
        fertilizer_amount: Fertilizer applied in kg/ha.
        temperature:       Average temperature in °C.
        season:            Planting season.

    Returns:
        dict with keys:
          predicted_yield       - Total yield in tonnes
          yield_per_acre        - Yield per acre in tonnes
          confidence_interval   - [low, high] range in tonnes
          base_yield_per_acre   - Reference base yield
          efficiency_score      - Overall efficiency %
          factors               - List of factor impact descriptions
    """
    # Normalize crop name for lookup
    crop_key = crop_name.strip().title()
    crop_key = {
        'Paddy': 'Rice', 'Maize': 'Corn', 'Bajra': 'Mungbean',
    }.get(crop_key, crop_key)

    # Default to generic if crop not found
    base_yield = CROP_BASE_YIELDS.get(crop_key, 1.5)
    conditions = CROP_IDEAL_CONDITIONS.get(crop_key, {
        'rainfall': (600, 1200), 'temp': (20, 30), 'fertilizer': 150
    })

    # Calculate individual modifiers
    rain_mod = _rainfall_modifier(rainfall, conditions['rainfall'])
    temp_mod = _temperature_modifier(temperature, conditions['temp'])
    fert_mod = _fertilizer_modifier(fertilizer_amount, conditions['fertilizer'])
    season_mod = SEASON_MULTIPLIERS.get(season.lower(), 0.95)

    # Combined efficiency score
    efficiency = rain_mod * temp_mod * fert_mod * season_mod

    # Predicted yield per acre
    yield_per_acre = base_yield * efficiency
    total_yield = yield_per_acre * area

    # Confidence interval ±10% of prediction
    ci_low = round(total_yield * 0.90, 2)
    ci_high = round(total_yield * 1.10, 2)

    # Build factor impact descriptions
    factors = []

    if rain_mod < 0.75:
        if rainfall < conditions['rainfall'][0]:
            factors.append(f'Low rainfall ({rainfall}mm) reducing yield significantly.')
        else:
            factors.append(f'Excess rainfall ({rainfall}mm) causing waterlogging risk.')
    elif rain_mod >= 0.95:
        factors.append(f'Rainfall ({rainfall}mm) is optimal.')

    if temp_mod < 0.80:
        factors.append(f'Temperature ({temperature}°C) is outside optimal range, affecting yield.')
    elif temp_mod >= 0.95:
        factors.append(f'Temperature ({temperature}°C) is ideal.')

    if fert_mod < 0.80:
        if fertilizer_amount < conditions['fertilizer']:
            factors.append(f'Under-fertilization ({fertilizer_amount}kg/ha) limiting potential yield.')
        else:
            factors.append(f'Over-fertilization may cause nutrient imbalance.')
    elif fert_mod >= 0.95:
        factors.append(f'Fertilizer application ({fertilizer_amount}kg/ha) is near optimal.')

    if season_mod < 0.95:
        factors.append(f'Season "{season}" is not the primary growing season for {crop_key}.')

    if not factors:
        factors.append('All growing conditions are optimal.')

    return {
        'crop_name': crop_key,
        'area_acres': area,
        'predicted_yield': round(total_yield, 2),
        'yield_per_acre': round(yield_per_acre, 2),
        'base_yield_per_acre': base_yield,
        'efficiency_score': round(efficiency * 100, 1),
        'confidence_interval': [ci_low, ci_high],
        'factors': factors,
        'modifiers': {
            'rainfall': round(rain_mod, 2),
            'temperature': round(temp_mod, 2),
            'fertilizer': round(fert_mod, 2),
            'season': season_mod,
        }
    }
