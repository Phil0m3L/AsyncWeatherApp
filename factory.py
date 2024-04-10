from typing import Any

from quart import Quart
from quart_wtf import CSRFProtect


csrf: CSRFProtect = Any


def create_app() -> Quart:
    app = Quart(__name__, static_url_path="/assets", static_folder="assets")
    app.config.from_pyfile("config.py")

    global csrf
    csrf = CSRFProtect()
    csrf.init_app(app)

    from blueprints.meta import meta_bp
    from blueprints.weather import weather_bp

    app.register_blueprint(meta_bp)
    app.register_blueprint(weather_bp)

    return app
