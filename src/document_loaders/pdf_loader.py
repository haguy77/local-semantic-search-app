import os

from langchain_community.document_loaders import PyMuPDFLoader

from document_loaders.document_loader import DocumentLoader


class PdfLoader(DocumentLoader):
    """
    A class for loading PDF documents from a specified directory.

    This class provides functionality to load PDF documents from a given directory
    using the PyMuPDFLoader.

    Attributes:
        directory (str): The path to the directory containing PDF files.
    """

    def load_documents(self):
        """
        Load all PDF documents from the specified directory.

        This method uses DirectoryLoader to recursively load all PDF files
        from the specified directory and its subdirectories.

        Returns:
            list: A list of loaded document objects.

        Raises:
            ValueError: If the specified directory path is invalid.
        """
        if not os.path.isdir(self.directory):
            raise ValueError("Invalid directory path")

        documents = []
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.pdf'):
                    file_path = os.path.join(root, file)
                    loader = PyMuPDFLoader(file_path)
                    documents.extend(loader.load())
        return documents
