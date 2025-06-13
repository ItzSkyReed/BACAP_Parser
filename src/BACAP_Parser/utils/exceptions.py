class AdvancementException(Exception):
    """
    A default exception class for handling errors during advancement initialization.
    Serves as a base class for creating other specific advancement-related exceptions.
    """

    def __init__(self, message="Something went wrong"):
        super().__init__(message)


class JSONParsingError(AdvancementException):
    """
    Exception raised when parsing JSON data fails.
    Indicates that the provided JSON data could not be successfully parsed.
    """

    def __init__(self):
        super().__init__("Failed to parse JSON data")


class InvalidRewardFunction(AdvancementException):
    """
    Exception raised when an invalid reward function is passed, or reward function does not exist.
    """
    def __init__(self):
        super().__init__("Advancement does not contain a valid reward function")


class MissingTitleField(AdvancementException):
    """
    Exception raised when a title does not exist.
    """
    def __init__(self):
        super().__init__("Advancement does not contain a title")


class MissingDescriptionField(AdvancementException):
    """
    Exception raised when description does not exist.
    """
    def __init__(self):
        super().__init__("Advancement does not contain a description")
