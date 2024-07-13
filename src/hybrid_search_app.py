import streamlit as st
import yaml

from src.document_loader import DocumentLoader
from src.index_creator import IndexCreator
from src.indexed_folders_manager import IndexedFoldersManager
from src.search_engine import SearchEngine
from src.utils import truncate_text, folder_needs_update


class HybridSearchApp:
    def __init__(self):
        if 'initialized' not in st.session_state:
            self.initialize_session_state()

    @staticmethod
    def initialize_session_state():
        st.session_state.initialized = True
        st.session_state.directory = None
        st.session_state.db = None
        st.session_state.texts = None
        st.session_state.search_engine = None
        st.session_state.indexed_folders_manager = IndexedFoldersManager()
        with open("config.yaml", "r") as f:
            st.session_state.config = yaml.safe_load(f)

    def run(self):
        st.title("Hybrid Semantic Search")

        st.sidebar.header("Model Configuration")
        st.sidebar.text(f"Embedding Model: {st.session_state.config['embedding_model']}")
        st.sidebar.text(f"Cross-Encoder Model: {st.session_state.config['cross_encoder_model']}")

        self.show_indexed_folders()
        self.handle_new_folder_input()
        self.create_search_interface()

    def show_indexed_folders(self):
        indexed_folders = st.session_state.indexed_folders_manager.get_indexed_folders()
        if indexed_folders:
            st.sidebar.header("Indexed Folders")
            selected_folder = st.sidebar.selectbox("Select a folder", list(indexed_folders.keys()))
            if st.sidebar.button("Use Selected Folder"):
                st.session_state.directory = selected_folder
                self.load_and_index_documents(update=True)

    def handle_new_folder_input(self):
        new_directory = st.text_input("Enter a new directory path to search:")
        if new_directory and new_directory != st.session_state.directory:
            if st.button("Index New Folder"):
                st.session_state.directory = new_directory
                self.load_and_index_documents(update=False)

    @staticmethod
    def load_and_index_documents(update=False):
        try:
            indexed_folders = st.session_state.indexed_folders_manager.get_indexed_folders()

            if st.session_state.directory in indexed_folders and not update:
                st.info(f"Folder '{st.session_state.directory}' is already indexed. Loading existing index.")
                # Here you would load the existing index instead of recreating it
                # For simplicity, we'll recreate it in this example

            loader = DocumentLoader(st.session_state.directory)
            documents = loader.load_documents()

            index_creator = IndexCreator()
            st.session_state.db, st.session_state.texts = index_creator.create_faiss_index(documents)

            st.session_state.search_engine = SearchEngine(st.session_state.db, st.session_state.texts)

            if st.session_state.directory not in indexed_folders:
                st.session_state.indexed_folders_manager.add_indexed_folder(st.session_state.directory)
                st.success(f"Folder '{st.session_state.directory}' has been indexed successfully.")
            elif update:
                st.session_state.indexed_folders_manager.update_indexed_folder(st.session_state.directory)
                st.success(f"Folder '{st.session_state.directory}' has been updated successfully.")

        except ValueError as e:
            st.error(str(e))

    @staticmethod
    def create_search_interface():
        if st.session_state.search_engine:
            query = st.text_input("Enter your search query:")
            st.sidebar.header("Search Configuration")
            alpha = st.sidebar.slider("Alpha weight (0: BM25 only, 1: Semantic search only)", 0.0, 1.0, 0.5)
            top_k = st.sidebar.slider("Number of results", 1, 20, 5)

            if query:
                results = st.session_state.search_engine.hybrid_search(query, alpha, top_k)

                st.subheader("Search Results:")
                for i, (doc, score) in enumerate(results, 1):
                    st.write(f"{i}. Score: {score:.4f}")
                    st.write(truncate_text(doc.page_content))
                    st.write("---")

    def check_for_updates(self):
        indexed_folders = st.session_state.indexed_folders_manager.get_indexed_folders()
        for folder, info in indexed_folders.items():
            if folder_needs_update(folder, info['last_updated']):
                st.warning(f"Folder '{folder}' has been modified. Consider updating the index.")
                if st.button(f"Update '{folder}'"):
                    st.session_state.directory = folder
                    self.load_and_index_documents(update=True)
