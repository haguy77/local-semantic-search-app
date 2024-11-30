from abc import ABC, abstractmethod


class DocumentLoader(ABC):
    """
    Abstract base class for loading documents from a specified directory.

    Attributes:
    directory (str): The directory from which to load documents.

    Methods:
    load_documents(): Abstract method to be implemented by subclasses.
    """

    def __init__(self, directory):
        """
        Initialize a DocumentLoader instance.

        Parameters:
        directory (str): The directory from which to load documents.
        """
        self.directory = directory

    @abstractmethod
    def load_documents(self):
        """
        Abstract method to be implemented by subclasses.

        Returns:
        list: A list of loaded documents.
        """
        pass
