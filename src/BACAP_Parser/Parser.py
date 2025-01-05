from collections.abc import Iterable, Iterator

from autoslot import Slots

from .utils import to_collection
from .Datapack import Datapack


class Parser(Slots):
    def __init__(self, *datapacks: Iterable[Datapack] | Datapack):
        self._datapacks: dict[str, Datapack] = {dp.name: dp for dp in to_collection(datapacks, list)}

    def add_datapack(self, datapack: Datapack):
       self._datapacks[datapack.name] = datapack

    def add_datapacks(self, datapacks: Iterable[Datapack]):
        for datapack in datapacks:
           self.add_datapack(datapack)

    def get_datapack(self, name: str) -> Datapack:
        """
        :param name: name of the datapack
        :return: Datapack instance with the specified name
        :raises KeyError: if the datapack does not exist
        """
        if name in self._datapacks:
            return self._datapacks[name]
        raise KeyError(f"Datapack named '{name}' not found.")

    @property
    def datapacks_dict(self) -> dict[str, Datapack]:
        return self._datapacks

    @property
    def datapacks(self) -> list[Datapack]:
        return list(self._datapacks.values())

    @property
    def info(self) -> str:
        return f"Datapacks: {len(self._datapacks)}, Advancements: {sum([len(dp.advancement_manager.adv_list) for dp in self._datapacks.values()])}"