# TODO: Implement generic filestore
from typing import Protocol, Any

class FileStoreProtocol(Protocol):
    def get_file(self, filepath: str) -> Any:
        pass

    def save_file(self, filepath: str, content: Any) -> None:
        pass
