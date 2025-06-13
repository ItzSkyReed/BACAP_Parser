from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from typing import Self

from .Criteria import AbstractCriteria, Criteria


class AbstractCriteriaList(list, ABC):
    @property
    @abstractmethod
    def is_all_impossible(self) -> bool:
        ...

    @abstractmethod
    def append(self, criteria: AbstractCriteria) -> None:
        ...

    @abstractmethod
    def extend(self, criteria_list: Self):
        ...

    @abstractmethod
    def insert(self, index: int, criteria: AbstractCriteria):
        ...

    @abstractmethod
    def sort(self, *, key: Callable = None, reverse: bool = False):
        ...

    @abstractmethod
    def remove(self, criteria: AbstractCriteria | str):
        ...

    @abstractmethod
    def __eq__(self, other: Self) -> bool:
        ...

    @abstractmethod
    def __contains__(self, criteria: AbstractCriteria) -> bool:
        ...

    @abstractmethod
    def __ne__(self, other: Self) -> bool:
        ...

    @abstractmethod
    def __add__(self, other: Self) -> Self:
        ...

    @abstractmethod
    def __or__(self, other: Self) -> Self:
        ...

    @abstractmethod
    def __and__(self, other: Self) -> Self:
        ...

    @abstractmethod
    def __xor__(self, other: Self):
        ...


class CriteriaList(AbstractCriteriaList):
    def __init__(self, adv_criteria: dict | AbstractCriteria | list | Self | None = None, *, criteria_class: AbstractCriteria | Criteria = Criteria):
        """
        :param adv_criteria: dict with parsed criteria JSON, list of Criteria, CriteriaList, single Criteria or None
        """
        super().__init__()
        if adv_criteria is None:
            return

        elif isinstance(adv_criteria, CriteriaList):
            self.extend(adv_criteria)

        elif isinstance(adv_criteria, dict):
            for name, crit in adv_criteria.items():
                criteria = criteria_class.__init__(name, crit["trigger"], conditions=crit.get("conditions"))
                self.append(criteria)

        elif isinstance(adv_criteria, AbstractCriteria):
            self.append(adv_criteria)

        elif isinstance(adv_criteria, list):
            if not all(isinstance(item, Criteria) for item in adv_criteria):
                raise TypeError("All elements must be instances of the Criteria class")
            self.extend(adv_criteria)
        else:
            raise TypeError("Argument must be a dict, Criteria object, or a list of Criteria objects")

    def is_all_impossible(self) -> bool:
        """
        :return: True if all criteria are impossible, False otherwise
        """
        return all(criteria.is_impossible for criteria in self)

    def __repr__(self):
        return super().__repr__()

    def append(self, criteria: AbstractCriteria):
        if not isinstance(criteria, AbstractCriteria):
            raise TypeError("Element must be an instance of the Criteria class")
        super().append(criteria)

    def __str__(self):
        return super().__str__()

    def extend(self, criteria_list: Self | Iterable[AbstractCriteria]):
        if not all(isinstance(criteria, AbstractCriteria) for criteria in criteria_list):
            raise TypeError("All elements must be instances of the Criteria class")
        super().extend(criteria_list)

    def insert(self, index, criteria) -> None:
        if not isinstance(criteria, AbstractCriteria):
            raise TypeError("Element must be an instance of the Criteria class")
        super().insert(index, criteria)

    def sort(self, *, key: Callable = None, reverse: bool = False):
        if key is None:
            key = lambda criteria: criteria.name
        super().sort(key=key, reverse=reverse)

    def remove(self, criteria: AbstractCriteria | str):
        """
        :param criteria: Criteria to remove (will check both trigger and name string equation), or criteria name
        """
        if isinstance(criteria, AbstractCriteria):
            for crit in self:
                if criteria.name == crit.name and criteria.trigger == crit.trigger:
                    self.remove(criteria)
        else:
            for criteria in self:
                if criteria.name == criteria:
                    self.remove(criteria)

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return super().__eq__(other)

    def __contains__(self, criteria: AbstractCriteria) -> bool:
        """
        :param criteria: Criteria to check
        :return: True if criteria is in CriteriaList, False otherwise
        """
        if not isinstance(criteria, AbstractCriteria):
            raise TypeError("Element must be an instance of the Criteria class")
        return any(crt.name == criteria.name and crt.trigger == criteria.trigger for crt in self)

    def __ne__(self, other: Self) -> bool:
        return super().__ne__(other)

    def __add__(self, other: Self) -> Self:
        """
        :param other: Other CriteriaList
        :return: New CriteriaList that contains both lists
        """
        if not isinstance(other, self.__class__):
            raise TypeError("Element must be an instance of the CriteriaList class")
        new_list = CriteriaList(self)
        new_list.extend(other)
        return new_list

    def __or__(self, other: Self) -> Self:
        """
        :param other: Other CriteriaList
        :return: New CriteriaList that contains elements from both lists
        """
        if not isinstance(other, self.__class__):
            raise TypeError("Element must be an instance of the CriteriaList class")
        return self + other

    def __and__(self, other: Self) -> Self:
        """
        :param other: Other CriteriaList
        :return: New CriteriaList that contains elements that are in both lists
        """
        if not isinstance(other, self.__class__):
            raise TypeError("Other element must be an instance of the CriteriaList class")
        new_list = CriteriaList()
        for crit in self:
            if crit in self and crit in other:
                new_list.append(crit)
        return new_list

    def __xor__(self, other: Self) -> Self:
        if not isinstance(other, self.__class__):
            raise TypeError("Other element must be an instance of the CriteriaList class")
        new_list = CriteriaList()

        for crit in self:
            if crit not in other:
                new_list.append(crit)

        for crit in other:
            if crit not in self:
                new_list.append(crit)

        return new_list
