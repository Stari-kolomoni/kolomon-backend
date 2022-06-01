from pathlib import Path
from typing import Union

from .configuration_base import TOMLConfig, BASE_PROJECT_DIR


class _DatabaseConfiguration:
    """
    A smaller portion of the configuration.
    This class parses values in the "database" table.
    """
    def __init__(self, database_table: TOMLConfig):
        self.HOST = database_table.get("host", raise_on_missing_key=True)
        self.PORT = database_table.get("port", raise_on_missing_key=True)

        self.USER = database_table.get("user", raise_on_missing_key=True)
        self.PASSWORD = database_table.get("password", raise_on_missing_key=True)
        self.DATABASE_NAME = database_table.get("database_name", raise_on_missing_key=True)


class _TestDatabaseConfiguration:
    """
    A smaller portion of the configuration.
    This class parses values in the "database_test" table.
    """
    def __init__(self, database_table: TOMLConfig):
        self.HOST = database_table.get("host", raise_on_missing_key=True)
        self.PORT = database_table.get("port", raise_on_missing_key=True)

        self.USER = database_table.get("user", raise_on_missing_key=True)
        self.PASSWORD = database_table.get("password", raise_on_missing_key=True)
        self.DATABASE_NAME = database_table.get("database_name", raise_on_missing_key=True)


class _JWTConfiguration:
    """
    A smaller portion of the configuration.
    This class parses values in the "JWT" table.
    """
    def __init__(self, jwt_table: TOMLConfig):
        self.SECRET_KEY = jwt_table.get("secret_key", raise_on_missing_key=True)
        self.ALGORITHM = jwt_table.get("algorithm", raise_on_missing_key=True)
        self.ACCESS_TOKEN_EXPIRE_MINUTES = jwt_table.get("access_token_expire_minutes", raise_on_missing_key=True)


class KolomoniConfiguration:
    """
    Main configuration class that contains all the available options for Stari Kolomoni's configuration.
    """
    def __init__(self, configuration: TOMLConfig):
        self._config: TOMLConfig = configuration

        ### Tables
        self._database = self._config.get_table("database", raise_on_missing_key=True)
        self._jwt = self._config.get_table("JWT", raise_on_missing_key=True)

        ### Pass individual tables around to each specific "group" of the configuration.
        self.DATABASE = _DatabaseConfiguration(self._database)
        self.TEST_DATABASE = _TestDatabaseConfiguration(self._database)
        self.JWT = _JWTConfiguration(self._jwt)

    @classmethod
    def from_file_path(cls, configuration_filepath: Union[str, Path]) -> "KolomoniConfiguration":
        """
        Initialize a new instance by reading from the specified configuration file.

        :param configuration_filepath: File path of the config file to read from.
        :return: KolomoniConfiguration instance with the parsed values.
        """
        return cls(TOMLConfig.from_filename(str(configuration_filepath)))


configuration_file_path = BASE_PROJECT_DIR / "data" / "configuration.toml"

## IMPORTANT
# This is the configuration that should be imported and used from elsewhere.
# Don't create new instances of KolomoniConfiguration (unnecesarry).
##
config = KolomoniConfiguration.from_file_path(configuration_file_path)
