""" """

from dataclasses import dataclass, field
from typing import Optional, Sequence

from .common import (
    cii_node,
    CopyIndicator,
    DateTimeString,
    ID,
    IncludedNote,
    TestIndicator,
    TypeCode,
)


DEFAULT_GUIDELINE_SPECIFICATION = "urn:cen.eu:en16931:2017"


@cii_node("udt")
class IssueDateTime:
    """Invoice date"""

    def __init__(self, value):
        self._sub_element = DateTimeString(value)


@cii_node("udt")
class CompleteDateTime:
    """Contractual due date of the invoice"""

    def __init__(self, value):
        self._sub_element = DateTimeString(value)


@cii_node("ram")
class EffectiveSpecifiedPeriod:
    """
    Contractual due date of the invoice.
    Information only required if the contractual due date differs from
    due date of the payment (i.e. for SEPA direct debit).
    """

    def __init__(self, value):
        self._sub_element = CompleteDateTime(value)


@cii_node("udt")
class LanguageID:
    """Language identifier"""

    def __init__(self, value):
        self._value = value


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
            TestIndicator(self.indicator).render(node)
        if self.business_process_id:
            BusinessProcessSpecifiedDocumentContextParameter(self.business_process_id).render(node)
        GuidelineSpecifiedDocumentContextParameter(self.profile).render(node)


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

    optional supported by EXTENDED profile:
    `copy_indicator`: should be "true" | "false"
    `language_ids`: sequence of language ids[0..u]: ("DE", "FR", ...)
    `complete_date`: Contractual due date of the invoice
    """

    invoice_id: str
    issue_date: str
    type_code: str = "380"
    included_note: Optional[IncludedNote] = None
    copy_indicator: str = ""  # should be "true" | "false"
    language_ids: Sequence[str] = field(default_factory=list)
    complete_date: str = ""

    def render(self, parent):
        node = self.get_node(parent)
        ID(self.invoice_id).render(node)
        TypeCode(self.type_code).render(node)
        IssueDateTime(self.issue_date).render(node)
        if self.copy_indicator:
            CopyIndicator(self.copy_indicator).render(node)
        for language_id in self.language_ids:
            LanguageID(language_id).render(node)
        if self.included_note:
            self.included_note.render(node)
        if self.complete_date:
            EffectiveSpecifiedPeriod(self.complete_date).render(node)
