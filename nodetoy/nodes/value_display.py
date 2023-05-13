from nodetoy.nodes.node import Node
import dearpygui.dearpygui as dpg
from typing import Any, List

class ValueDisplay(Node):
    def __init__(self, name="Value Display"):
        self._name = name

        self._id_in = None
        self._id_label = None
        self._value = None

    def setup_dearpygui(self, node_editor, pos, delete_callback):
        with dpg.node(label=self._name, parent=node_editor, pos=pos) as n:
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input) as self._id_in:
                self._id_label = dpg.add_text()
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                dpg.add_button(label="X", callback=lambda: delete_callback(self, n))

    def update(self):
        dpg.set_value(self._id_label, self._value)

    def input_attribute_ids(self) -> List[int]:
        return [self._id_in]

    def output_attribute_ids(self) -> List[int]:
        return []

    def set_input_attribute_value(self, attrib_id: int, value: Any) -> None:
        if attrib_id == self._id_in:
            self._value = value

    def get_output_attribute_value(self, attrib_id: int) -> Any:
        return None
