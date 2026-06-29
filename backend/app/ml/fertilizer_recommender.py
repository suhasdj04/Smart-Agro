"""
Smart Agro - Fertilizer Recommendation Engine
================================================
Recommends fertilizers based on crop type, soil nutrient levels, and pH.

Input:
  - soil_type:   Sandy / Loamy / Clay / Silt / Peaty / Chalky
  - crop_type:   Crop name
  - nitrogen:    Current soil N level (kg/ha)
  - phosphorus:  Current soil P level (kg/ha)
  - potassium:   Current soil K level (kg/ha)
  - ph_level:    Soil pH (1–14)

Logic:
  1. Look up ideal NPK for the crop
  2. Calculate deficit/surplus for each nutrient
  3. Recommend specific fertilizers with dosage to fill deficits
  4. Adjust for soil type (some soils need more or less)
  5. Provide organic alternatives
"""

import logging

logger = logging.getLogger(__name__)

# ── Ideal NPK requirements per crop (kg/ha) ───────────────────────────────────
CROP_NPK_REQUIREMENTS = {
    'Rice':        {'N': 120, 'P': 60,  'K': 60},
    'Wheat':       {'N': 120, 'P': 60,  'K': 40},
    'Corn':        {'N': 150, 'P': 75,  'K': 75},
    'Cotton':      {'N': 120, 'P': 60,  'K': 60},
    'Sugarcane':   {'N': 250, 'P': 100, 'K': 120},
    'Jute':        {'N': 100, 'P': 50,  'K': 50},
    'Coffee':      {'N': 100, 'P': 50,  'K': 100},
    'Tea':         {'N': 120, 'P': 50,  'K': 70},
    'Rubber':      {'N': 90,  'P': 50,  'K': 90},
    'Coconut':     {'N': 100, 'P': 60,  'K': 200},
    'Papaya':      {'N': 200, 'P': 100, 'K': 200},
    'Orange':      {'N': 120, 'P': 60,  'K': 120},
    'Apple':       {'N': 100, 'P': 50,  'K': 100},
    'Mango':       {'N': 100, 'P': 60,  'K': 100},
    'Banana':      {'N': 200, 'P': 60,  'K': 300},
    'Grapes':      {'N': 100, 'P': 60,  'K': 100},
    'Watermelon':  {'N': 80,  'P': 50,  'K': 80},
    'Muskmelon':   {'N': 80,  'P': 50,  'K': 80},
    'Pomegranate': {'N': 100, 'P': 50,  'K': 100},
    'Papaya':      {'N': 200, 'P': 80,  'K': 200},
    'Lentil':      {'N': 25,  'P': 60,  'K': 40},
    'Chickpea':    {'N': 20,  'P': 60,  'K': 40},
    'Mungbean':    {'N': 25,  'P': 50,  'K': 40},
    'Blackgram':   {'N': 25,  'P': 50,  'K': 40},
    'Pigeonpeas':  {'N': 20,  'P': 60,  'K': 40},
    'Kidneybeans': {'N': 25,  'P': 60,  'K': 40},
    'Mothbeans':   {'N': 20,  'P': 40,  'K': 30},
}

# Default NPK requirement if crop not in database
DEFAULT_NPK = {'N': 100, 'P': 60, 'K': 60}

