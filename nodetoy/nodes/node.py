from abc import ABC, abstractmethod
from typing import List, Any

class Node(ABC):
    @abstractmethod
    def setup_dearpygui(self, node_editor, pos, delete_callback):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def input_attribute_ids(self) -> List[int]:
        pass

    @abstractmethod
    def output_attribute_ids(self) -> List[int]:
        pass

    @abstractmethod
    def set_input_attribute_value(self, attrib_id: int, value: Any) -> None:
        pass

    @abstractmethod
    def get_output_attribute_value(self, attrib_id: int) -> Any:
        pass
