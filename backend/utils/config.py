import os
from dotenv import load_dotenv
from pydantic import SecretStr
from functools import lru_cache

load_dotenv()


class Config:
    OPENAPI_BASE_URL: SecretStr = SecretStr(os.getenv("OPENROUTER_BASE_URL", ""))
    OPENAPI_API_KEY: SecretStr = SecretStr(os.getenv("OPENROUTER_API_KEY", ""))


    @classmethod
    def validate_config(cls) -> None:
        required_secrets = {
            "OPENAPI_BASE_URL": cls.OPENAPI_BASE_URL.get_secret_value(),
            "OPENAPI_API_KEY": cls.OPENAPI_API_KEY.get_secret_value(),
        }

        missing_secrets = [
            var_name
            for var_name, var_value in required_secrets.items()
            if not var_value or var_value == "<secret_here>"
        ]

        if missing_secrets:
            raise ValueError(
                f"Missing required secret environment variables: {', '.join(missing_secrets)}. "
                f"Please check your .env file."
            )

    @classmethod
    def get_base_url(cls) -> str:
        return cls.OPENAPI_BASE_URL.get_secret_value()

    @classmethod
    def get_api_key(cls) -> str:
        return cls.OPENAPI_API_KEY.get_secret_value()



@lru_cache(maxsize=1)
def getConfig() -> Config:
    config = Config()
    config.validate_config()
    return config