# ── Fertilizer products database ──────────────────────────────────────────────
# Each fertilizer has: N%, P%, K%, typical_name, notes
FERTILIZERS = {
    'Urea': {
        'N': 46, 'P': 0, 'K': 0,
        'description': 'Most concentrated nitrogen fertilizer (46% N)',
        'timing': 'Apply in split doses: 50% at sowing, 25% at tillering, 25% at panicle initiation.',
        'method': 'Broadcast or deep placement to reduce volatilization.',
        'price_per_kg': 6.0,  # approximate INR
    },
    'DAP': {
        'N': 18, 'P': 46, 'K': 0,
        'description': 'Di-Ammonium Phosphate — primary phosphorus source (46% P₂O₅)',
        'timing': 'Apply at sowing/planting time for best root development.',
        'method': 'Incorporate into soil before planting.',
        'price_per_kg': 27.0,
    },
    'MOP': {
        'N': 0, 'P': 0, 'K': 60,
        'description': 'Muriate of Potash — primary potassium source (60% K₂O)',
        'timing': 'Apply before sowing or at planting.',
        'method': 'Broadcast and incorporate into soil.',
        'price_per_kg': 17.0,
    },
    'NPK 19-19-19': {
        'N': 19, 'P': 19, 'K': 19,
        'description': 'Balanced water-soluble fertilizer for foliar and fertigation use.',
        'timing': 'Apply at active growth stages through drip/foliar.',
        'method': 'Fertigation or foliar spray (2–3 kg per 200L water).',
        'price_per_kg': 45.0,
    },
    'SSP': {
        'N': 0, 'P': 16, 'K': 0,
        'description': 'Single Super Phosphate — phosphorus + sulfur source',
        'timing': 'Apply before or at sowing.',
        'method': 'Incorporate into root zone.',
        'price_per_kg': 12.0,
    },
    'SOP': {
        'N': 0, 'P': 0, 'K': 50,
        'description': 'Sulphate of Potash — chloride-free potassium for sensitive crops',
        'timing': 'Apply before planting or through fertigation.',
        'method': 'Soil application or fertigation.',
        'price_per_kg': 30.0,
    },
    'Ammonium Sulfate': {
        'N': 21, 'P': 0, 'K': 0,
        'description': 'Nitrogen + sulfur fertilizer, slightly acidifying',
        'timing': 'Apply as basal dose or top dressing.',
        'method': 'Broadcast and incorporate.',
        'price_per_kg': 16.0,
    },
}

# Organic alternatives database
ORGANIC_ALTERNATIVES = {
    'N': [
        {'name': 'Neem Cake', 'nutrient_content': '5% N', 'dosage': '200–400 kg/ha'},
        {'name': 'Farmyard Manure (FYM)', 'nutrient_content': '0.5% N', 'dosage': '10–15 tonnes/ha'},
        {'name': 'Vermicompost', 'nutrient_content': '1.5–2% N', 'dosage': '2–5 tonnes/ha'},
        {'name': 'Green Manure (Dhaincha/Sesbania)', 'nutrient_content': '2–3% N', 'dosage': 'Incorporate crop at flowering'},
    ],
    'P': [
        {'name': 'Rock Phosphate', 'nutrient_content': '20–30% P₂O₅', 'dosage': '100–200 kg/ha'},
        {'name': 'Bone Meal', 'nutrient_content': '20% P', 'dosage': '100–150 kg/ha'},
        {'name': 'Vermicompost', 'nutrient_content': '0.8–1.2% P', 'dosage': '2–5 tonnes/ha'},
    ],
    'K': [
        {'name': 'Wood Ash', 'nutrient_content': '5–10% K', 'dosage': '200–500 kg/ha'},
        {'name': 'Banana Stem Compost', 'nutrient_content': '1.5–2% K', 'dosage': '2–4 tonnes/ha'},
        {'name': 'Granite Dust', 'nutrient_content': '3–5% K', 'dosage': '200–400 kg/ha'},
    ],
}

# Soil pH adjustment recommendations
PH_RECOMMENDATIONS = {
    'too_acidic': {   # pH < 5.5
        'problem': 'Soil is too acidic. Many nutrients become less available.',
        'solution': 'Apply agricultural lime (1–2 tonnes/ha) to raise pH.',
        'organic': 'Wood ash application (250–500 kg/ha) can gently raise pH.',
    },
    'slightly_acidic': {  # pH 5.5–6.5
        'problem': 'Slightly acidic — ideal for most crops.',
        'solution': 'No correction needed. Maintain with regular organic matter addition.',
        'organic': None,
    },
    'optimal': {  # pH 6.5–7.5
        'problem': None,
        'solution': 'Optimal pH range for maximum nutrient availability.',
        'organic': None,
    },
    'slightly_alkaline': {  # pH 7.5–8.5
        'problem': 'Slightly alkaline — some micronutrient deficiencies possible.',
        'solution': 'Apply gypsum (calcium sulfate) to slightly acidify.',
        'organic': 'Incorporate organic matter (compost, peat) to buffer pH.',
    },
    'too_alkaline': {  # pH > 8.5
        'problem': 'Highly alkaline soil limits nutrient uptake severely.',
        'solution': 'Apply elemental sulfur (100–200 kg/ha) to lower pH.',
        'organic': 'Use acidifying organic materials like pine needle compost.',
    },
}

