"""
Smart Agro - ML Model Loader (Singleton)
==========================================
Loads ML models once at startup and caches them for reuse.
This prevents slow model loading on every request.

Usage:
    from app.ml.model_loader import ModelLoader
    model_loader = ModelLoader()
    crop_model = model_loader.get_crop_model()
"""

import os
import pickle
import logging
import threading

logger = logging.getLogger(__name__)

# Directory where pkl/h5 model files are stored
MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')


class ModelLoader:
    """
    Thread-safe singleton for loading and caching ML models.
    Models are loaded lazily on first access.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._crop_model = None
        self._crop_model_loaded = False
        self._disease_model = None
        self._disease_model_loaded = False
        self._initialized = True
        logger.info('ModelLoader singleton initialized.')

    def get_crop_model(self):
        """
        Load and return the crop recommendation sklearn model.
        Expects a scikit-learn Pipeline or model at: app/ml/models/crop_model.pkl

        Returns:
            The loaded model object, or None if not available.
        """
        if not self._crop_model_loaded:
            model_path = os.path.join(MODELS_DIR, 'crop_model.pkl')
            if os.path.exists(model_path):
                try:
                    with open(model_path, 'rb') as f:
                        self._crop_model = pickle.load(f)
                    logger.info(f'Crop model loaded from {model_path}')
                except Exception as e:
                    logger.error(f'Failed to load crop model: {e}')
                    self._crop_model = None
            else:
                logger.info(
                    f'Crop model not found at {model_path}. '
                    'Rule-based recommendation will be used.'
                )
                self._crop_model = None
            self._crop_model_loaded = True

        return self._crop_model

    def get_disease_model(self):
        """
        Load and return the disease detection deep learning model.
        Expects a Keras/TF SavedModel or .h5 at: app/ml/models/disease_model.h5
        Or a pickle at: app/ml/models/disease_model.pkl

        Returns:
            The loaded model, or None if not available.
        """
        if not self._disease_model_loaded:
            h5_path = os.path.join(MODELS_DIR, 'disease_model.h5')
            pkl_path = os.path.join(MODELS_DIR, 'disease_model.pkl')

            if os.path.exists(h5_path):
                try:
                    # Requires tensorflow/keras: from tensorflow import keras
                    # self._disease_model = keras.models.load_model(h5_path)
                    logger.info(f'Disease model (h5) found at {h5_path}. Install TensorFlow to use.')
                except Exception as e:
                    logger.error(f'Failed to load disease model: {e}')
                    self._disease_model = None

            elif os.path.exists(pkl_path):
                try:
                    with open(pkl_path, 'rb') as f:
                        self._disease_model = pickle.load(f)
                    logger.info(f'Disease model loaded from {pkl_path}')
                except Exception as e:
                    logger.error(f'Failed to load disease model: {e}')
                    self._disease_model = None
            else:
                logger.info(
                    f'Disease model not found at {h5_path} or {pkl_path}. '
                    'Mock predictions will be used.'
                )
                self._disease_model = None

            self._disease_model_loaded = True

        return self._disease_model

    def reload_models(self):
        """
        Force reload of all models. Useful after updating model files without restarting.
        """
        self._crop_model_loaded = False
        self._disease_model_loaded = False
        self._crop_model = None
        self._disease_model = None
        logger.info('All models cleared. They will be reloaded on next access.')

    @property
    def status(self) -> dict:
        """Return model availability status."""
        return {
            'crop_model': 'loaded' if self._crop_model else 'not_available',
            'disease_model': 'loaded' if self._disease_model else 'not_available',
        }


# Global singleton instance
model_loader = ModelLoader()
