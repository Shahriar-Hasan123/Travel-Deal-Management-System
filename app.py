from flask import Flask, request
from config import Config
from database.models import db
from routes.deal_routes import deal_bp
from routes.stats_routes import stats_bp
from utils.logger import get_logger


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize db
    db.init_app(app)

    # register blueprint
    app.register_blueprint(deal_bp)
    app.register_blueprint(stats_bp)

    logger = get_logger(__name__)

    # -----Middleware-----
    @app.before_request
    def before_each_request():
        """Logs every incoming request."""
        logger.info(f"Incoming request — {request.method} {request.path}")

    @app.after_request
    def after_each_request(response):
        """Logs every response and records API stats automatically."""
        from services.stats_service import record_request

        success = response.status_code < 400

        destination = None
        if request.path == "/deals/search" and request.method == "GET":
            destination = request.args.get("destination", "").strip() or None

        record_request(success=success, destination=destination)

        logger.info(
            f"Response — {request.method} {request.path} "
            f"→ {response.status_code}"
        )

        return response

    # Global error handlers
    @app.errorhandler(Exception)
    def handle_exception(error):
        return ({"message": str(error)}, 500)

    # create all db tables
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
