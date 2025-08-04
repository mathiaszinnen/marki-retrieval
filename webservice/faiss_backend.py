import faiss
import numpy as np
import torch
from typing import List


def load_faiss_index(index_path: str, filenames_path: str):
    """
    Load a FAISS index and corresponding filenames list.

    Parameters:
        index_path (str): Path to the FAISS index file (.index).
        filenames_path (str): Path to the NumPy file (.npy) containing filenames.

    Returns:
        tuple: (faiss.IndexFlatL2, np.ndarray[str])
    """
    index = faiss.read_index(index_path)
    filenames = np.load(filenames_path)
    return index, filenames


def query_index(index, filenames: np.ndarray, query_vector: np.ndarray, top_k: int = 5) -> List[str]:
    """
    Query the FAISS index for the top-k most similar items.

    Parameters:
        index (faiss.Index): Loaded FAISS index.
        filenames (np.ndarray): Array of filenames corresponding to the indexed vectors.
        query_vector (np.ndarray): A (D,) or (1, D) float32 vector.
        top_k (int): Number of similar results to return.

    Returns:
        List[str]: Filenames of the top-k most similar images.
    """
    if query_vector.ndim == 1:
        query_vector = query_vector[None, :]  # Convert to shape (1, D)

    query_vector = query_vector.to(torch.float32)
    distances, indices = index.search(query_vector, top_k)
    return [filenames[i] for i in indices[0]]
