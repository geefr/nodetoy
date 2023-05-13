from nodetoy.nodes.node import Node
import dearpygui.dearpygui as dpg
from typing import Any, List
import numpy as np
import cv2

class ImageDisplay(Node):
    def __init__(self, name="Image Display"):
        self._name = name

        self._id_in = None
        self._id_texture = None

        img = np.ones((240, 320, 4), np.uint8) * 255
        self._texture = np.divide(img.astype(np.float32), 255.0)

    def setup_dearpygui(self, node_editor, pos, delete_callback):

        with dpg.node(label=self._name, parent=node_editor, pos=pos) as n:
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input) as self._id_in:
                with dpg.texture_registry():
                    self._id_texture = dpg.add_raw_texture(width=320, height=240, default_value=self._texture,
                                                           format=dpg.mvFormat_Float_rgba)
                dpg.add_image(self._id_texture)
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                dpg.add_button(label="X", callback=lambda: delete_callback(self, n))

    def update(self):
        pass

    def input_attribute_ids(self) -> List[int]:
        return [self._id_in]

    def output_attribute_ids(self) -> List[int]:
        return []

    def set_input_attribute_value(self, attrib_id: int, value: Any) -> None:
        if attrib_id == self._id_in and value is not None:
            img = cv2.resize(value, (320, 240))
            num_channels = img.shape[-1] if img.ndim == 3 else 1
            if num_channels == 1:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGRA)
            elif num_channels == 3:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGRA)

            dpg.set_value(self._id_texture, img.astype(np.float32))

    def get_output_attribute_value(self, attrib_id: int) -> Any:
        return None
