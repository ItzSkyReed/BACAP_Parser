from abc import ABC, abstractmethod

from src.BACAP_Parser.core.Item import AbstractItem


class AbstractDisplay(ABC):
    @property
    @abstractmethod
    def icon(self) -> AbstractItem:
        ...

    @property
    @abstractmethod
    def title(self):