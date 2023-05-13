from nodetoy.nodes.node import Node
import dearpygui.dearpygui as dpg
from typing import Any, List
import sys

class ValueSourceFloat(Node):
    def __init__(self, name="Float"):
        self._name = name
        self._width = 150

        self._id_input = None
        self._id_output = None
        self._value = None

    def setup_dearpygui(self, node_editor, pos, delete_callback):
        with dpg.node(label=self._name, parent=node_editor, pos=pos) as n:
            with dpg.node_attribute(label="Value", attribute_type=dpg.mvNode_Attr_Output) as self._id_output:
                self._id_input = dpg.add_input_float(width=self._width, min_value=-sys.float_info.max, max_value=sys.float_info.max)
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                dpg.add_button(label="X", callback=lambda: delete_callback(self, n))

    def update(self):
        self._value = dpg.get_value(self._id_input)

    def input_attribute_ids(self) -> List[int]:
        return []

    def output_attribute_ids(self) -> List[int]:
        return [self._id_output]

    def set_input_attribute_value(self, attrib_id: int, value: Any) -> None:
        pass

    def get_output_attribute_value(self, attrib_id: int) -> Any:
        if attrib_id == self._id_output:
            return self._value

class ValueSourceInt(Node):
    def __init__(self, name="Int"):
        self._name = name
        self._width = 150

        self._id_input = None
        self._id_output = None
        self._value = None

    def setup_dearpygui(self, node_editor, pos, delete_callback):
        with dpg.node(label=self._name, parent=node_editor, pos=pos) as n:
            with dpg.node_attribute(label="Value", attribute_type=dpg.mvNode_Attr_Output) as self._id_output:
                self._id_input = dpg.add_input_int(width=self._width, min_value=-(sys.maxsize - 1), max_value=sys.maxsize)
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                dpg.add_button(label="X", callback=lambda: delete_callback(self, n))

    def update(self):
        self._value = dpg.get_value(self._id_input)

    def input_attribute_ids(self) -> List[int]:
        return []

    def output_attribute_ids(self) -> List[int]:
        return [self._id_output]

    def set_input_attribute_value(self, attrib_id: int, value: Any) -> None:
        pass

    def get_output_attribute_value(self, attrib_id: int) -> Any:
        if attrib_id == self._id_output:
            return self._value
