from abc import ABC, abstractmethod


class AbstractTab(ABC):

    @property
    @abstractmethod
    def display_name(self) -> str:
        ...

    @property
    @abstractmethod
    def folder_structure(self) -> str:
        ...

    @property
    @abstractmethod
    def internal_name(self) -> str:
        ...


class Tab(AbstractTab):
    """
    This class describes a tab in the file system and in Minecraft,
    including the display name, internal name, and the corresponding folder in the system.
    """

    def __init__(self, display_name: str, folder_structure: str, internal_name: str):
        self._display_name = display_name
        self._folder_structure = folder_structure
        self._internal_name = internal_name

    @property
    def display_name(self) -> str | None:
        """
        Display name of the tab, that you can see in Minecraft advancement menu, name of the root advancement of the tab.
        Can be ``None`` if the tab is not from BACAP and ``TabNameMapper`` is not used.
        """
        return self._display_name

    @property
    def folder_structure(self) -> str:
        """
        A string representing the folder structure (can used to construct a relative path) after the "datapack"/data/"namespace"/advancement directories.
        For example, in the path "bacap/data/blazeandcave/advancement/stuff/hard", this would be "stuff/hard".
        """
        return self._folder_structure

    @property
    def internal_name(self) -> str | None:
        """
        The internal name of the tab, used in rewards. While it typically matches the folder structure, this is not always the case, especially in addons.
        The value is derived from the ``reward_mcpath``, if it exists.
        It is ``None`` for all ``TechnicalAdvancements``
        """
        return self._internal_name
