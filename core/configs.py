import os
from spotify import AlsaSink


class DefaultConfig:

    plugins = []
    audio_class = lambda x: x
    database_uri = "postgres:///spotique"


class RaspberryConfig(DefaultConfig):
    audio_class = AlsaSink

    @property
    def plugins(self):
        """ Imports from inside as they throw exceptions otherwise """
        from .plugins.raspberry_gpio import RaspberryGPIOPlugin
        return [RaspberryGPIOPlugin]


configs = {
    "raspberry": RaspberryConfig(),
    "_default": DefaultConfig(),
}


def get_config():
    return configs.get(os.environ.get("CORE_ENVIRONMENT"), configs["_default"])
