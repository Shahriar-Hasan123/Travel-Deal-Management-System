from flask import Flask, request, jsonify
from config import Config
from database.models import db
from routes.deal_routes import deal_bp
from routes.stats_routes import stats_bp
from utils.logger import get_logger

logger = get_logger(__name__)


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize db
    db.init_app(app)

    # register blueprint
    app.register_blueprint(deal_bp)
    app.register_blueprint(stats_bp)

    # create all db tables
    with app.app_context():
        db.create_all()

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
            f"Response — {request.method} {request.path} " f"→ {response.status_code}"
        )

        return response
    
    # -------Global Error Handlers-----------
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "message": "Endpoint not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"success": False, "message": "Method not allowed"}), 405

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return jsonify({"success": False, "message": "Internal server error"}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
