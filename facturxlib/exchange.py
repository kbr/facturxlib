""" """

from dataclasses import dataclass
from typing import Optional

from .common import (
    cii_node,
    ID,
    IncludedNote,
    IssueDateTime,
    TestIndicator,
    TypeCode,
)


DEFAULT_GUIDELINE_SPECIFICATION = "urn:cen.eu:en16931:2017"


@cii_node("ram")
class BusinessProcessSpecifiedDocumentContextParameter:
    """Represents Grouping of business process information."""

    def __init__(self, value):
        self._sub_element = ID(value)


@cii_node("ram")
class GuidelineSpecifiedDocumentContextParameter:
    """Represents a ram:DocumentContextParameterType"""

    def __init__(self, value):
        self._sub_element = ID(value)


@dataclass
@cii_node("ram")
class ExchangedDocumentContext:
    """
    An aggregation of business terms containing information about the
    business process regarding the rules which are applicable to the
    invoicing document. Grouping of message based properties
    """

    indicator: Optional[str] = None
    business_process_id: Optional[str] = None
    profile: str = DEFAULT_GUIDELINE_SPECIFICATION

    def render(self, parent):
        """render: Grouping of message based properties"""
        node = self.get_node(parent)
        if self.indicator is not None:
            indicator = TestIndicator(self.indicator)
            indicator.render(node)
        if self.business_process_id:
            parameter = BusinessProcessSpecifiedDocumentContextParameter(self.business_process_id)
            parameter.render(node)
        profile = GuidelineSpecifiedDocumentContextParameter(self.profile)
        profile.render(node)


@dataclass
@cii_node("ram")
class ExchangedDocument:
    """
    Grouping of characteristics that affect the entire document.

    required arguments:
    `invoice_id`: string representing the invoice number
    `issue_date`: string of invoice date as CCYYMMDD

    optional supported by BASIC profile:
    `type_code`: string, kind of invoice, defaults to "380" (commercial invoice)
    `included_note`: if given must be an instance of -> IncludedNote

    """

    invoice_id: str
    issue_date: str
    type_code: str = "380"
    included_note: Optional[IncludedNote] = None

    def __post_init__(self):
        pass

    def render(self, parent):
        node = self.get_node(parent)
        id = ID(self.invoice_id)
        id.render(node)
        type_code = TypeCode(self.type_code)
        type_code.render(node)
        invoice_date = IssueDateTime(self.issue_date)
        invoice_date.render(node)

        if self.included_note:
            self.included_note.render(node)
