"""Set configuration  settings."""
import os


class Config(object):
    """Common configuration Setting."""
    SQLALCHEMY_DATABASE_URI= os.getenv('DATABASE_URL')
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Configuration setting at development stage."""

    DEBUG = True


class TestingConfig(Config):
    """Configuration setting at testing stage."""
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:mypass_bootcamp@localhost:5432/test_hello_books"
    TESTING = True


class ProductionConfig(Config):
    """Configuration setting at production stage."""

    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
