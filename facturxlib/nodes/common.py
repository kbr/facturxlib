"""
common tags and datastructures.

Base classes are defined first,
derived classes and nodes (decorated by @cii_node)
are defined in alphabetical order.
Nodes that are also dataclasses are last, because of dependencies from
other nodes.
"""

import xml.etree.ElementTree as ET

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Optional, Sequence


DO_NOT_RENDER_ON_EMPTY_VALUE = "_do_not_render_on_empty_value"


def cii_node(namespace=None):
    """
    Convenience class decorator to get the node of a class-instance
    and automate the rendering.
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
        # then skip this node:
        if not getattr(self, "_do_render", True):
            return

        # optionaly prevent a ValueClass getting rendered if there
        # is no Value. Do this with `getattr` because the attributes
        # may not exist.
        if getattr(self, DO_NOT_RENDER_ON_EMPTY_VALUE, False):
            if not getattr(self, "_value", False):
                return

        # create the node, optional node-attributes and the content:
        node = self.get_node(parent)
        if hasattr(self, "_node_attributes"):
            for key, value in self._node_attributes.items():
                node.set(key, value)
        if hasattr(self, "_value"):
            node.text = self._value

        # check for explicit render exceptions:
        nodes_to_ignore_if_empty = getattr(self, "_suppress_nodes_with_empty_values", None)
        if nodes_to_ignore_if_empty:
            for entry in nodes_to_ignore_if_empty.split():
                item = getattr(self, entry, None)
                setattr(item, DO_NOT_RENDER_ON_EMPTY_VALUE, True)
        # check for selected subnodes:
        selection = getattr(self, "_render_selection", None)
        if selection:
            for attribute_name in selection.split():
                if attr := getattr(self, attribute_name, None):
                    _render_object(attr, node)
        else:
            # for all instance attributes: try to render them
            for item in self.__dict__.values():
                _render_object(item, node)

        # chance to do some additonal stuff
        self._render(node)

    def _render_object(obj, node):
        try:
            obj.render(node)
        except AttributeError:
            # check for iterable and try to delegate:
            if isinstance(obj, Iterable):
                for item in obj:
                    try:
                        item.render(node)
                    except AttributeError:
                        # nothing to render, just skip
                        pass

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

    def __init__(self, value):
        self._value = value


class BaseTotalAmount(ValueClass):
    """Base class for rendering an amount with a currency-id."""

    def __init__(self, value, currency_id=None):
        """the currency_id is an optional token."""
        super().__init__(value)
        if currency_id:
            self._node_attributes = {"currencyID": currency_id}


class QuantityClass(ValueClass):
    """Base class for a Quantity with required Unit Code"""

    def __init__(self, value, unit_code):
        super().__init__(value)
        self._node_attributes = {"unitCode": unit_code}


class SchemeClass(ValueClass):
    """Base class for a value with an optional schemeID token."""

    def __init__(self, value, scheme_id=None):
        super().__init__(value)
        if scheme_id:
            self._node_attributes = {"schemeID": scheme_id}


@cii_node("udt")
class CompleteNumber(ValueClass):
    """
    Contact phone number.
    Used by `UniversalCommunication` and in turn by
    `TelephoneUniversalCommunication` and `FaxUniversalCommunication`.
    """


class UniversalCommunication:
    """
    Details about the contact number.
    The number itself is rendered by a subnode.
    So render this node only when a number is given.
    The Subclass must be decorated by `@cii_node`.
    """

    def __init__(self, number):
        self._do_render = bool(number)
        self._sub_element = CompleteNumber(number)


# ====================================================
# alphabetical definition of nodes


@cii_node("ram")
class ActualDeliverySupplyChainEvent:
    """
    Detailed information about the actual delivery

    `occurence_date`: In Germany, the actual delivery date is mandatory.
                      Format CCYYMMDD

    """

    def __init__(self, occurence_date):
        self._sub_element = OccurrenceDateTime(occurence_date)


@cii_node("udt")
class ActualAmount(ValueClass):
    """
    Actual amount of calculations.
    Node used in multiple places.
    """


@cii_node("udt")
class AllowanceTotalAmount(ValueClass):
    """Total amount of discounts."""


@cii_node("udt")
class AttachmentBinaryObject:
    """
    Attached document.

    `mime_code`: mime-code of the attached file. Permissible MIME-codes are:
        - application/pdf;
        - image/png;
        - image/jpeg;
        - text/csv;
        - application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;
        - application/vnd.oasis.opendocument.spreadsheet;

    `filename`: name of the attached document.
        Often referred as 'embedded' document.
    """

    def __init__(self, mime_code, filename):
        self._node_attributes = {"mimeCode": mime_code, "filename": filename}


@cii_node("udt")
class BasisAmount(ValueClass):
    """base amount (for further calculations)."""


@cii_node("udt")
class BasisQuantity(QuantityClass):
    """Represents an udt:Item Base Quantity with required Unit Code"""


@cii_node("udt")
class BilledQuantity(QuantityClass):
    """Represents an udt:Item Billed Quantity with required Unit Code"""


@cii_node("udt")
class CalculatedAmount(ValueClass):
    """Calculated tax related amount."""


@cii_node("udt")
class CalculationPercent(ValueClass):
    """Discount / Charge in percent"""


@cii_node("qdt")
class CategoryCode(ValueClass):
    """Coded indication of a sales tax category."""


@cii_node("udt")
class ChargeAmount(ValueClass):
    """Item net price."""


@cii_node("udt")
class ChargeIndicator:
    """
    Represents a boolean Indicator.
    Value should be "true" | "false"
    """

    def __init__(self, value):
        self._sub_element = Indicator(value)


@cii_node("udt")
class ChargeTotalAmount(ValueClass):
    """Sum of all surcharges on document level in the invoice."""


@cii_node("udt")
class CityName(ValueClass):
    """City for the postcode (zip)."""


@cii_node("udt")
class Content(ValueClass):
    """Freetext on document level (Content)"""


@cii_node("udt")
class ContentCode(ValueClass):
    """Free text on header level (qualifying the content)"""


@cii_node("udt")
class CopyIndicator:
    """
    Represents a boolean Indicator.
    Value should be "true" | "false"
    """

    def __init__(self, value):
        self._sub_element = Indicator(value)


@cii_node("qdt")
class CountryID(ValueClass):
    """Country code (like "DE")."""


@cii_node("udt")
class CountrySubDivisionName(ValueClass):
    """Country sub division."""


@cii_node()
class DateTimeString(ValueClass):
    """Represents a DateString formatted as 'CCYYMMDD'."""

    _node_attributes = {"format": "102"}  # fixed code for CCYYMMDD


@cii_node("udt")
class DepartmentName(ValueClass):
    """Department Name (of contact person)."""


@cii_node("udt")
class Description(ValueClass):
    """
    Description as text for a node that needs further description.
    """


@cii_node("udt")
class DuePayableAmount(ValueClass):
    """Amount due for payment."""


@cii_node("udt")
class EndDateTime:
    """End time of a period formatted as 'CCYYMMDD'."""

    def __init__(self, value):
        self._sub_element = DateTimeString(value)


@cii_node("udt")
class ExemptionReason(ValueClass):
    """VAT exemption reason (free text)."""


@cii_node("udt")
class ExemptionReasonCode(ValueClass):
    """Reason for the exemption of VAT provided in code."""


@cii_node("ram")
class FaxUniversalCommunication(UniversalCommunication):
    """Details about the contact fax number."""


@cii_node("qdt")
class FormattedIssueDateTime:
    """Order confirmation date"""

    def __init__(self, value):
        self._sub_element = DateTimeString(value)


@cii_node("udt")
class GlobalID(SchemeClass):
    """
    For GlobalIDs with a schemeID
    (by implementation the schemeID is optional, but by facturx definition
    a GlobalID must have a schemeID)
    """


@cii_node("udt")
class GrandTotalAmount(BaseTotalAmount):
    """
    Invoice total amount with VAT.
    The invoice total amount with VAT is the invoice without VAT plus
    the invoice total VAT amount.
    """


@cii_node("udt")
class ID(SchemeClass):
    """For IDs with an optional schemeID"""


@cii_node()
class Indicator(ValueClass):
    """
    Represents an Indicator tag (xs:boolean).
    value should be "true" | "false".
    """


@cii_node("udt")
class IssuerAssignedID(SchemeClass):
    """Context dependent identifier."""


@cii_node("udt")
class LanguageID(ValueClass):
    """Language identifier"""


@cii_node("udt")
class LineID(ValueClass):
    """Line number"""


@cii_node("udt")
class LineOne(ValueClass):
    """address line one."""


@cii_node("qdt")
class LineStatusCode(ValueClass):
    """
    Indicating whether an item includes the prices which must be taken
    into account when calculating the invoice amount, or whether it only
    contains information.
    """


@cii_node("udt")
class LineStatusReasonCode(ValueClass):
    """
    Complements the type to clarify whether the invoice item is one of
    the following:
        - Detail (default positioning)
        - Subtotal
        - Solely information
    When using the field LineStatusCode, the field LineStatusReasonCode
    must apply the following codes:
        - Detail
        - Aggregation
        - Information
    """


@cii_node("udt")
class LineTwo(ValueClass):
    """address line two."""


@cii_node("udt")
class LineThree(ValueClass):
    """address line three."""


@cii_node("udt")
class LineTotalAmount(ValueClass):
    """Sum of invoice line total amount."""


@cii_node("udt")
class Name(ValueClass):
    """The full formal name of an entity."""


@cii_node("udt")
class OccurrenceDateTime:
    """Contractual due date of the invoice"""

    def __init__(self, value):
        self._sub_element = DateTimeString(value)


@cii_node("udt")
class ParentLineID(ValueClass):
    """Parent Line ID. Seems to be optional even for EXTENDED"""


@cii_node("udt")
class PersonName(ValueClass):
    """Contact Name."""


@cii_node("udt")
class PostcodeCode(ValueClass):
    """The postcode (zip) of an address."""


@cii_node("udt")
class RateApplicablePercent(ValueClass):
    """Percent Value like 19.00 for 19%"""

    _do_not_render_on_empty_value = True


@cii_node("udt")
class Reason(ValueClass):
    """Reason for the charge/discount (free text)"""


@cii_node("qdt")
class ReasonCode(ValueClass):
    """
    Reason for allowance or charge (Code).
    (like "95" for Discount).
    If a Reason is given, text must be used as well.
    """


@cii_node("qdt")
class ReferenceTypeCode(ValueClass):
    """Reference codes or schemes depending on the context."""


@cii_node("udt")
class RoundingAmount(ValueClass):
    """
    The amount to be added to the invoice total to round the amount to
    be paid. In some European countries the calculated invoice total
    amount are rounded to 5 cents. The resulting difference of the
    amount can be depicted in the element RoundingAmount by the
    different receipt totals. The rounding rules of the particular
    country have to be respected since those rules are not consistent in
    Europe.
    """


@cii_node("ram")
class SpecifiedTaxRegistration:
    """Detailed tax information (like VAT)"""

    def __init__(self, value, scheme_id=None):
        self._do_render = bool(value)
        self._sub_element = ID(value, scheme_id)


@cii_node("udt")
class StartDateTime:
    """Start time of a period formatted as 'CCYYMMDD'."""

    def __init__(self, value):
        self._sub_element = DateTimeString(value)


@cii_node("udt")
class SubjectCode(ValueClass):
    """Code for qualifying the free text for the invoice"""


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


@cii_node("ram")
class TelephoneUniversalCommunication(UniversalCommunication):
    """Details about the contact phone number."""


@cii_node("udt")
class TestIndicator:
    """Represents a boolean Indicator."""

    def __init__(self, value):
        self._sub_element = Indicator(value)


@cii_node("udt")
class TotalPrepaidAmount(ValueClass):
    """Paid amount."""


@cii_node("udt")
class TradingBusinessName(ValueClass):
    """Trading Business Name."""


@cii_node("qdt")
class TypeCode(ValueClass):
    """Represents a CodeType."""


@cii_node("udt")
class URIID(ValueClass):
    """Node for a URI-ID."""


# ========================================================
# definition of classes with dependencies from other nodes


@dataclass
class BillingSpecifiedPeriodBase:
    """
    Base class for the two BillingSpecifiedPeriod classes in
    SpecifiedLineTradeSettlement and ApplicableHeaderTradeSettlement
    where the latter has also Description attribute

    optional arguments:
    `start_date_time`: start of a period "CCYYMMDD"
    `end_date_time`: end of a period "CCYYMMDD"
    """

    start_date_time: Optional[StartDateTime] = None
    end_date_time: Optional[EndDateTime] = None


@cii_node("ram")
class EmailURIUniversalCommunication:
    """
    Wrapper for the URIID node holding the email-address.
    """

    def __init__(self, email_address):
        self._do_render = bool(email_address)
        self._sub_element = URIID(email_address)


@dataclass
@cii_node("ram")
class DefinedTradeContact:
    """
    Contact Address for Trade Partys. A Trade Party can have multiple
    contact addresses. So instances of this class are stored inside a
    sequence.

    `person_name`: contact name
    `department_name`: department name
    `type_code`: The code specifying the type of trade contact.
            To be chosen from the entries in UNTDID 3139.
    `telephone_universal_communication`: Details about the contact phone number.
    `fax_universal_communication`: believe it or not ;)
    `email_uri_universal_communication`: email-address of the contact person
    """

    person_name: Optional[PersonName] = None
    department_name: Optional[DepartmentName] = None
    type_code: Optional[TypeCode] = None
    telephone_universal_communication: Optional[TelephoneUniversalCommunication] = None
    fax_universal_communication: Optional[FaxUniversalCommunication] = None
    email_uri_universal_communication: Optional[EmailURIUniversalCommunication] = None


@dataclass
@cii_node("ram")
class IncludedTradeTax:
    """
    Included tax for B2C and Tax information on advanced payments
    (same structure).

    required:
    `calculated_amount`: the tax amount
    `type_code`: should be fixed as "VAT"
    `category_code`: choose from UNTID 5305 Entire code list

    optional:
    `rate_applicable_percent`: the tax rate.
            required if used in subnode of NetPriceProductTradePrice.
            optional if used in subnode of SpecifiedAdvancePayment
    `exemption_reason`: VAT exemption reason (free text)
    `exemption_reason_code`: Reason for the exemption of VAT provided in code
    """

    calculated_amount: CalculatedAmount
    type_code: TypeCode
    category_code: CategoryCode
    exemption_reason: Optional[ExemptionReason] = None
    exemption_reason_code: Optional[ExemptionReasonCode] = None
    rate_applicable_percent: Optional[RateApplicablePercent] = None


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


@dataclass
@cii_node("ram")
class SpecifiedLegalOrganization:
    """
    Details about the organization.
    Used as optional subnode from `BaseTradeParty`.
    All arguments of this node are also optional:

    `id`: Registration Number with a schemeID identifier (like SWIFT, EAN)

    """

    id: Optional[ID] = None
    trading_business_name: Optional[TradingBusinessName] = None


@dataclass
@cii_node("ram")
class ReceivableSpecifiedTradeAccountingAccount:
    """
    Detailed information on the accounting reference
    """

    id: ID
    type_code: Optional[TypeCode] = None


@dataclass
class BaseTradeParty:
    """
    Base implementation for all TradePartys
    Subclasses must apply the @cii_node decorator to make the
    `render`-method work.

    required:
    `name`: trade party name
    `postal_address`: instance of `PostalTradeAddress`.

    optional:
    `id`: deviating id
    `global_id`: deviating global id
    `description`: text node if further description is needed.
    `specified_tax_registration`
    """

    name: Name
    postal_address: PostalTradeAddress
    id: Optional[ID] = None
    global_id: Optional[GlobalID] = None
    description: Optional[Description] = None
    specified_legal_organization: Optional[SpecifiedLegalOrganization] = None
    defined_trade_contact: Optional[Sequence[DefinedTradeContact]] = field(default_factory=list)
    specified_tax_registration: Optional[SpecifiedTaxRegistration] = None
