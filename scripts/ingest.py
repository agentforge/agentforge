import argparse
import json
import os
# import shutil  # Uncomment if you want to use the moving files functionality
from typing import Any, Dict
# from dotenv import load_dotenv  # Not needed if not using .env files anymore
from agentforge.interfaces.interface_factory import InterfaceFactory

def read_json_files_from_directory(directory: str) -> Dict[str, Any]:
    json_files = [file for file in os.listdir(directory) if file.endswith('.json')]
    json_contents = []

    for json_file in json_files:
        with open(os.path.join(directory, json_file), 'r') as file:
            print(f"Loading {file}")
            json_contents.append(json.load(file))
            
        # Move the processed file to the 'processed' folder
        # Uncomment the lines below if you want to move the processed files to a 'processed' directory
        # processed_directory = os.path.join(directory, 'processed')
        # if not os.path.exists(processed_directory):
        #     os.makedirs(processed_directory)
        # shutil.move(os.path.join(directory, json_file), os.path.join(processed_directory, json_file))

    return json_contents

# Set up the argument parser
parser = argparse.ArgumentParser(description='Process some files.')
parser.add_argument('directory', type=str, help='The directory with JSON files to process')
parser.add_argument('--milvus_collection', type=str, help='Milvus collection name', required=False)

# Parse arguments
args = parser.parse_args()
directory_path = args.directory
milvus_collection = args.milvus_collection or os.environ.get("MILVUS_COLLECTION")

# Read JSON files from directory
json_contents = read_json_files_from_directory(directory_path)

# Initialize the VectorStore
interface_interactor = InterfaceFactory()
interface_interactor.create_vectorstore()
vector_store = interface_interactor.get_interface("vectorstore")

# Add texts and metadata from each JSON file to the VectorStore
total_texts = []
total_meta = []
for content in json_contents:
    total_texts.append(content['pageContent'])
    total_meta.append({key: value for key, value in content.items() if key != 'pageContent'})
vector_store.add_texts(total_texts, total_meta, collection=milvus_collection)
