"""
cross industry incoice:
class decorator for node-rendering.
"""

import xml.etree.ElementTree as ET
from collections.abc import Iterable

DO_NOT_RENDER_ON_EMPTY_VALUE = "_do_not_render_on_empty_value"


def cii_node(namespace=None):
    """
    Class decorator to make classes renderable nodes.
    """

    def get_node(self, parent):
        if hasattr(self, "_tag_name"):
            tag = self._tag_name
        else:
            tag = self.__class__.__name__
        if namespace:
            tag = f"{namespace}:{tag}"
        return ET.SubElement(parent, tag)

    def render(self, parent):
        # skip nodes marked to not get rendered
        if not getattr(self, "_do_render", True):
            return

        # check whether nodes with no value should get rendered
        if getattr(self, DO_NOT_RENDER_ON_EMPTY_VALUE, False):
            if not getattr(self, "_value", False):
                return

        # create the node and add node-attributes and the content, if given:
        node = self.get_node(parent)
        if hasattr(self, "_node_attributes"):
            for key, value in self._node_attributes.items():
                node.set(key, value)
        if hasattr(self, "_value"):
            node.text = self._value

        # check for explicit subnode render-exceptions:
        nodes_to_ignore_if_empty = getattr(self, "_suppress_nodes_with_empty_values", None)
        if nodes_to_ignore_if_empty:
            for entry in nodes_to_ignore_if_empty.split():
                item = getattr(self, entry, None)
                setattr(item, DO_NOT_RENDER_ON_EMPTY_VALUE, True)

        # give render-selection exclusive priority to attributes:
        selection = getattr(self, "_render_selection", None)
        if selection:
            for attribute_name in selection.split():
                if attr := getattr(self, attribute_name, None):
                    _render_object(attr, node)
        else:
            for item in self.__dict__.values():
                _render_object(item, node)
        self._render(node)

    def _render_object(obj, node):
        if isinstance(obj, Iterable):
            for item in obj:
                _try_to_render(item, node)
        else:
            _try_to_render(obj, node)

    def _try_to_render(obj, node):
        try:
            obj.render(node)
        except AttributeError:
            pass

    def _render(self, node):
        """Specific render-fallback. Overload this method in case of need."""
        pass

    def wrapper(cls):
        cls.get_node = get_node
        if not hasattr(cls, "render"):
            cls.render = render
            if not hasattr(cls, "_render"):
                cls._render = _render
        return cls

    return wrapper
