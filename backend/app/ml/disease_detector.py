"""
Smart Agro - Disease Detection Engine
=======================================
Detects crop diseases from plant images.

Architecture:
  - In production: Replace _predict() with a real TensorFlow/Keras CNN model call
  - In development/mock mode: Uses image file hash to deterministically pick a disease
    (same image always returns the same result, making testing consistent)

To plug in a real model:
  1. Place your model at app/ml/models/disease_model.h5
  2. Load it in model_loader.py
  3. Replace the _mock_predict() call in detect_disease() with a real inference call
"""

import hashlib
import io
import logging
from PIL import Image

logger = logging.getLogger(__name__)

# ── Comprehensive disease database ────────────────────────────────────────────
# Structure per disease:
#   name, crop, confidence_range, severity, treatment,
#   prevention, organic_treatment, affected_parts
DISEASE_DATABASE = [
    # ── Rice diseases ─────────────────────────────────────────────────────────
    {
        'id': 'rice_blast',
        'name': 'Rice Blast',
        'crop': 'Rice',
        'confidence_range': (0.82, 0.97),
        'severity': 'high',
        'affected_parts': 'Leaves, nodes, panicles',
        'symptoms': (
            'Diamond-shaped lesions with grey centers and brown borders on leaves; '
            'collar rot at nodes; infected panicles show white or grey discoloration.'
        ),
        'treatment': (
            '1. Apply Tricyclazole (0.06%) or Isoprothiolane (0.075%) at first sign of disease.\n'
            '2. Spray Carbendazim (0.05%) at early infection stage.\n'
            '3. Remove and destroy infected plant parts.\n'
            '4. Ensure proper drainage to reduce humidity in the field.\n'
            '5. Avoid excess nitrogen application which promotes disease spread.'
        ),
        'prevention': (
            '• Use blast-resistant rice varieties.\n'
            '• Seed treatment with Carbendazim (2g/kg seed).\n'
            '• Avoid over-application of nitrogenous fertilizers.\n'
            '• Maintain proper spacing to improve air circulation.\n'
            '• Drain fields periodically to reduce humidity.'
        ),
        'organic_treatment': (
            'Spray Pseudomonas fluorescens (10g/L water) on affected plants. '
            'Trichoderma viride application at 2.5 kg/ha mixed with 50 kg FYM also helps. '
            'Neem oil (3ml/L) spray reduces spore germination.'
        ),
    },
    {
        'id': 'rice_bacterial_blight',
        'name': 'Rice Bacterial Blight',
        'crop': 'Rice',
        'confidence_range': (0.78, 0.94),
        'severity': 'high',
        'affected_parts': 'Leaves, vascular system',
        'symptoms': (
            'Water-soaked to yellowish stripes on leaf margins that turn yellowish-white; '
            'bacterial ooze visible in the morning on infected leaves.'
        ),
        'treatment': (
            '1. Spray Copper Oxychloride (0.3%) + Streptomycin Sulfate (100ppm).\n'
            '2. Remove infected tillers immediately.\n'
            '3. Drain the field and allow soil to dry.\n'
            '4. Avoid overhead irrigation which spreads bacteria.\n'
            '5. Apply Bleaching Powder (25 kg/ha) to reduce bacterial population in water.'
        ),
        'prevention': (
            '• Use certified disease-free seed.\n'
            '• Treat seeds with Streptocycline (0.5g/L) + Copper Oxychloride (2g/L) for 8 hours.\n'
            '• Use resistant varieties.\n'
            '• Avoid field flooding with water from infected fields.'
        ),
        'organic_treatment': (
            'Spray garlic extract (50g/L) or onion extract on infected plants. '
            'Compost tea spray helps improve plant immunity. '
            'Trichoderma application in soil reduces bacterial populations.'
        ),
    },
    {
        'id': 'rice_brown_spot',
        'name': 'Rice Brown Spot',
        'crop': 'Rice',
        'confidence_range': (0.75, 0.92),
        'severity': 'medium',
        'affected_parts': 'Leaves, glumes',
        'symptoms': (
            'Small, circular to oval brown spots with yellow halo on leaves; '
            'severely infected leaves turn brown and die; infected grains show dark brown discoloration.'
        ),
        'treatment': (
            '1. Apply Mancozeb (0.25%) or Iprodione (0.1%) fungicide spray.\n'
            '2. Ensure adequate potassium fertilization to improve plant resistance.\n'
            '3. Spray Edifenphos at 500ml/ha in 500L water.\n'
            '4. Remove and burn severely infected plant material.'
        ),
        'prevention': (
            '• Treat seeds with Thiram (2g/kg) or Carbendazim.\n'
            '• Avoid late nitrogen application.\n'
            '• Maintain balanced soil nutrients, especially potassium.\n'
            '• Use resistant varieties where available.'
        ),
        'organic_treatment': (
            'Spray neem oil (5ml/L) every 10 days. '
            'Wood ash application improves potassium levels. '
            'Trichoderma viride seed treatment helps prevent infection.'
        ),
    },
    {
        'id': 'rice_sheath_blight',
        'name': 'Rice Sheath Blight',
        'crop': 'Rice',
        'confidence_range': (0.80, 0.95),
        'severity': 'high',
        'affected_parts': 'Sheath, leaves',
        'symptoms': (
            'Initially oval or elliptic greenish-grey lesions on leaf sheaths; '
            'lesions enlarge with irregular margins; in severe cases extends to leaves causing them to die.'
        ),
        'treatment': (
            '1. Spray Hexaconazole (0.1%) or Propiconazole (0.1%) at disease onset.\n'
            '2. Validamycin (0.1%) is highly effective against sheath blight.\n'
            '3. Ensure field drainage to reduce humidity.\n'
            '4. Reduce plant density for better air circulation.'
        ),
        'prevention': (
            '• Avoid excessive nitrogen fertilization.\n'
            '• Use moderate spacing (20cm × 15cm) to reduce canopy humidity.\n'
            '• Remove plant debris after harvest.\n'
            '• Plow deep to bury sclerotia.'
        ),
        'organic_treatment': (
            'Biological control with Trichoderma harzianum (1%) spray has shown 50% disease reduction. '
            'Garlic-ginger extract spray also helps suppress mycelial growth.'
        ),
    },
    # ── Wheat diseases ────────────────────────────────────────────────────────
    {
        'id': 'wheat_rust',
        'name': 'Wheat Yellow Rust (Stripe Rust)',
        'crop': 'Wheat',
        'confidence_range': (0.83, 0.97),
        'severity': 'high',
        'affected_parts': 'Leaves, stems',
        'symptoms': (
            'Yellow-orange pustules arranged in stripes parallel to leaf veins; '
            'infected areas turn necrotic; severe infection can devastate entire crop.'
        ),
        'treatment': (
            '1. Spray Propiconazole (0.1%) or Tebuconazole (0.1%) at first sign.\n'
            '2. Apply Mancozeb (0.25%) as a protectant spray.\n'
            '3. Repeat spray every 14–21 days if disease pressure continues.\n'
            '4. Remove volunteer wheat plants that harbor the pathogen.'
        ),
        'prevention': (
            '• Plant rust-resistant varieties.\n'
            '• Avoid late sowing.\n'
            '• Use balanced fertilization.\n'
            '• Monitor fields weekly during flag leaf stage.'
        ),
        'organic_treatment': (
            'No fully effective organic cure exists. Sulfur dust (20–30 kg/ha) can reduce spread. '
            'Neem oil spray provides some protection. Maintaining plant health through '
            'balanced nutrition reduces severity.'
        ),
    },
    {
        'id': 'wheat_powdery_mildew',
        'name': 'Wheat Powdery Mildew',
        'crop': 'Wheat',
        'confidence_range': (0.79, 0.93),
        'severity': 'medium',
        'affected_parts': 'Leaves, stems, spike',
        'symptoms': (
            'White powdery fungal growth on upper leaf surfaces; '
            'infected tissue turns yellow then brown; severe infection reduces photosynthesis.'
        ),
        'treatment': (
            '1. Apply Triadimefon (0.1%) or Propiconazole (0.1%).\n'
            '2. Spray Sulphur (0.3%) at early infection.\n'
            '3. Use Myclobutanil (0.04%) for severe infections.\n'
            '4. Avoid dense planting which increases humidity.'
        ),
        'prevention': (
            '• Plant resistant varieties.\n'
            '• Balanced fertilization (avoid excess N).\n'
            '• Improve air circulation through proper spacing.\n'
            '• Remove infected plant material.'
        ),
        'organic_treatment': (
            'Spray baking soda solution (5g/L water + 2ml/L liquid soap) every 7 days. '
            'Milk spray (1:10 ratio with water) has shown effectiveness in trials. '
            'Neem oil (5ml/L) spray every 10 days.'
        ),
    },
    {
        'id': 'wheat_loose_smut',
        'name': 'Wheat Loose Smut',
        'crop': 'Wheat',
        'confidence_range': (0.76, 0.91),
        'severity': 'medium',
        'affected_parts': 'Spike (ear head)',
        'symptoms': (
            'Entire spike replaced by black mass of smut spores; '
            'infected spikes emerge earlier than healthy ones and quickly disperse spores.'
        ),
        'treatment': (
            '1. No effective spray treatment after infection — prevention is key.\n'
            '2. Destroy infected plants immediately to prevent spore dispersal.\n'
            '3. Treat seed with Carboxin (2g/kg) for systemic protection.'
        ),
        'prevention': (
            '• Seed treatment with systemic fungicides (Carboxin, Vitavax).\n'
            '• Use certified smut-free seed.\n'
            '• Hot water seed treatment: soak in water at 52°C for 10 min.\n'
            '• Plant resistant varieties.'
        ),
        'organic_treatment': (
            'Solar seed treatment: spread seeds in thin layer under sun for 3 days. '
            'Garlic extract seed treatment (250g garlic in 1L water per 10kg seed) reduces incidence.'
        ),
    },
    # ── Corn/Maize diseases ───────────────────────────────────────────────────
    {
        'id': 'corn_gray_leaf_spot',
        'name': 'Corn Gray Leaf Spot',
        'crop': 'Corn',
        'confidence_range': (0.80, 0.95),
        'severity': 'medium',
        'affected_parts': 'Leaves',
        'symptoms': (
            'Tan to brown rectangular lesions with parallel margins that follow leaf veins; '
            'lesions turn gray as they mature; severe infection causes premature senescence.'
        ),
        'treatment': (
            '1. Apply Azoxystrobin (0.1%) or Pyraclostrobin at tassel stage.\n'
            '2. Propiconazole (0.1%) effective if applied before lesions expand.\n'
            '3. Remove severely infected lower leaves.'
        ),
        'prevention': (
            '• Crop rotation with non-host crops.\n'
            '• Tillage to reduce infected residue.\n'
            '• Plant resistant hybrids.\n'
            '• Avoid overhead irrigation.'
        ),
        'organic_treatment': (
            'Compost tea spray (1:10) applied weekly improves general plant immunity. '
            'Bacillus subtilis-based biological fungicides show promising results.'
        ),
    },
    {
        'id': 'corn_common_rust',
        'name': 'Corn Common Rust',
        'crop': 'Corn',
        'confidence_range': (0.82, 0.96),
        'severity': 'medium',
        'affected_parts': 'Leaves',
        'symptoms': (
            'Circular to elongate, golden-brown to cinnamon-brown pustules on both leaf surfaces; '
            'heavily infected leaves may yellow and die prematurely.'
        ),
        'treatment': (
            '1. Spray Mancozeb (0.25%) at disease onset.\n'
            '2. Tebuconazole or Propiconazole fungicide if disease is severe.\n'
            '3. Early infections before silking are most critical to treat.'
        ),
        'prevention': (
            '• Plant rust-resistant hybrids.\n'
            '• Monitor regularly from seedling to tasseling stage.\n'
            '• Adjust planting dates to avoid peak rust season.'
        ),
        'organic_treatment': (
            'Sulfur-based fungicide (wettable sulfur 80%) at 2–3 kg/ha. '
            'Neem oil spray (5ml/L) provides some protection.'
        ),
    },
    {
        'id': 'corn_northern_leaf_blight',
        'name': 'Corn Northern Leaf Blight',
        'crop': 'Corn',
        'confidence_range': (0.79, 0.94),
        'severity': 'high',
        'affected_parts': 'Leaves',
        'symptoms': (
            'Long, elliptical, gray-green to tan lesions (up to 15cm) on leaves; '
            'lesions may appear on lower leaves first and move upward.'
        ),
        'treatment': (
            '1. Apply Azoxystrobin + Propiconazole combination fungicide.\n'
            '2. Chlorothalonil (0.2%) as preventative spray.\n'
            '3. Fungicide application most effective at early tasseling.'
        ),
        'prevention': (
            '• Use resistant corn hybrids (Ht gene).\n'
            '• Crop rotation.\n'
            '• Residue management through tillage.\n'
            '• Avoid excessive plant density.'
        ),
        'organic_treatment': (
            'Bacillus subtilis or Trichoderma-based biocontrol agents show moderate effectiveness. '
            'Compost amendments improve general soil and plant health.'
        ),
    },
    # ── Tomato diseases ───────────────────────────────────────────────────────
    {
        'id': 'tomato_early_blight',
        'name': 'Tomato Early Blight',
        'crop': 'Tomato',
        'confidence_range': (0.81, 0.96),
        'severity': 'medium',
        'affected_parts': 'Leaves, stem, fruit',
        'symptoms': (
            'Circular dark brown spots with concentric rings (target-board pattern) on older leaves; '
            'infected leaves yellow and drop; stem lesions are dark and sunken.'
        ),
        'treatment': (
            '1. Spray Mancozeb (0.25%) or Chlorothalonil (0.2%) at disease onset.\n'
            '2. Copper-based fungicides (Copper Oxychloride 0.3%) are effective.\n'
            '3. Remove and destroy infected leaves immediately.\n'
            '4. Repeat spray every 7–10 days during wet weather.'
        ),
        'prevention': (
            '• Stake plants to improve air circulation.\n'
            '• Mulch to reduce soil splash.\n'
            '• Water at base rather than overhead.\n'
            '• Crop rotation (3-year cycle).\n'
            '• Remove plant debris after harvest.'
        ),
        'organic_treatment': (
            'Spray copper soap fungicide (approved organic). '
            'Baking soda spray (5g/L + neem oil 2ml/L). '
            'Compost tea spray weekly. '
            'Trichoderma viride soil application reduces inoculum.'
        ),
    },
    {
        'id': 'tomato_late_blight',
        'name': 'Tomato Late Blight',
        'crop': 'Tomato',
        'confidence_range': (0.85, 0.98),
        'severity': 'high',
        'affected_parts': 'Leaves, stem, fruit',
        'symptoms': (
            'Water-soaked, pale green to dark brown irregular lesions on leaves; '
            'white downy mold visible on underside of leaves in humid conditions; '
            'brown sunken lesions on stems and fruit.'
        ),
        'treatment': (
            '1. Apply Metalaxyl + Mancozeb (0.2%) immediately upon detection.\n'
            '2. Cymoxanil + Mancozeb (0.2%) for quick knockdown.\n'
            '3. Remove severely infected plants to prevent spread.\n'
            '4. Spray every 5–7 days in wet weather.'
        ),
        'prevention': (
            '• Plant resistant varieties.\n'
            '• Avoid overhead irrigation.\n'
            '• Ensure good air circulation.\n'
            '• Prophylactic copper spray during monsoon season.\n'
            '• Destroy infected plant material — do not compost.'
        ),
        'organic_treatment': (
            'Copper hydroxide spray (approved organic). '
            'Avoid the disease by planting resistant varieties and good cultural practices. '
            'Once severe, organic options are limited — copper is most effective.'
        ),
    },
    # ── Potato diseases ───────────────────────────────────────────────────────
    {
        'id': 'potato_early_blight',
        'name': 'Potato Early Blight',
        'crop': 'Potato',
        'confidence_range': (0.79, 0.93),
        'severity': 'medium',
        'affected_parts': 'Leaves, tubers',
        'symptoms': (
            'Small dark brown spots with concentric rings on older leaves; '
            'infected tissue surrounded by yellow halo; tubers show dark, circular, sunken lesions.'
        ),
        'treatment': (
            '1. Spray Mancozeb (0.25%) or Chlorothalonil (0.2%).\n'
            '2. Azoxystrobin (0.1%) provides both preventive and curative action.\n'
            '3. Remove and destroy severely infected foliage.'
        ),
        'prevention': (
            '• Use certified disease-free seed tubers.\n'
            '• Crop rotation.\n'
            '• Avoid excessive nitrogen.\n'
            '• Hilling to protect tubers.\n'
            '• Remove volunteer potato plants.'
        ),
        'organic_treatment': (
            'Copper-based sprays (copper sulfate 0.5%) every 10 days. '
            'Neem extract (5ml/L) spray as preventive. '
            'Compost amendment improves plant resistance.'
        ),
    },
    {
        'id': 'potato_late_blight',
        'name': 'Potato Late Blight',
        'crop': 'Potato',
        'confidence_range': (0.86, 0.98),
        'severity': 'high',
        'affected_parts': 'Leaves, stems, tubers',
        'symptoms': (
            'Water-soaked lesions that rapidly turn dark brown; '
            'white cottony growth on leaf undersides in high humidity; '
            'infected tubers have reddish-brown internal rot.'
        ),
        'treatment': (
            '1. Metalaxyl + Mancozeb (Ridomil Gold) spray immediately.\n'
            '2. Dimethomorph (0.1%) for systemic control.\n'
            '3. Remove infected haulms before tuber harvest to prevent spread.\n'
            '4. Spray every 5–7 days during wet weather.'
        ),
        'prevention': (
            '• Use certified seed tubers and resistant varieties.\n'
            '• Destroy infected volunteer plants.\n'
            '• Prophylactic copper spray at canopy closure.\n'
            '• Avoid overhead irrigation.\n'
            '• Harvest in dry conditions.'
        ),
        'organic_treatment': (
            'Certified copper fungicide applications are the primary organic option. '
            'Biocontrol with Bacillus subtilis (0.2%) has shown up to 40% reduction. '
            'Prevention through resistant variety selection is most effective.'
        ),
    },
    {
        'id': 'potato_black_scurf',
        'name': 'Potato Black Scurf (Rhizoctonia)',
        'crop': 'Potato',
        'confidence_range': (0.74, 0.89),
        'severity': 'low',
        'affected_parts': 'Tubers, stems',
        'symptoms': (
            'Irregularly shaped, dark black sclerotia on tuber surface (look like dirt that won\'t wash off); '
            'stem lesions cause wilting and stunted growth.'
        ),
        'treatment': (
            '1. Seed tuber treatment with Thiram + Carboxin (3g/kg).\n'
            '2. Pencycuron (0.2%) soil drench at planting.\n'
            '3. Crop rotation with non-host crops.'
        ),
        'prevention': (
            '• Use certified sclerotia-free seed tubers.\n'
            '• Plant in well-drained, warm soil.\n'
            '• Crop rotation with cereals.\n'
            '• Trichoderma viride soil application.'
        ),
        'organic_treatment': (
            'Trichoderma harzianum (5g/kg seed) treatment reduces incidence. '
            'Compost with suppressive microorganisms reduces soil inoculum. '
            'Mustard cake soil application has shown antifungal activity.'
        ),
    },
    # ── Healthy plant ─────────────────────────────────────────────────────────
    {
        'id': 'healthy',
        'name': 'Healthy Plant',
        'crop': 'General',
        'confidence_range': (0.85, 0.99),
        'severity': 'none',
        'affected_parts': 'None',
        'symptoms': 'No disease symptoms detected. Plant appears healthy.',
        'treatment': (
            'No treatment required. Maintain good agronomic practices:\n'
            '1. Regular irrigation and fertilization schedule.\n'
            '2. Periodic scouting for early pest/disease detection.\n'
            '3. Preventive fungicide/pesticide as per crop schedule.'
        ),
        'prevention': (
            '• Continue regular monitoring.\n'
            '• Maintain balanced nutrition.\n'
            '• Practice crop rotation.\n'
            '• Remove weeds and debris regularly.'
        ),
        'organic_treatment': 'No treatment needed. Maintain soil health with compost and crop rotation.',
    },
]


