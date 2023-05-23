import os
from typing import Any
from agentforge.adapters import FileStoreProtocol

class LocalFileStore(FileStoreProtocol):
    def __init__(self, base_directory: str) -> None:
        self.base_directory = base_directory

    def get_file(self, filepath: str) -> Any:
        with open(os.path.join(self.base_directory, filepath), 'r') as file:
            content = file.read()
        return content

    def save_file(self, filepath: str, content: Any) -> None:
        with open(os.path.join(self.base_directory, filepath), 'w') as file:
            file.write(content)
