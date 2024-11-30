import os

from langchain_community.document_loaders import DirectoryLoader, TextLoader

from document_loaders.document_loader import DocumentLoader


class TxtLoader(DocumentLoader):
    """
    A class for loading text documents from a specified directory.

    This class uses the DirectoryLoader from langchain_community.document_loaders module to load all text files
    (with .txt extension) from a given directory. It also uses TextLoader to parse the content of each text file.

    Attributes:
    directory (str): The path to the directory containing the text files.

    Methods:
    load_documents(): Load text documents from the specified directory.
    """

    def load_documents(self):
        """
        Load text documents from a specified directory.

        This function uses the DirectoryLoader from langchain_community.document_loaders module to load all text files
        (with .txt extension) from a given directory. It also uses TextLoader to parse the content of each text file.

        Parameters:
        - self.directory (str): The path to the directory containing the text files.

        Returns:
        - List[Document]: A list of Document objects, where each Document represents a text file.

        Raises:
        - ValueError: If the specified directory path is invalid.
        """
        if not os.path.isdir(self.directory):
            raise ValueError("Invalid directory path")

        loader = DirectoryLoader(self.directory, glob="**/*.txt", loader_cls=TextLoader,
                                 loader_kwargs={"encoding": "utf8"})
        return loader.load()