def _get_image_hash(image_bytes: bytes) -> int:
    """Generate a deterministic integer hash from image bytes."""
    md5 = hashlib.md5(image_bytes).hexdigest()
    return int(md5, 16)


def _mock_predict(image_bytes: bytes, crop_type: str = None) -> dict:
    """
    Mock disease prediction for development/testing.
    Uses image hash to deterministically select a disease.
    Same image → same result every time.

    Args:
        image_bytes: Raw image bytes.
        crop_type:   Optional crop type hint for filtering diseases.

    Returns:
        Disease record dict from DISEASE_DATABASE.
    """
    img_hash = _get_image_hash(image_bytes)

    # Filter diseases by crop type if provided
    if crop_type:
        crop_normalized = crop_type.strip().title()
        crop_diseases = [
            d for d in DISEASE_DATABASE
            if d['crop'].lower() == crop_normalized.lower() or d['crop'] == 'General'
        ]
        if not crop_diseases:
            crop_diseases = DISEASE_DATABASE  # fallback to all
    else:
        crop_diseases = DISEASE_DATABASE

    # Deterministically pick disease by hash
    idx = img_hash % len(crop_diseases)
    disease = crop_diseases[idx]

    # Pick a confidence within the disease's range using hash
    conf_low, conf_high = disease['confidence_range']
    conf_range = conf_high - conf_low
    confidence = conf_low + (img_hash % 1000) / 1000 * conf_range

    return disease, round(confidence, 4)


