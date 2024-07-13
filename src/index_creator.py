from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS


class IndexCreator:
    def __init__(self):
        self.text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        self.embeddings = HuggingFaceEmbeddings()

    def create_faiss_index(self, documents):
        texts = self.text_splitter.split_documents(documents)
        return FAISS.from_documents(texts, self.embeddings), texts
