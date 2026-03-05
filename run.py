"""
Entry Point — Punto de entrada de la aplicación.
"""
import os
from src.interfaces.web.app_factory import create_app

app = create_app()

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    port = int(os.getenv("PORT", 5000))
    app.run(debug=debug, host="0.0.0.0", port=port)
