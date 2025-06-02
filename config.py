import os
from datetime import date
from dotenv import load_dotenv
from typing import Union, get_type_hints


def _parse_bool(value: Union[str, bool]) -> bool:
    return value if type(value) is bool else value.lower() in ("true", "1", "t")


class Config:
    DEBUG: str = "False"
    ENV: str = "dev"
    KAGGLE_USERNAME: str
    KAGGLE_KEY: str
    KAGGLE_CONFIG_DIR: str
    DATA_LAKE: str
    LOG_DIR: str
    LOG_LEVEL: str
    HF_ACCOUNT: str
    HF_TOKEN: str
    today: str = date.today().strftime("%Y-%m-%d")

    def __getattr__(self, name):
        if name.isupper():
            return os.getenv(name)
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )

    def __setattr__(self, name, value):
        if name.isupper():
            super().__setattr__(name, value)

    def __init__(self):
        load_dotenv()
        env = os.environ
        for field in self.__annotations__:
            if not field.isupper():
                continue

            default_value = getattr(self, field, None)
            if default_value is None and env.get(field) is None:
                raise ValueError(f"Environment variable {field} is not set")

            var_type = get_type_hints(self)[field]
            try:
                if var_type is bool:
                    value = _parse_bool(env.get(field, default_value))
                else:
                    value = var_type(env.get(field, default_value))

                self.__setattr__(field, value)
            except ValueError:
                raise ValueError(
                    f"Unable to convert {field} to {var_type} for {env.get(field)}"
                )


cfg = Config()
