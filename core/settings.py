from functools import lru_cache
from typing import Optional

from databases import DatabaseURL
from pydantic import BaseSettings
from starlette.config import Config

config = Config(".env")


class Settings(BaseSettings):
    """System Settings file for app configuration.

    Args:
        BaseSettings (object): Global base settings for configuration.
    """

    # project declaratives.
    project_name: str = config("PROJECT_NAME", cast=str, default="Inventory System")
    version: str = config("VERSION", cast=str, default="1.0.0")
    app_domain: str = config("APP_DOMAIN", cast=str, default="localhost")
    app_port: str = config("APP_PORT", cast=str, default="8000")
    api_prefix: str = config("API_PREFIX", cast=str, default="/api")
    docs_prefix: str = config("DOCS_PREFIX", cast=str, default="/docs")
    admin_email: str = config("APP_ADMIN_EMAIL", cast=str, default="admin@inventorymanager.com")
    root_url: str = config("ROOT_URL", cast=str, default=f"http://{ app_domain }:{ app_port }")

    # app settings.
    allowed_hosts: str = config("ALLOWED_HOSTS", cast=str, default="")
    environment: str = config("ENVIRONMENT", cast=str, default="DEV")
    secret_key: str = config("SECRET_KEY", cast=str, default="CHANGEME")
    algorithm: str = config("ALGORITHM", cast=str, default="HS256")
    default_page_limit: int = config("DEFAULT_PAGE_LIMIT", cast=int, default=50)
    debug: bool = False
    testing: bool = False

    # db settings
    db_host: str = config("DB_HOST", cast=str, default="db")
    db_port: str = config("DB_PORT", cast=str, default="5432")
    db_name: str = config("DB_NAME", cast=str, default="postgres")
    db_user: str = config("POSTGRES_USER", cast=str)
    db_password: str = config("POSTGRES_PASSWORD", cast=str)
    ssl_mode: str = config("SSL_MODE", cast=str, default="prefer")
    database_url: DatabaseURL = config(
        "DATABASE_URL", cast=DatabaseURL,
        default=f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    db_pool_min_size: int = config("DB_POOL_MIN_SIZE", cast=int, default=2)
    db_pool_max_size: int = config("DB_POOL_MAX_SIZE", cast=int, default=15)
    db_force_roll_back: bool = False

    # mongo db settings
    mongo_db_url : str = config("MONGO_DB_URL", cast=str)
    mongo_db_name : str = config("MONGO_DB_NAME", cast=str)

    # integrations
    payment_service_url: str = config("PAYMENT_SERVICE_URL", cast=str, default="http://localhost:8045")
    payment_intent_enpoint: str = config("PAYMENT_INTENT_ENDPOINT", cast=str, default="/api/v1/payments_intent")
    payment_precheck_enpoint: str = config("PAYMENT_PRECHECK_ENDPOINT", cast=str,
                                           default="/api/v1/rest/payment-prechecks")
    payment_authorize_enpoint: str = config("PAYMENT_AUTHORIZATION_ENDPOINT",
                                            cast=str, default="/api/v1/payment-authorize")


class ProdSettings(Settings):
    debug: bool = False


class DevSettings(Settings):
    debug: bool = True


class TestSettings(Settings):
    debug: bool = True
    testing: bool = True
    db_force_roll_back: bool = True


class FactoryConfig:
    """
    Returns a config instance depends on the ENV_STATE variable.
    """

    def __init__(self, environment: Optional[str] = "DEV"):
        self.environment = environment

    def __call__(self):
        if self.environment == "PROD":
            return ProdSettings()
        elif self.environment == "TEST":
            return TestSettings()
        return DevSettings()


@lru_cache()
def get_app_settings():
    return FactoryConfig(Settings().environment)()
