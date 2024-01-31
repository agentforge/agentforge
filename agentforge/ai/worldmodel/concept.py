import pandas as pd

class Concept:
    def __init__(self, name, category, metadata=None):
        self.name = name
        self.category = category
        self.connections = []
        self.metadata = metadata if metadata is not None else {}

    def add_connection(self, concept_name, probability):
        self.connections.append({'concept': concept_name, 'probability': probability})

    def remove_connection(self, concept_name):
        self.connections = [c for c in self.connections if c['concept'] != concept_name]

    def get_connections(self):
        return self.connections

    def update_metadata(self, key, value):
        """
        Update the metadata of the concept.
        :param key: The key in the metadata dictionary.
        :param value: The value to be added/updated.
        """
        self.metadata[key] = value

    def __repr__(self):
        return f"Concept(name={self.name}, category={self.category}, connections={self.connections}, metadata={self.metadata})"
    

def ensure_non_negative_and_normalize_row(row):
    """
    Ensure that all values in the DataFrame row are non-negative and normalize the row.

    :param row: A row from a pandas DataFrame.
    :return: A row with non-negative values that sum to 1.
    """
    # Set negative values to zero
    row[row < 0] = 0

    # Normalize the row to sum to 1
    row_sum = row.sum()
    if row_sum > 0:
        row = row / row_sum
    else:
        # If the sum is zero, assign equal probabilities
        row = pd.Series(1.0 / len(row), index=row.index)
    
    return row

def normalize_rows(matrix_df):
    """
    Normalize the rows of a DataFrame so that each row sums to 1.

    :param matrix_df: The DataFrame to normalize.
    :return: The normalized DataFrame.
    """
    matrix_np = matrix_df.to_numpy()  # Convert to numpy array for multi-dimensional indexing
    row_sums = matrix_np.sum(axis=1, keepdims=True)
    # Avoid division by zero
    row_sums[row_sums == 0] = 1
    return pd.DataFrame(matrix_np / row_sums, index=matrix_df.index, columns=matrix_df.columns)
