import yaml
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


class IndexCreator:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=250,
                                                            separators=["\n\n", "\n", "\t"])
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        self.embeddings = HuggingFaceEmbeddings(model_name=config["embedding_model"])

    def create_faiss_index(self, documents):
        texts = [text for text in self.text_splitter.split_documents(documents) if
                 len(text.page_content.split(" ")) > 3]
        return FAISS.from_documents(texts, self.embeddings), texts
