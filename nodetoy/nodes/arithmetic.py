from nodetoy.nodes.node import Node
import dearpygui.dearpygui as dpg
from typing import Any, List


class Arithmetic(Node):
    ADD = 0
    SUBTRACT = 1
    DIVIDE = 2
    MULTIPLY = 3

    def __init__(self, name="Arithmetic", op=ADD):
        self._name = name
        self._op = op

        self._id_a = None
        self._id_a_label = None
        self._id_b = None
        self._id_b_label = None
        self._id_c = None
        self._id_c_label = None

        self._a = None
        self._b = None
        self._c = None

    def setup_dearpygui(self, node_editor, pos, delete_callback):
        with dpg.node(label=self._name, parent=node_editor, pos=pos) as n:
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input) as self._id_a:
                dpg.add_spacer(width=32, height=8)
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output) as self._id_c:
                dpg.add_spacer(width=32, height=8)
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input) as self._id_b:
                dpg.add_spacer(width=32, height=8)
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                dpg.add_button(label="X", callback=lambda: delete_callback(self, n))

    def update(self):
        if self._a is not None and self._b is not None:
            if self._op == Arithmetic.ADD:
                self._c = self._a + self._b
            elif self._op == Arithmetic.SUBTRACT:
                self._c = self._a - self._b
            elif self._op == Arithmetic.DIVIDE:
                self._c = self._a / self._b
            elif self._op == Arithmetic.MULTIPLY:
                self._c = self._a * self._b

    def input_attribute_ids(self) -> List[int]:
        return [self._id_a, self._id_b]

    def output_attribute_ids(self) -> List[int]:
        return [self._id_c]

    def set_input_attribute_value(self, attrib_id: int, value: Any) -> None:
        if attrib_id == self._id_a:
            self._a = value
        if attrib_id == self._id_b:
            self._b = value

    def get_output_attribute_value(self, attrib_id: int) -> Any:
        if attrib_id == self._id_c:
            return self._c
