"""File upload service for handling images."""
import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename
from PIL import Image


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_IMAGE_SIZE = (1200, 1200)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, subfolder='general'):
    """
    Save an uploaded file to the upload folder.

    Args:
        file: FileStorage object from Flask request.
        subfolder: Subfolder within uploads (e.g., 'crops', 'profiles', 'disease').

    Returns:
        Tuple (filename, url_path) or raises ValueError on invalid file.
    """
    if not file or file.filename == '':
        raise ValueError('No file provided.')

    if not allowed_file(file.filename):
        raise ValueError(f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}')

    # Generate unique filename
    ext = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = f'{uuid.uuid4().hex}.{ext}'

    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    target_folder = os.path.join(upload_folder, subfolder)
    os.makedirs(target_folder, exist_ok=True)

    filepath = os.path.join(target_folder, unique_filename)

    # Save and optionally resize the image
    try:
        img = Image.open(file)
        img.thumbnail(MAX_IMAGE_SIZE, Image.LANCZOS)
        # Convert RGBA to RGB if needed (for JPEG)
        if img.mode in ('RGBA', 'P') and ext in ('jpg', 'jpeg'):
            img = img.convert('RGB')
        img.save(filepath, optimize=True, quality=85)
    except Exception:
        # Fallback to direct save if PIL processing fails
        file.seek(0)
        file.save(filepath)

    url_path = f'/uploads/{subfolder}/{unique_filename}'
    return unique_filename, url_path


def delete_file(url_path):
    """Delete a file given its URL path."""
    if not url_path:
        return
    try:
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        # url_path starts with /uploads/
        relative = url_path.lstrip('/uploads/')
        filepath = os.path.join(upload_folder, relative)
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f'[FileService] Could not delete file {url_path}: {e}')
