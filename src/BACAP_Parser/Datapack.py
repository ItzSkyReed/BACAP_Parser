from collections.abc import Iterable
from pathlib import Path

from .utils import to_collection
from .AdvType import AdvTypeManager
from .TabNameMapper import TabNameMapper

class Datapack:
    def __init__(self, name: str, path: Path, adv_type_manager: AdvTypeManager, reward_namespace: str | None = None, technical_tabs: Iterable[str] | None = None, tab_name_mapper: TabNameMapper = TabNameMapper()):
        """
        :param name: Name of the datapack that will be used to identify it in Parser instance
        :param path: Path to the datapack
        :param adv_type_manager: AdvTypeManager instance
        :param reward_namespace: namespace where rewards (exp, trophy, reward) are stored.
        If None Exp, Trophy and item rewards will not be parsed.
        :param technical_tabs: a list of tabs with technical advancements
        :param tab_name_mapper: TabNameMapper instance with custom tabs, if not specified.
        It will be created automatically with default BACAP tabs
        """
        from .Advancement import AdvancementManager

        self._name = name
        self._path = path

        technical_tabs = to_collection(technical_tabs, tuple)

        if not (self._path / "pack.mcmeta").exists():
            raise FileNotFoundError("pack.mcmeta not found in the datapack root, may be this is a wrong path")

        if not (self._path / "data").exists() or not (self._path / "data").is_dir():
            raise ValueError("data folder does not exist")

        self._namespaces = [entry for entry in (self._path / "data").iterdir() if entry.is_dir()]

        if reward_namespace is not None:
            if reward_namespace not in [entry.name for entry in self._namespaces]:
                raise FileNotFoundError(f"Reward namespace \"{reward_namespace}\" does not exist, possible namespaces: {[entry.name for entry in self._namespaces]}")
            self._reward_namespace_path = next(entry for entry in self._namespaces if entry.name == reward_namespace)
        else:
            self._reward_namespace_path = None

        self._reward_namespace = reward_namespace

        self._adv_type_manager = adv_type_manager
        self._advancement_manager = AdvancementManager(self._path, self, technical_tabs)
        self._tab_name_mapper = tab_name_mapper

    def __repr__(self):
        return f"Datapack('{self._name}')"

    @property
    def name(self) -> str:
        """
        :return: Name of the datapack
        """
        return self._name

    @property
    def path(self):
        """
        :return: Path to the datapack
        """
        return self._path

    @property
    def adv_type_manager(self):
        """
        :return: AdvTypeManager instance of the datapack
        """
        return self._adv_type_manager

    @property
    def advancement_manager(self):
        """
        :return: AdvancementManager instance of the datapack
        """
        return self._advancement_manager

    @property
    def reward_namespace(self):
        """
        :return: namespace that contains advancement rewards of the datapack
        """
        return self._reward_namespace

    @property
    def reward_namespace_path(self):
        """
        :return: path to the reward_namespace
        """
        return self._reward_namespace_path

    @property
    def namespaces(self):
        """
        :return: list of namespaces of the datapack
        """
        return self._namespaces

    @property
    def tab_name_mapper(self):
        """
        :return: TabMap instance of the datapack
        """
        return self._tab_name_mapper