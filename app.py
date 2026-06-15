from flask import Flask
from config import Config
from database.models import db
from routes.deal_routes import deal_bp


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize db
    db.init_app(app)

    # register blueprint
    app.register_blueprint(deal_bp)

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
