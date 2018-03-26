"""Set configuration  settings."""
import os


class Config(object):
    """Common configuration Setting."""

    DEBUG = False


class DevelopmentConfig(Config):
    """Configuration setting at development stage."""

    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """Configuration setting at production stage."""

    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
