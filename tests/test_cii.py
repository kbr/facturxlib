import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Optional, Sequence

import pytest


from facturxlib.nodes.common import (
    cii_node,
    ValueClass,
)

ENCLOSURE = "<cii>%s</cii>"


@pytest.fixture
def parent():
    return ET.Element("cii")


def check_result(root, node, expected):
    node.render(root)
    result = ET.tostring(root, encoding="unicode")
    if expected:
        expected = ENCLOSURE % expected
    else:
        expected = "<cii />"
    assert result == expected


@cii_node("ns")
class A:
    pass


def test_render_class_tag(parent):
    node = A()
    expected = "<ns:A />"
    check_result(parent, node, expected)


@cii_node("ns")
class VC(ValueClass):
    pass


def test_render_value(parent):
    node = VC("42")
    expected = "<ns:VC>42</ns:VC>"
    check_result(parent, node, expected)


@cii_node("ns")
class VCn(ValueClass):
    _do_not_render_on_empty_value = True


def test_do_not_render_empty_value(parent):
    node = VCn("")
    expected = ""
    check_result(parent, node, expected)


@cii_node("ns")
class OtherName:
    _tag_name = "TN"


def test_render_other_tag_name(parent):
    node = OtherName()
    expected = "<ns:TN />"
    check_result(parent, node, expected)


@cii_node("ns")
class Invisible:
    _do_render = False


def test_render_invisible(parent):
    node = Invisible()
    expected = ""
    check_result(parent, node, expected)


@cii_node("ns")
class Attributes(ValueClass):
    _node_attributes = {"unitCode": "cm", "format": "metric"}


def test_node_with_attributes(parent):
    node = Attributes("3.141")
    expected = """<ns:Attributes unitCode="cm" format="metric">3.141</ns:Attributes>"""
    check_result(parent, node, expected)


@cii_node("ns")
class B:
    pass


@dataclass
@cii_node("ns")
class Outer:
    a: A
    b: B


def test_render_inner_nodes(parent):
    node = Outer(A(), B())
    expected = "<ns:Outer><ns:A /><ns:B /></ns:Outer>"
    check_result(parent, node, expected)


@cii_node("ns")
class C:
    pass


@dataclass
@cii_node("ns")
class Selective:
    a: A
    b: B
    c: C

    _render_selection = "c a"  # space separated attribute names


def test_render_selected_nodes(parent):
    node = Selective(A(), B(), C())
    expected = "<ns:Selective><ns:C /><ns:A /></ns:Selective>"
    check_result(parent, node, expected)


@dataclass
@cii_node("ns")
class IT:
    a: A
    li: [VC]
    b: B


def test_render_with_iterable(parent):
    node = IT(a=A(), li=[VC("3"), VC("42")], b=B())
    expected = "<ns:IT><ns:A /><ns:VC>3</ns:VC><ns:VC>42</ns:VC><ns:B /></ns:IT>"
    check_result(parent, node, expected)



@dataclass
@cii_node("ns")
class Suppress:
    a: VC
    b: VC

    _suppress_nodes_with_empty_values = "b"

@pytest.mark.parametrize(
    "x, y, expected", [
        ("3", "4", "<ns:Suppress><ns:VC>3</ns:VC><ns:VC>4</ns:VC></ns:Suppress>"),
        ("3", "", "<ns:Suppress><ns:VC>3</ns:VC></ns:Suppress>"),
    ]
)
def test_render_with_suppress_setting(x, y, expected, parent):
    node = Suppress(a=VC(x), b=VC(y))
    check_result(parent, node, expected)



@dataclass
@cii_node("ns")
class Suppress2:
    a: VC
    b: VC
    c: VC

    _render_selection = "b c"
    _suppress_nodes_with_empty_values = "b"

def test_render_with_suppress2_setting(parent):
    node = Suppress2(a=VC("3"), b=VC(""), c=VC("42"))
    expected = "<ns:Suppress2><ns:VC>42</ns:VC></ns:Suppress2>"
    check_result(parent, node, expected)

