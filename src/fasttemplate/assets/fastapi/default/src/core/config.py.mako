from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings object, responsible for storing environment variables.
    For example, probably project will require Database connection,
    in that case settings could be:
    >>> from pydantic import PostgresDsn
    >>> database_url: PostgresDsn
    """


settings: Settings = Settings()


class FeatureFlags(BaseSettings):
    """
    Feature Flag object, almost the same as a Settings object.
    Needed for concept separation.
    """


feature_flags: FeatureFlags = FeatureFlags()
