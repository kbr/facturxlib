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
        if hasattr(self, "_tag_name"):
            tag = self._tag_name
        else:
            tag = self.__class__.__name__
        if namespace:
            tag = f"{namespace}:{tag}"
        return ET.SubElement(parent, tag)

    def render(self, parent):
        # if the instance has the flag _do_render and this flag is False,
        # then skip this node.
        if not getattr(self, "_do_render", True):
            return
        node = self.get_node(parent)
        if hasattr(self, "_node_attributes"):
            for key, value in self._node_attributes.items():
                node.set(key, value)
        if hasattr(self, "_value"):
            node.text = self._value
        # for all attributes: try to render them
        for tag in self.__dict__.values():
            try:
                tag.render(node)
            except AttributeError:
                # nothing to render, just skip
                pass
        # chance to do some additonal stuff
        self._render(node)

    def _render(self, node):
        """
        Specific render-fallback. Overload this method in case of need.
        """
        pass

    def wrapper(cls):
        cls.get_node = get_node
        if not hasattr(cls, "render"):
            cls.render = render
            if not hasattr(cls, "_render"):
                cls._render = _render
        return cls

    return wrapper


class ValueClass:
    """
    Base class for a class with a single self._value-attribute.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)  # in case of (multiple-)inheritance
        self._value = value


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
class DateTimeString(ValueClass):
    """Represents a DateString formatted as 'CCYYMMDD'."""

    _node_attributes = {"format": "102"}  # fixed code for CCYYMMDD


@cii_node("udt")
class OccurenceDateTime:
    """Contractual due date of the invoice"""

    def __init__(self, value):
        self._sub_element = DateTimeString(value)


@cii_node("qdt")
class TypeCode(ValueClass):
    """Represents a CodeType."""


@cii_node("udt")
class ID:
    """Represents an udt:IDType"""

    def __init__(self, value, scheme_id=None):
        self._value = value
        if scheme_id is not None:
            self._node_attributes = {"schemeID": scheme_id}


@cii_node("udt")
class LineID(ValueClass):
    """Line number"""


@cii_node("udt")
class ContentCode(ValueClass):
    """Free text on header level (qualifying the content)"""


@cii_node("udt")
class Content(ValueClass):
    """Freetext on document level (Content)"""


@cii_node("udt")
class SubjectCode(ValueClass):
    """Code for qualifying the free text for the invoice"""


class BaseTotalAmount:
    """Base class for rendering an amount with a currency-id."""

    def __init__(self, value, currency_id=None):
        """the currency_id is an optional token."""
        self._value = value
        if currency_id:
            self._node_attributes = {"currencyID": currency_id}


@cii_node("udt")
class TaxBasisTotalAmount(BaseTotalAmount):
    """
    The total amount of the invoice without VAT.
    The invoice total amount without VAT is the sum of invoice line net
    amount minus sum of discounts on document level plus sum of
    surcharges on document level.
    """


@cii_node("udt")
class TaxTotalAmount(BaseTotalAmount):
    """
    Invoice total VAT amount.
    Invoice total VAT amount in accounting currency
    """


@cii_node("udt")
class GrandTotalAmount(BaseTotalAmount):
    """
    Invoice total amount with VAT.
    The invoice total amount with VAT is the invoice without VAT plus
    the invoice total VAT amount.
    """


@cii_node("udt")
class BasisAmount(ValueClass):
    """taxable amount (aka net price)."""


@cii_node("udt")
class CalculatedAmount(ValueClass):
    """Calculated tax related amount."""


@cii_node("qdt")
class CategoryCode(ValueClass):
    """Coded indication of a sales tax category."""


@cii_node("udt")
class RateApplicablePercent(ValueClass):
    """Percent Value like 19.00 for 19%"""


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


@cii_node("ram")
class ActualDeliverySupplyChainEvent:
    """
    Detailed information about the actual delivery

    `occurence_date`: In Germany, the actual delivery date is mandatory.
                      Format CCYYMMDD

    """

    def __init__(self, occurence_date):
        self._sub_element = OccurenceDateTime(occurence_date)


@cii_node("udt")
class Name(ValueClass):
    """The full formal name of an entity."""


@cii_node("udt")
class PostcodeCode(ValueClass):
    """The postcode (zip) of an address."""


@cii_node("udt")
class LineOne(ValueClass):
    """address line one."""


@cii_node("udt")
class LineTwo(ValueClass):
    """address line two."""


@cii_node("udt")
class LineThree(ValueClass):
    """address line three."""


@cii_node("udt")
class CityName(ValueClass):
    """City for the postcode (zip)."""


@cii_node("qdt")
class CountryID(ValueClass):
    """Country code (like "DE")."""


@cii_node("udt")
class CountrySubDivisionName(ValueClass):
    """Country sub division."""


@dataclass
@cii_node("ram")
class PostalTradeAddress:
    """The postal address of a trade party."""

    country_id: CountryID
    postcode: Optional[PostcodeCode] = None
    line_one: Optional[LineOne] = None
    line_two: Optional[LineTwo] = None
    line_three: Optional[LineThree] = None
    city_name: Optional[CityName] = None
    country_sub_division_name: Optional[CountrySubDivisionName] = None

    def render(self, parent):
        node = self.get_node(parent)
        # same as in self.__dict__.values() but in defined order:
        for tag in (
            self.postcode,
            self.line_one,
            self.line_two,
            self.line_three,
            self.city_name,
            self.country_id,
        ):
            if tag and tag._value:
                tag.render(node)

    @classmethod
    def from_pure_postal_address(cls, address):
        return cls(
            country_id=CountryID(address.country_id),
            postcode=PostcodeCode(address.postcode),
            line_one=LineOne(address.line_one),
            line_two=LineTwo(address.line_two),
            line_three=LineThree(address.line_three),
            city_name=CityName(address.city_name),
            country_sub_division_name=CountrySubDivisionName(address.country_sub_division_name),
        )


@cii_node("ram")
class SpecifiedTaxRegistration:
    """Detailed tax information (like VAT)"""

    def __init__(self, value, scheme_id=None):
        self._do_render = bool(value)
        self._sub_element = ID(value, scheme_id)


@dataclass
class BaseTradeParty:
    """
    Base implementation for all TradePartys
    Subclasses must apply the @cii_node decorator to make the
    `render`-method of this super-class work.
    """

    name: Name
    postal_address: PostalTradeAddress
    specified_tax_registration: Optional[SpecifiedTaxRegistration] = None
