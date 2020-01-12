from collections.abc import Mapping
from pathlib import Path

import yaml


with open("config-default.yml", encoding="UTF-8") as f:
    _CONFIG_YAML = yaml.safe_load(f)


def _recursive_update(original, new):
    """
    Helper method which implements a recursive `dict.update`
    method, used for updating the original configuration with
    configuration specified by the user.
    """

    for key, value in original.items():
        if key not in new:
            continue

        if isinstance(value, Mapping):
            if not any(isinstance(subvalue, Mapping) for subvalue in value.values()):
                original[key].update(new[key])
            _recursive_update(original[key], new[key])
        else:
            original[key] = new[key]


if Path("config.yml").exists():
    with open("config.yml", encoding="UTF-8") as f:
        user_config = yaml.safe_load(f)
    _recursive_update(_CONFIG_YAML, user_config)


class YAMLGetter(type):
    subsection = None

    def __getattr__(cls, name):
        name = name.lower()

        try:
            if cls.subsection is not None:
                return _CONFIG_YAML[cls.section][cls.subsection][name]
            return _CONFIG_YAML[cls.section][name]
        except KeyError:
            dotted_path = '.'.join(
                (cls.section, cls.subsection, name)
                if cls.subsection is not None else (cls.section, name)
            )
            raise

    def __getitem__(cls, name):
        return cls.__getattr__(name)


# Dataclasses
class Bot(metaclass=YAMLGetter):
    section = "bot"

    prefix: str
    token: str


class Emojis(metaclass=YAMLGetter):
    section = "emojis"

    warrior: str
    warlock: str
    rogue: str
    priest: str
    paladin: str
    mage: str
    hunter: str
    druid: str


class Guild(metaclass=YAMLGetter):
    section = "guild"

    id: int


class Channels(metaclass=YAMLGetter):
    section = "guild"
    subsection = "channels"

    welcome: int

    warrior: int
    warlock: int
    rogue: int
    priest: int
    paladin: int
    mage: int
    hunter: int
    druid: int


class Roles(metaclass=YAMLGetter):
    section = "guild"
    subsection = "roles"

    officer: int
    gm: int
    social: int

    warrior: int
    warlock: int
    rogue: int
    priest: int
    paladin: int
    mage: int
    hunter: int
    druid: int
