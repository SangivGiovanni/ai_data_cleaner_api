from flask import Flask
import os
import logging
import sys

def create_app():
    app = Flask(__name__)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Ensure upload folder exists
    os.makedirs('uploads', exist_ok=True)

    from .routes.upload_routes import upload_bp
    from .routes.process_routes import process_bp

    app.register_blueprint(upload_bp)
    app.register_blueprint(process_bp)

    return app
