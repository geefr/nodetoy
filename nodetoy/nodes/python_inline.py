from nodetoy.nodes.node import Node
import dearpygui.dearpygui as dpg
from typing import Any, List


class PythonEval(Node):

    def __init__(self, name="Eval"):
        self._name = name

        self._id_a = None
        self._id_b = None
        self._id_c = None
        self._id_d = None
        self._id_out = None
        self._id_out_eq = None
        self._id_out_err = None

        self._a = None
        self._b = None
        self._c = None
        self._d = None
        self._out = None

    def setup_dearpygui(self, node_editor, pos, delete_callback):
        with dpg.node(label=self._name, parent=node_editor, pos=pos) as n:
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input) as self._id_a:
                dpg.add_text(default_value="a")
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input) as self._id_b:
                dpg.add_text(default_value="b")
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output) as self._id_out:
                pass
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input) as self._id_c:
                dpg.add_text(default_value="c")
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input) as self._id_d:
                dpg.add_text(default_value="d")
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                self._id_out_eq = dpg.add_input_text(width=320, multiline=False, default_value=1)
                self._id_out_err = dpg.add_text()
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                dpg.add_button(label="X", callback=lambda: delete_callback(self, n))

    def update(self):
        eq = str(dpg.get_value(self._id_out_eq))

        try:
            self._out = eval(eq, {}, {
                "a": self._a,
                "b": self._b,
                "c": self._c,
                "d": self._d,
            })
            dpg.set_value(self._id_out_err, "")
        except Exception as e:
            dpg.set_value(self._id_out_err, str(e))

    def input_attribute_ids(self) -> List[int]:
        return [self._id_a, self._id_b, self._id_c, self._id_d]

    def output_attribute_ids(self) -> List[int]:
        return [self._id_out]

    def set_input_attribute_value(self, attrib_id: int, value: Any) -> None:
        if attrib_id == self._id_a:
            self._a = value
        if attrib_id == self._id_b:
            self._b = value
        if attrib_id == self._id_c:
            self._c = value
        if attrib_id == self._id_d:
            self._d = value

    def get_output_attribute_value(self, attrib_id: int) -> Any:
        if attrib_id == self._id_out:
            return self._out


class PythonExec(Node):

    def __init__(self, name="Exec"):
        self._name = name

        self._id_a = None
        self._id_b = None
        self._id_c = None
        self._id_d = None
        self._id_out = None
        self._id_out_eq = None
        self._id_out_err = None

        self._a = None
        self._b = None
        self._c = None
        self._d = None
        self._out = None

    def setup_dearpygui(self, node_editor, pos, delete_callback):
        with dpg.node(label=self._name, parent=node_editor, pos=pos) as n:
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input) as self._id_a:
                dpg.add_text(default_value="a")
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input) as self._id_b:
                dpg.add_text(default_value="b")
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output) as self._id_out:
                # dpg.add_text(default_value="out")
                pass
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input) as self._id_c:
                dpg.add_text(default_value="c")
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input) as self._id_d:
                dpg.add_text(default_value="d")
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                self._id_out_eq = dpg.add_input_text(width=320, height=240, multiline=True, default_value="out = 1")
                self._id_out_err = dpg.add_text()
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                dpg.add_button(label="X", callback=lambda: delete_callback(self, n))

    def update(self):
        eq = str(dpg.get_value(self._id_out_eq))

        try:
            out = None
            loc = {
                "a": self._a,
                "b": self._b,
                "c": self._c,
                "d": self._d,
                "out": out,
            }
            exec(eq, {}, loc)
            dpg.set_value(self._id_out_err, "")
            self._out = loc["out"]
        except Exception as e:
            dpg.set_value(self._id_out_err, str(e))

    def input_attribute_ids(self) -> List[int]:
        return [self._id_a, self._id_b, self._id_c, self._id_d]

    def output_attribute_ids(self) -> List[int]:
        return [self._id_out]

    def set_input_attribute_value(self, attrib_id: int, value: Any) -> None:
        if attrib_id == self._id_a:
            self._a = value
        if attrib_id == self._id_b:
            self._b = value
        if attrib_id == self._id_c:
            self._c = value
        if attrib_id == self._id_d:
            self._d = value

    def get_output_attribute_value(self, attrib_id: int) -> Any:
        if attrib_id == self._id_out:
            return self._out
