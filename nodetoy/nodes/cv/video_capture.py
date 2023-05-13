from nodetoy.nodes.node import Node
import dearpygui.dearpygui as dpg
from typing import Any, List
import cv2
import numpy as np
from pathlib import Path
import time


class VideoCaptureSource(Node):
    def __init__(self, name="Video Capture"):
        self._name = name
        self._width = 150

        self._id_output = None

        self._id_source_path = None
        self._source_path = None
        self._cap = None
        self._frame = None
        self._fps = 30.0
        self._last_frame_read = time.time()
        self._is_camera = False

    def setup_dearpygui(self, node_editor, pos, delete_callback):
        with dpg.node(label=self._name, parent=node_editor, pos=pos) as n:
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                self._id_source_path = dpg.add_input_text(width=240)
                dpg.add_button(label="Start", callback=lambda: self._open_source(dpg.get_value(self._id_source_path)))

            with dpg.node_attribute(label="frame", attribute_type=dpg.mvNode_Attr_Output) as self._id_output:
                pass

            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                dpg.add_button(label="X", callback=lambda: delete_callback(self, n))

    def _open_source(self, path):
        if not path:
            return

        self._is_camera = False

        if path[0] == '"':
            path = path[1:]
        if path[-1] == '"':
            path = path[:-1]
        self._source_path = str(Path(path))
        self._cap = cv2.VideoCapture(self._source_path)
        if not self._cap.isOpened():
            try:
                cam_index = int(path)
                self._cap = cv2.VideoCapture(cam_index)
                self._is_camera = True
            except ValueError:
                pass

        if not self._cap.isOpened():
            self._cap = None
        else:
            self._fps = self._cap.get(cv2.CAP_PROP_FPS)

    def update(self):
        if self._cap is None:
            return

        if not self._is_camera:
            now = time.time()
            if now < (self._last_frame_read + (1.0 / self._fps)):
                return
            self._last_frame_read = now

        ret, frame = self._cap.read()
        if not ret or frame is None:
            self._cap.set(cv2.CAP_PROP_POS_MSEC, 0)
            return

        self._frame = np.divide(frame.astype(np.float32), 255.0)

    def input_attribute_ids(self) -> List[int]:
        return []

    def output_attribute_ids(self) -> List[int]:
        return [self._id_output]

    def set_input_attribute_value(self, attrib_id: int, value: Any) -> None:
        pass

    def get_output_attribute_value(self, attrib_id: int) -> Any:
        if attrib_id == self._id_output:
            return self._frame
