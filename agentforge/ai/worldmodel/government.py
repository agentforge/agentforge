import numpy as np
import json, os

data_dir = os.environ.get("WORLDGEN_DATA_DIR", "./")
government_types = json.load(open(data_dir + "government_types.json"))

# Function to calculate the similarity score between actual dimensions and expected dimensions for each governance type
def calculate_similarity(gov_type, actual_dimensions):
    similarity_score = 0
    for dimension, value in actual_dimensions.items():
        expected_value = gov_type.get(dimension, 0)  # Default to 0 if dimension not found
        similarity_score += (1 - abs(expected_value - value))  # Higher score for closer match
    return similarity_score

# Function to determine governance type based on dimensions
def determine_governance_type(dimensions, era):
    scores = {}
    for gov_type, properties in government_types.items():
        if era not in properties['category']:
            continue
        score = calculate_similarity(properties['prob'], dimensions)
        scores[gov_type] = score
    return np.random.choice(list(scores.keys()), p=[score/sum(scores.values()) for score in scores.values()])
