import numpy as np


def cosine_similarity(a, b):
    """
    Calculate the cosine similarity between two vectors.

    This function computes the cosine similarity, which is a measure of the 
    cosine of the angle between two non-zero vectors in an inner product space. 
    This metric is a judgment of orientation and not magnitude.

    Parameters:
    a (array_like): The first input vector. Must be a 1D array-like structure (list, numpy array, etc.).
    b (array_like): The second input vector, similar to the first.

    Returns:
    float: Cosine similarity between the two vectors. The value ranges from -1 (exactly opposite) 
    to 1 (exactly the same), with 0 indicating orthogonality (decorrelation).

    Raises:
    ValueError: If any of the input vectors is zero-length or if the dimensions of the vectors do not match.

    Example:
    >>> a = np.array([1, 2, 3])
    >>> b = np.array([4, 5, 6])
    >>> cosine_similarity(a, b)
    0.9746318461970762

    Note:
    This function requires NumPy to be installed and imported as `np`.

    """
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        raise ValueError("One of the input vectors is zero-length.")
    if a.shape != b.shape:
        raise ValueError("Dimensions of the input vectors do not match.")

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
