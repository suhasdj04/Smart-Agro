"""
Smart Agro - Flask Application Entry Point
==========================================
Run this file to start the development server.
"""

from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    app.run(
        debug=os.getenv('FLASK_ENV', 'development') == 'development',
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000))
    )
