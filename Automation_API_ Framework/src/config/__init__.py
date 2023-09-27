import os

from dynaconf import Dynaconf

__all__ = ["settings"]

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_file="settings.yaml",
    SETTINGS_MODULE_FOR_DYNACONF=os.path.join(os.path.dirname(os.path.abspath(__file__)), f'settings.yaml')
)
