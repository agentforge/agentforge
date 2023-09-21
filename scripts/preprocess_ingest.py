from typing import Dict, List
import re
import unicodedata
import json
import os
from dotenv import load_dotenv
import string
import uuid

def create_json_files(file_path: str, directory: str):
    # Load data from the file
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Iterate over the data and create json files
    for obj in data:
        # generate a unique file name using uuid
        uuid_str = str(uuid.uuid4())
        file_name = f"terpene-desc-{uuid_str}.json"
        file_path = os.path.join(directory, file_name)

        # write the data to the file
        with open(file_path, 'w') as f:
            obj["pageContent"] = "This is the description of a cannabis terpene. " + obj["pageContent"]
            obj["id"] = uuid_str
            json.dump(obj, f)

def unicode_to_ascii(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
        and c in string.ascii_letters + string.digits + string.punctuation + string.whitespace)

def fix_content(content: str) -> str:
    ## replace "’" with "'" and "–" with "-"
    content = content.replace("’", "'").replace("–", "-")
    
    ## translate unicode to ascii if possible
    content = unicode_to_ascii(content)
    
    ## remove non-ascii characters
    content = re.sub(r'[^\x00-\x7F]+',' ', content)
    
    ## for latex/academic characters sometimes newlines are used to break words
    content = re.sub(r'\-\n', '', content)
    
    ## convert newlines to spaces
    content = content.replace('\n', ' ')
    
    ## remove emojis
    content = re.sub(r'[\U00010000-\U0010ffff]', '', content, flags=re.UNICODE)
    
    ## remove urls
    content = re.sub(r'http\S+|www.\S+', '', content, flags=re.MULTILINE)
    
    ## remove file-like objects
    content = re.sub(r'file:///\S+', '', content)
    
    ## remove hashtags
    content = re.sub(r'\#\S+', '', content)
    
    ## remove mentions
    content = re.sub(r'\@\S+', '', content)
    
    ## remove citations, assuming citations are inside brackets
    content = re.sub(r'\[.*?\]', '', content)
    
    ## remove underscores of length 2 or greater
    content = re.sub(r'_{2,}', '', content)
    
    ## remove any strings within brackets
    content = re.sub(r'\(.*?\)', '', content)
    
    ## convert \" to '
    content = content.replace('\"', "'")
    
    ## remove 2 or more spaces and replace them with a single space
    content = re.sub(r' {2,}', ' ', content)
    
    ## replace " ." with "." and " ," with ","
    content = content.replace(" .", ".").replace(" ,", ",")
    
    ## remove "FIGURE X.X" like strings
    content = re.sub(r'FIGURE \d+\.\d+', '', content, flags=re.IGNORECASE)
    
    ## remove date/time stamps
    content = re.sub(r'\d{1,2}/\d{1,2}/\d{2,4} \d{1,2}:\d{2}:\d{2} (AM|PM)', '', content, flags=re.IGNORECASE)
    
    ## remove 2 or more spaces and replace them with a single space again after removing date/time stamps
    content = re.sub(r' {2,}', ' ', content)
    
    return content

# Function to process a directory of JSON files
def process_directory(directory: str):
    # Loop over all files in the directory
    for filename in os.listdir(directory):
        # Only process JSON files
        if filename.endswith('.json'):
            # Construct the full file path
            filepath = os.path.join(directory, filename)
            
            # Open the file and load the JSON data
            with open(filepath, 'r') as file:
                data = json.load(file)
            
            # Apply the fix_content function to the pageContent field
            data['pageContent'] = fix_content(data['pageContent'])
            
            # Write the processed data back to the file
            with open(filepath, 'w') as file:
                json.dump(data, file)

# Test strings
test_strings = ["\"Now, if there were any deleterious properties\" (22%, 44%, 26%, 4%, 1%)",
                "This is a test string with __ underscores and ___ more underscores.",
                "The enhancement of morphine antinoci-\nception in mice by delta9-tetrahydrocannabinol."]

# Load .env file
load_dotenv()

# Get the directory path from the .env file
# directory_path = os.environ.get("COLLECTOR_DIRECTORY")

directory_path = "/app/cache/vectorstore_data/tmp"
terps_path = "/app/cache/vectorstore_data/terpenes.json"

# process_directory(directory_path)
create_json_files(terps_path, "/app/cache/vectorstore_data/terpenes")
