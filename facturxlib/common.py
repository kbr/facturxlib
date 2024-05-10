"""
common tags and datastructures.
"""

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Optional


def cii_node(namespace=None):
    """
    Convenience class decorator to get the node of a class-instance
    and automate some rendering.
    """

    def get_node(self, parent):
        tag = self.__class__.__name__
        if namespace:
            tag = f"{namespace}:{tag}"
        return ET.SubElement(parent, tag)

    def render(self, parent):
        node = self.get_node(parent)
        if hasattr(self, "_node_attributes"):
            for key, value in self._node_attributes.items():
                node.set(key, value)
        if hasattr(self, "_value"):
            node.text = self._value
        elif hasattr(self, "_sub_element"):
            self._sub_element.render(node)
        else:
            # fallback for something else
            self._render(node)

    def _render(self, node):
        """
        Specific render-fallback. Overload this method in case of need.
        """
        print(f"render: {self.__class__.__name__}")

    def wrapper(cls):
        cls.get_node = get_node
        if not hasattr(cls, "render"):
            cls.render = render
            if not hasattr(cls, "_render"):
                cls._render = _render
        return cls

    return wrapper


class BaseIndicator:
    """Represents an Indicator tag (xs:boolean)."""

    def __init__(self, value: str):  # value = "true" | "false"
        self.value = value

    def render(self, parent):
        node = ET.SubElement(parent, "Indicator")
        node.text = self.value


@cii_node("udt")
class TestIndicator(BaseIndicator):
    """Represents an Indicator."""

    def render(self, parent):
        node = self.get_node(parent)
        super().render(node)


@cii_node("udt")
class CopyIndicator(BaseIndicator):
    """Represents an Indicator."""

    def render(self, parent):
        node = self.get_node(parent)
        super().render(node)


@cii_node()
class DateTimeString:
    """Represents a DateString formatted as 'CCYYMMDD'."""

    _node_attributes = {"format": "102"}  # code for CCYYMMDD

    def __init__(self, value):
        self._value = value


@cii_node("qdt")
class TypeCode:
    """Represents a CodeType."""

    def __init__(self, value):
        self._value = value


@cii_node("udt")
class ID:
    """Represents an udt:IDType"""

    def __init__(self, value):
        self._value = value


@cii_node("udt")
class ContentCode:
    """Free text on header level (qualifying the content)"""

    def __init__(self, value):
        self._value = value


@cii_node("udt")
class Content:
    """Freetext on document level (Content)"""

    def __init__(self, value):
        self._value = value


@cii_node("udt")
class SubjectCode:
    """Code for qualifying the free text for the invoice"""

    def __init__(self, value):
        self._value = value


@dataclass
@cii_node("ram")
class IncludedNote:
    """
    Free text on header level.
    An aggregation of business terms to disclose free text which is
    invoice-relevant, as well as their qualification.

    `content`: required, supported by BASIC
    `subject_code`: optional, supported by BASIC
    `content_code`: optional, supported by EXTENDED
    """

    content: str
    subject_code: Optional[str] = None
    content_code: Optional[str] = None

    def render(self, parent):
        node = self.get_node(parent)
        for item, obj in zip((self.content_code, self.content, self.subject_code), (ContentCode, Content, SubjectCode)):
            if item is not None:
                obj(item).render(node)
