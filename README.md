# Hybrid Semantic Search Engine

## Overview

This project implements a hybrid semantic search engine using Langchain and Streamlit. It combines the power of semantic search (using cosine similarity) with traditional keyword-based search (BM25) to provide highly relevant results from a collection of documents.

The application allows users to index local directories, save indexed folders for quick access, and perform hybrid searches with adjustable weighting between semantic and keyword-based results.

## Features

- **Hybrid Search**: Combine semantic search and BM25 for optimal results
- **Reranking**: Use CrossEncoder to refine search results
- **Configurable Models**: Easily change embedding and cross-encoder models via config file
- **Local Directory Indexing**: Index and search through documents in local directories
- **Adjustable Search Parameters**: Fine-tune the balance between semantic and keyword-based search and the number of results
- **Folder Management**: Save and manage indexed folders for quick access
- **Update Detection**: Automatically detect changes in indexed folders and prompt for updates
- **User-Friendly Interface**: Easy-to-use Streamlit-based web interface

## Installation

1. Clone the repository:\
   <code> git clone https://github.com/yourusername/hybrid-semantic-search.git </code>
   <br>
   <code> cd hybrid-semantic-search </code>

2. Install the required dependencies:\
   <code> pip install -r requirements.txt </code>

## Usage

1. Run the Streamlit app:\
   <code> streamlit run app.py </code>

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Use the interface to:
- Index new folders
- Select previously indexed folders
- Perform hybrid searches
- Adjust search parameters

## Configuration

The `config.yaml` file allows you to specify the following:

- `embedding_model`: The Hugging Face model name for document embedding
- `cross_encoder_model`: The Hugging Face model name for the CrossEncoder used in reranking

## Project Structure


hybrid_search_project/\
│\
├── src/\
│ ├── init.py\
│ ├── document_loader.py\
│ ├── index_creator.py\
│ ├── search_engine.py\
│ ├── indexed_folders_manager.py\
│ └── utils.py\
│\
├── app.py\
├── requirements.txt\
└── indexed_folders.json

- `src/`: Contains the core functionality of the search engine
- `app.py`: The main Streamlit application
- `requirements.txt`: List of Python dependencies
- `indexed_folders.json`: Stores information about indexed folders

## How It Works

1. **Document Loading**: The application loads text documents from specified directories.
2. **Indexing**: Documents are processed and indexed using FAISS for vector similarity search.
3. **Hybrid Search**: 
   - Semantic search is performed using cosine similarity on document embeddings.
   - BM25 algorithm is used for keyword-based relevance scoring.
   - Results are combined using an adjustable alpha parameter.
4. **Reranking**: A CrossEncoder model refines the ordering of search results.
5. **Folder Management**: Indexed folders are saved and can be quickly accessed for future searches.
6. **Update Detection**: The system checks for changes in indexed folders and allows for easy updates.

## Contributing

Contributions to improve the Hybrid Semantic Search Engine are welcome. Please feel free to submit pull requests or create issues for bugs and feature requests.
