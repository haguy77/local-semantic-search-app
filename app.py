import streamlit as st

from src.document_loader import DocumentLoader
from src.index_creator import IndexCreator
from src.indexed_folders_manager import IndexedFoldersManager
from src.search_engine import SearchEngine
from src.utils import truncate_text, folder_needs_update


class HybridSearchApp:
    def __init__(self):
        self.directory = None
        self.db = None
        self.texts = None
        self.search_engine = None
        self.indexed_folders_manager = IndexedFoldersManager()

    def run(self):
        st.title("Hybrid Semantic Search")

        self.show_indexed_folders()
        self.handle_new_folder_input()
        self.create_search_interface()

    def show_indexed_folders(self):
        indexed_folders = self.indexed_folders_manager.get_indexed_folders()
        if indexed_folders:
            st.sidebar.header("Indexed Folders")
            selected_folder = st.sidebar.selectbox("Select a folder", list(indexed_folders.keys()))
            if st.sidebar.button("Use Selected Folder"):
                self.directory = selected_folder
                self.load_and_index_documents(update=True)

    def handle_new_folder_input(self):
        new_directory = st.text_input("Enter a new directory path to search:")
        if new_directory:
            if st.button("Index New Folder"):
                self.directory = new_directory
                self.load_and_index_documents(update=False)

    def load_and_index_documents(self, update=False):
        try:
            indexed_folders = self.indexed_folders_manager.get_indexed_folders()

            if self.directory in indexed_folders and not update:
                st.info(f"Folder '{self.directory}' is already indexed. Loading existing index.")
                # Here you would load the existing index instead of recreating it
                # For simplicity, we'll recreate it in this example

            loader = DocumentLoader(self.directory)
            documents = loader.load_documents()

            index_creator = IndexCreator()
            self.db, self.texts = index_creator.create_faiss_index(documents)

            self.search_engine = SearchEngine(self.db, self.texts)

            if self.directory not in indexed_folders:
                self.indexed_folders_manager.add_indexed_folder(self.directory)
                st.success(f"Folder '{self.directory}' has been indexed successfully.")
            elif update:
                self.indexed_folders_manager.update_indexed_folder(self.directory)
                st.success(f"Folder '{self.directory}' has been updated successfully.")

        except ValueError as e:
            st.error(str(e))

    def create_search_interface(self):
        if self.search_engine:
            query = st.text_input("Enter your search query:")
            alpha = st.slider("Alpha weight (0: BM25 only, 1: Semantic search only)", 0.0, 1.0, 0.5)

            if query:
                results = self.search_engine.hybrid_search(query, alpha)

                st.subheader("Search Results:")
                for i, (doc, score) in enumerate(results, 1):
                    st.write(f"{i}. Score: {score:.4f}")
                    st.write(truncate_text(doc.page_content))
                    st.write("---")

    def check_for_updates(self):
        indexed_folders = self.indexed_folders_manager.get_indexed_folders()
        for folder, info in indexed_folders.items():
            if folder_needs_update(folder, info['last_updated']):
                st.warning(f"Folder '{folder}' has been modified. Consider updating the index.")
                if st.button(f"Update '{folder}'"):
                    self.directory = folder
                    self.load_and_index_documents(update=True)


if __name__ == "__main__":
    app = HybridSearchApp()
    app.run()
