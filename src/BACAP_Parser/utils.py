import json
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Type

from .ExtendedDict import ExtendedDict
from .constants import ARABIC_TO_ROMAN_MAP


def path_to_mc_path(file_path: Path) -> str:
    """
    :param file_path: Path to file, that starts from namespace
    :return: Path like in mc: relative, without backslashes and suffix.
    """
    parts = file_path.parts
    return f"{parts[0]}:{'/'.join(parts[2:]).rsplit('.', 1)[0]}"


def trim_path_to_namespace(path: Path, namespaces: Sequence[Path]) -> Path:
    """
    Trims the path to the first found namespace, including the namespace, if ф path is a subdirectory of that namespace.

    :param path: The path with namespace in it
    :param namespaces: A list of namespaces to search for
    :return: A new path trimmed to the first namespace found, including it
    """
    namespace_names = [namespace.name for namespace in namespaces]

    for i, part in enumerate(path.parts):
        if part in namespace_names:
            return Path(*path.parts[i:])
    return path

def cut_namespace(string_with_namespace: str) -> str:
    """
    :param string_with_namespace: string that contains namespace
    :return: string without a namespace
    """
    if ":" in string_with_namespace:
        return string_with_namespace.split(":", 1)[1]
    return string_with_namespace


def to_collection[T, C: set | list | tuple | frozenset](item: Iterable[T] | T, constructor: Type[C]) -> C:
    """
    Converts an element or a collection of elements into a specified collection type.

    :param item: An element or a collection of elements.
    :param constructor: The constructor of the target collection, e.g., set, frozenset, tuple.
    :return: A collection of the specified Type.
    """
    if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
        return constructor(item)
    return constructor([item])


def get_file_text(path: Path, encoding: str = None) -> str:
    """

    :param path: Path-object
    :param encoding: Encoding. Default value in config
    :return: File's context
    """
    with path.open(encoding=encoding) as f:
        return f.read()


def safe_load_json(path: Path, encoding: str = "utf-8") -> ExtendedDict | None:
    """

    :param path: Path-object
    :param encoding: Encoding. Default value in config
    :return: File's JSON
    """
    text = get_file_text(path, encoding)
    try:
        return json.loads(text, object_hook=lambda d: ExtendedDict(d))
    except json.decoder.JSONDecodeError:
        try:
            return json.loads(text.replace("\\'", ""), object_hook=lambda d: ExtendedDict(d))
        except json.decoder.JSONDecodeError:
            return None


def arabic_to_rims(value: int | str) -> str:
    """
    Converts an integer to its Roman numeral representation.
    """
    value = int(value)

    if value <= 0:
        raise ValueError("Value must be positive")

    result: list[str] = []
    for num in sorted(ARABIC_TO_ROMAN_MAP.keys(), reverse=True):
        count = value // num
        if count:
            result.append(ARABIC_TO_ROMAN_MAP[num] * count)
            value %= num

    return "".join(result)
