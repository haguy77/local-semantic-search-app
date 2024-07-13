import os

from langchain_community.document_loaders import DirectoryLoader, TextLoader


class DocumentLoader:
    def __init__(self, directory):
        self.directory = directory

    def load_documents(self):
        if not os.path.isdir(self.directory):
            raise ValueError("Invalid directory path")

        loader = DirectoryLoader(self.directory, glob="**/*.txt", loader_cls=TextLoader,
                                 loader_kwargs={"encoding": "utf8"})
        return loader.load()
