from collections.abc import Iterable
from pathlib import Path

from autoslot import Slots

from . import to_collection
from .AdvType import AdvTypeManager


class Datapack(Slots):
    def __init__(self, name: str, path: Path, adv_type_manager: AdvTypeManager, reward_namespace: str, technical_tabs: Iterable[str] | None = None):

        from .Advancement import AdvancementManager

        self._name = name
        self._path = path

        technical_tabs = to_collection(technical_tabs, tuple)


        if self._path.is_absolute():
            raise ValueError("Path must be relative")
        if not (self._path / "pack.mcmeta").exists():
            raise FileNotFoundError("pack.mcmeta not found in the datapack root, may be this is a wrong path")

        if not (self._path / "data").exists() or not (self._path / "data").is_dir():
            raise ValueError("data folder does not exist")

        self._namespaces = [entry for entry in (self._path / "data").iterdir() if entry.is_dir()]

        if reward_namespace not in [entry.name for entry in self._namespaces]:
            raise FileNotFoundError(f"Reward namespace \"{reward_namespace}\" does not exist, possible namespaces: {[entry.name for entry in self._namespaces]}")

        self._reward_namespace = reward_namespace

        self._reward_namespace_path = next(entry for entry in self._namespaces if entry.name == reward_namespace)

        self._adv_type_manager = adv_type_manager
        self._advancement_manager = AdvancementManager(self._path, self, technical_tabs)

    def __repr__(self):
        return f"Datapack('{self._name}')"

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def adv_type_manager(self):
        return self._adv_type_manager

    @property
    def advancement_manager(self):
        return self._advancement_manager

    @property
    def reward_namespace(self):
        return self._reward_namespace

    @property
    def reward_namespace_path(self):
        return self._reward_namespace_path

    @property
    def namespaces(self):
        return self._namespaces