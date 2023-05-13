import dearpygui.dearpygui as dpg

from nodes.value_sources import *
from nodes.arithmetic import Arithmetic
from nodes.value_display import *
from typing import List, Optional

id_main_window = "##main_window"
id_node_editor = "##node_editor"
id_right_click = "##right_click_menu"

dpg.create_context()

nodes = [
    # ValueSourceFloat("Input 1"),
    # ValueSourceFloat("Input 2"),
    # Arithmetic("Add", Arithmetic.ADD),
    # Arithmetic("Sub", Arithmetic.SUBTRACT),
    # Arithmetic("Div", Arithmetic.DIVIDE),
    # Arithmetic("Mul", Arithmetic.MULTIPLY),
    # ValueDisplay(),
]
links = dict()


def _find_node_with_output_attribute_id(nodes: List[Node], attrib_id: int) -> Optional[Node]:
    for node in nodes:
        attribs = node.output_attribute_ids()
        if attrib_id in attribs:
            return node
    return None


def _find_node_with_input_attribute_id(nodes: List[Node], attrib_id: int) -> Optional[Node]:
    for node in nodes:
        attribs = node.input_attribute_ids()
        if attrib_id in attribs:
            return node
    return None


# callback runs when user attempts to connect attributes
def link_callback(sender, app_data):
    # app_data -> (link_id1, link_id2)
    # link_id is the 'id' attribute of dpg.node_attribute
    # (Despite that attribute being marked as deprecated in favour of tag
    #  - This code doesn't use tags to avoid the weirdness..)

    for link in links.values():
        if link[1] == app_data[1]:
            # Something is already linked to this input - Not allowed
            return

    link_id = dpg.add_node_link(app_data[0], app_data[1], parent=sender)
    links[link_id] = app_data


# callback runs when user attempts to disconnect attributes
def delink_callback(sender, app_data):
    # app_data -> link_id
    print(f"UNLINK: {app_data}")
    dpg.delete_item(app_data)
    del links[app_data]


def on_button_spawn_node(created_node, nodes, node_editor):
    pos = dpg.get_mouse_pos(local=False)
    created_node.setup_dearpygui(node_editor, pos, on_delete_node)
    nodes.append(created_node)
    dpg.configure_item(id_right_click, show=False)


def on_delete_node(node_to_delete: Node, dpg_id: int):
    node_inputs = node_to_delete.input_attribute_ids()
    node_outputs = node_to_delete.output_attribute_ids()
    link_ids_to_delete = set()
    for k, v in links.items():
        if v[0] in node_outputs or v[1] in node_inputs:
            link_ids_to_delete.add(k)

    for link_id in link_ids_to_delete:
        dpg.delete_item(link_id)
        del links[link_id]

    dpg.delete_item(dpg_id)
    nodes.remove(node_to_delete)


def setup_dearpygui(nodes: List[Node]) -> None:
    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()

    with dpg.window(tag=id_main_window, width=viewport_width, height=viewport_height, no_title_bar=True,
                    no_resize=True):
        with dpg.node_editor(tag=id_node_editor, callback=link_callback, delink_callback=delink_callback) as n:
            for node in nodes:
                node.setup_dearpygui(n, (0, 0), on_delete_node)

        def right_click_cb(sender, app_data):
            mouse_pos = dpg.get_mouse_pos(local=False)
            dpg.configure_item(id_right_click, show=True, pos=mouse_pos)

        def left_click_cb(sender, app_data):
            dpg.configure_item(id_right_click, show=False)

        with dpg.handler_registry():
            dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Right, callback=right_click_cb)
            # TODO: Nice to be able to hide the window by clicking background, but it breaks the menu buttons
            # dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Left, callback=left_click_cb)

        with dpg.window(label="Right click window", modal=True, show=False, id=id_right_click, no_title_bar=True):
            dpg.add_button(label="Close", callback=lambda: dpg.configure_item(id_right_click, show=False))
            dpg.add_separator()
            dpg.add_button(label="Float", callback=lambda: on_button_spawn_node(ValueSourceFloat("Float"), nodes, n))
            dpg.add_separator()
            dpg.add_button(label="Add",
                           callback=lambda: on_button_spawn_node(Arithmetic("Add", Arithmetic.ADD), nodes, n))
            dpg.add_button(label="Subtract",
                           callback=lambda: on_button_spawn_node(Arithmetic("Sub", Arithmetic.SUBTRACT), nodes, n))
            dpg.add_button(label="Divide",
                           callback=lambda: on_button_spawn_node(Arithmetic("Div", Arithmetic.DIVIDE), nodes, n))
            dpg.add_button(label="Multiply",
                           callback=lambda: on_button_spawn_node(Arithmetic("Mul", Arithmetic.MULTIPLY), nodes, n))
            dpg.add_separator()
            dpg.add_button(label="Display", callback=lambda: on_button_spawn_node(ValueDisplay(), nodes, n))

    dpg.setup_dearpygui()


def main():
    dpg.create_viewport(title="Node Graph Toy", min_width=800, min_height=600)

    setup_dearpygui(nodes)
    dpg.show_viewport()

    dpg.set_primary_window(id_main_window, True)

    while dpg.is_dearpygui_running():
        # TODO: The nodes here are updated in the order they were created
        #       This is very wrong
        #       It should be a tree / graph
        #       It should always be unidirectional, given how the node links work

        # Propagate data across links
        for link in links.values():
            node_a = _find_node_with_output_attribute_id(nodes, link[0])
            node_b = _find_node_with_input_attribute_id(nodes, link[1])

            if node_a is not None and node_b is not None:
                v = node_a.get_output_attribute_value(link[0])
                node_b.set_input_attribute_value(link[1], v)

        for node in nodes:
            node.update()

        dpg.render_dearpygui_frame()

    dpg.destroy_context()


if __name__ == '__main__':
    main()
