"""Configuration File
"""
import os


class Config():
    """Default configuration variables
    """
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # Protecting against XSS
    SESSION_COOKIE_SAMESITE = 'Lax'


class ProductionConfig(Config):
    """'Default configuration for production environments

    Args:
        Config (Object): Base Config object
    """

    # os.urandom(24).hex()
    SECRET_KEY: str = os.getenv('SECRET_KEY')

    # Protecting against XSS
    # SESSION_COOKIE_SECURE: bool = True
    # REMEMBER_COOKIE_HTTPONLY: bool = True

    API_URL_BASE: str = os.getenv('API_URL_BASE')
# 

class DevelopmentConfig(Config):
    """'Default configuration for development environments

    Args:
        Config (Object): Base Config object
    """
    DEBUG: bool = False

    SECRET_KEY: str = os.getenv('SECRET_KEY')

    API_URL_BASE: str = os.getenv('API_URL_BASE')


class TestingConfig(Config):
    """'Default configuration for testing environments

    Args:
        Config (Object): Base Config object
    """
    TESTING: bool = True