def detect_disease(image_bytes: bytes, crop_type: str = None) -> dict:
    """
    Detect crop disease from an uploaded image.

    In production: Replace _mock_predict with your trained CNN model inference.
    In development: Uses deterministic mock based on image hash.

    Args:
        image_bytes: Raw bytes of the uploaded image file.
        crop_type:   Optional crop type hint.

    Returns:
        dict with disease detection results.
    """
    # ── Validate image ─────────────────────────────────────────────────────────
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img_width, img_height = img.size
        img_format = img.format or 'UNKNOWN'
        img_mode = img.mode
    except Exception as e:
        logger.warning(f'Could not open image for validation: {e}')
        img_width, img_height = 0, 0
        img_format = 'UNKNOWN'
        img_mode = 'UNKNOWN'

    # ── Predict ────────────────────────────────────────────────────────────────
    # TODO: Replace with real model inference:
    # e.g., from app.ml.model_loader import get_disease_model
    #       model = get_disease_model()
    #       result = model.predict(preprocess(image_bytes))
    disease_record, confidence = _mock_predict(image_bytes, crop_type)

    return {
        'disease_name': disease_record['name'],
        'disease_id': disease_record['id'],
        'crop': disease_record['crop'],
        'confidence': round(confidence * 100, 1),  # Convert to percentage
        'severity': disease_record['severity'],
        'affected_parts': disease_record['affected_parts'],
        'symptoms': disease_record['symptoms'],
        'treatment': disease_record['treatment'],
        'prevention': disease_record['prevention'],
        'organic_treatment': disease_record['organic_treatment'],
        'image_info': {
            'width': img_width,
            'height': img_height,
            'format': img_format,
            'mode': img_mode,
            'size_bytes': len(image_bytes),
        },
        'model_type': 'mock',  # Change to 'cnn' when real model is used
    }
