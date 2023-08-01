import os
import json
import shutil
from typing import Any, Dict
from dotenv import load_dotenv
from agentforge.interfaces.interface_factory import InterfaceFactory


def read_json_files_from_directory(directory: str) -> Dict[str, Any]:
    json_files = [file for file in os.listdir(directory) if file.endswith('.json')]
    json_contents = []
    
    for json_file in json_files:
        with open(os.path.join(directory, json_file), 'r') as file:
            json_contents.append(json.load(file))
            
        # Move the processed file to the 'processed' folder
        processed_directory = os.path.join(directory, '../processed')
        if not os.path.exists(processed_directory):
            os.makedirs(processed_directory)
        shutil.move(os.path.join(directory, json_file), os.path.join(processed_directory, json_file))
            
    return json_contents

# Load .env file
load_dotenv()

# Get the directory path from the .env file
directory_path = os.environ.get("COLLECTOR_DIRECTORY")
milvus_collection = os.environ.get("MILVUS_COLLECTION")

# Read JSON files from directory
json_contents = read_json_files_from_directory(directory_path)

# Initialize the VectorStore
interface_interactor = InterfaceFactory()
interface_interactor.create_vectorstore()
vector_store = interface_interactor.get_interface("vectorstore")

# Add texts and metadata from each JSON file to the VectorStore
for content in json_contents:
    texts = [content['pageContent']]
    metadata = {key: value for key, value in content.items() if key != 'pageContent'}
    vector_store.add_texts(texts, [metadata], collection=milvus_collection)
