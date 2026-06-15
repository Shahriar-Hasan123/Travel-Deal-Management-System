"""Application configuration."""

class Config:
    """
    Application Configuration
    """
    # SQLite database
    SQLALCHEMY_DATABASE_URI = "sqlite:///travel.db"
    # Disable unnecessary tracking
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Enable debug mode
    DEBUG = True