# Soil type nutrient retention modifiers
# Some soils hold nutrients better; sandy soils need more frequent application
SOIL_RETENTION_MODIFIERS = {
    'Sandy': 1.25,   # Sandy soils leach more, need 25% more
    'Loamy': 1.00,   # Loam is the ideal reference
    'Clay': 0.85,    # Clay holds well, needs slightly less
    'Silt': 0.95,    # Silt retains moderately
    'Peaty': 0.90,   # Peat is organically rich
    'Chalky': 1.15,  # Chalky = alkaline, some nutrients become locked
}


def _get_ph_category(ph: float) -> str:
    if ph < 5.5:
        return 'too_acidic'
    elif ph < 6.5:
        return 'slightly_acidic'
    elif ph <= 7.5:
        return 'optimal'
    elif ph <= 8.5:
        return 'slightly_alkaline'
    else:
        return 'too_alkaline'


def recommend_fertilizer(
    soil_type: str,
    crop_type: str,
    nitrogen: float,
    phosphorus: float,
    potassium: float,
    ph_level: float
) -> dict:
    """
    Generate a comprehensive fertilizer recommendation.

    Args:
        soil_type:   Type of soil (Sandy/Loamy/Clay/Silt/Peaty/Chalky)
        crop_type:   Crop name
        nitrogen:    Current soil N (kg/ha)
        phosphorus:  Current soil P (kg/ha)
        potassium:   Current soil K (kg/ha)
        ph_level:    Soil pH

    Returns:
        dict with recommendation details, dosages, timing, and organic alternatives
    """
    crop_key = crop_type.strip().title()
    crop_key = {'Paddy': 'Rice', 'Maize': 'Corn'}.get(crop_key, crop_key)

    # Get crop's NPK requirement
    requirements = CROP_NPK_REQUIREMENTS.get(crop_key, DEFAULT_NPK)

    # Soil retention modifier
    retention_mod = SOIL_RETENTION_MODIFIERS.get(soil_type, 1.0)

    # Adjusted requirement (compensate for soil leaching)
    adj_N = requirements['N'] * retention_mod
    adj_P = requirements['P'] * retention_mod
    adj_K = requirements['K'] * retention_mod

    # Deficits (positive = need to add, negative = surplus)
    deficit_N = max(0, adj_N - nitrogen)
    deficit_P = max(0, adj_P - phosphorus)
    deficit_K = max(0, adj_K - potassium)

    # ── Build recommendations ──────────────────────────────────────────────────
    recommendations = []

    # Nitrogen recommendation (prefer Urea for large deficits)
    if deficit_N > 10:
        urea_kg_ha = deficit_N / (FERTILIZERS['Urea']['N'] / 100)
        recommendations.append({
            'fertilizer': 'Urea',
            'nutrient': 'Nitrogen (N)',
            'deficit_kg_ha': round(deficit_N, 1),
            'dosage_kg_ha': round(urea_kg_ha, 1),
            'description': FERTILIZERS['Urea']['description'],
            'timing': FERTILIZERS['Urea']['timing'],
            'method': FERTILIZERS['Urea']['method'],
            'estimated_cost_inr': round(urea_kg_ha * FERTILIZERS['Urea']['price_per_kg'], 0),
        })

    # Phosphorus recommendation (prefer DAP)
    if deficit_P > 5:
        dap_kg_ha = deficit_P / (FERTILIZERS['DAP']['P'] / 100)
        # Note DAP also provides some N
        n_from_dap = dap_kg_ha * FERTILIZERS['DAP']['N'] / 100
        recommendations.append({
            'fertilizer': 'DAP',
            'nutrient': 'Phosphorus (P)',
            'deficit_kg_ha': round(deficit_P, 1),
            'dosage_kg_ha': round(dap_kg_ha, 1),
            'description': FERTILIZERS['DAP']['description'],
            'note': f'DAP also provides {round(n_from_dap, 1)} kg/ha of N — deduct from Urea.',
            'timing': FERTILIZERS['DAP']['timing'],
            'method': FERTILIZERS['DAP']['method'],
            'estimated_cost_inr': round(dap_kg_ha * FERTILIZERS['DAP']['price_per_kg'], 0),
        })

    # Potassium recommendation (prefer MOP)
    if deficit_K > 5:
        mop_kg_ha = deficit_K / (FERTILIZERS['MOP']['K'] / 100)
        recommendations.append({
            'fertilizer': 'MOP (Muriate of Potash)',
            'nutrient': 'Potassium (K)',
            'deficit_kg_ha': round(deficit_K, 1),
            'dosage_kg_ha': round(mop_kg_ha, 1),
            'description': FERTILIZERS['MOP']['description'],
            'timing': FERTILIZERS['MOP']['timing'],
            'method': FERTILIZERS['MOP']['method'],
            'estimated_cost_inr': round(mop_kg_ha * FERTILIZERS['MOP']['price_per_kg'], 0),
        })

    # If all nutrients are adequate
    if not recommendations:
        recommendations.append({
            'fertilizer': 'Maintenance Dose',
            'nutrient': 'NPK',
            'deficit_kg_ha': 0,
            'dosage_kg_ha': 0,
            'description': 'Soil nutrients are at adequate levels. Apply NPK 19-19-19 as maintenance.',
            'timing': 'Apply at crop active growth stage.',
            'method': 'Foliar spray or fertigation.',
            'estimated_cost_inr': 0,
        })

    # pH recommendation
    ph_category = _get_ph_category(ph_level)
    ph_info = PH_RECOMMENDATIONS[ph_category]

    # Build organic alternatives list
    organic_alts = []
    if deficit_N > 10:
        organic_alts.extend(ORGANIC_ALTERNATIVES['N'])
    if deficit_P > 5:
        organic_alts.extend(ORGANIC_ALTERNATIVES['P'])
    if deficit_K > 5:
        organic_alts.extend(ORGANIC_ALTERNATIVES['K'])

    # Nutrient status summary
    nutrient_status = {
        'nitrogen': {
            'current': nitrogen,
            'required': round(adj_N, 1),
            'deficit': round(deficit_N, 1),
            'status': 'deficient' if deficit_N > 10 else ('adequate' if deficit_N >= 0 else 'surplus'),
        },
        'phosphorus': {
            'current': phosphorus,
            'required': round(adj_P, 1),
            'deficit': round(deficit_P, 1),
            'status': 'deficient' if deficit_P > 5 else ('adequate' if deficit_P >= 0 else 'surplus'),
        },
        'potassium': {
            'current': potassium,
            'required': round(adj_K, 1),
            'deficit': round(deficit_K, 1),
            'status': 'deficient' if deficit_K > 5 else ('adequate' if deficit_K >= 0 else 'surplus'),
        },
    }

    return {
        'crop': crop_key,
        'soil_type': soil_type,
        'ph_level': ph_level,
        'ph_status': ph_category,
        'ph_recommendation': ph_info,
        'nutrient_status': nutrient_status,
        'fertilizer_recommendations': recommendations,
        'organic_alternatives': organic_alts,
        'general_advice': (
            f'For {crop_key} on {soil_type} soil, apply fertilizers in split doses '
            'to minimize losses. Always water thoroughly after application. '
            'Conduct a soil test every 2–3 years for best results.'
        ),
    }
