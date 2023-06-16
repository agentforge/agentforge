import os
import json
from typing import Any, Dict
from dotenv import load_dotenv
from agentforge.interfaces.interface_factory import InterfaceFactory


def read_json_files_from_directory(directory: str) -> Dict[str, Any]:
    json_files = [file for file in os.listdir(directory) if file.endswith('.json')]
    json_contents = []
    
    for json_file in json_files:
        with open(os.path.join(directory, json_file), 'r') as file:
            json_contents.append(json.load(file))
            
    return json_contents


# Load .env file
load_dotenv()

# Get the directory path from the .env file
directory_path = os.environ.get("COLLECTOR_DIRECTORY")

# Read JSON files from directory
json_contents = read_json_files_from_directory(directory_path)

# Initialize the VectorStore
interface_interactor = InterfaceFactory()
vector_store = interface_interactor.create_vectorstore()

# Add texts and metadata from each JSON file to the VectorStore
for content in json_contents:
    texts = [content['pageContent']]
    metadata = {key: value for key, value in content.items() if key != 'pageContent'}
    vector_store.add_texts(texts, [metadata])
