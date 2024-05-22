"""
Implements the ExchangedDocumentContext and ExchangedDocument nodes as
well as specific sub-nodes.

"""

from dataclasses import dataclass, field
from typing import Optional, Sequence

from .common import (
    cii_node,
    CopyIndicator,
    DateTimeString,
    ID,
    IncludedNote,
    LanguageID,
    Name,
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

    `test_indicator`: The Indicator type may be used when implementing
            a new system in order to mark the invoice as „trial invoice“.
    `business_process_id`: Grouping of business process information.
            This identifies the context of a business process where the
            transaction is taking place, thus allowing the buyer to
            process the invoice in an appropriate manner. These data
            make it possible to define the purpose of the settlement
            (invoice of the authorised person, contractual partner,
            subcontractor, settlement document for a building contract
            etc.). If given, the value is given by the buyer and MUST be
            in the format 'urn:fdc:peppol.eu:2017:poacc:billing:NN:1.0'
            where NN indicates the process number.
    `profile`: The identification of the specification which contains
            the entire set of rules for the semantic content, for the
            cardinalities and for the business rules, and with which the
            rules contained in the instance document are conformant.
            Compliant invoices express the following:
            urn:cen.eu:en16931:2017. Invoices compliant with a user
            specification may return the user specification at this
            point. No identification scheme may be used.
            This argument is required and defaults to
            "urn:cen.eu:en16931:2017".
    """

    test_indicator: Optional[str] = None
    business_process_id: Optional[str] = None
    profile: str = DEFAULT_GUIDELINE_SPECIFICATION

    def render(self, parent):
        """render: Grouping of message based properties"""
        node = self.get_node(parent)
        if self.test_indicator is not None:
            TestIndicator(self.test_indicator).render(node)
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
    `name`: document name (free text)
    `type_code`: string, kind of invoice, defaults to "380" (commercial invoice)
    `included_note`: if given must be an instance of -> IncludedNote

    optional supported by EXTENDED profile:
    `copy_indicator`: should be "true" | "false"
    `language_ids`: sequence of language ids[0..u]: ("DE", "FR", ...)
    `effective_specified_period`: Contractual due date of the invoice.
            Information only required if the contractual due date
            differs from due date of the payment (i.e. for SEPA direct
            debit). Format: CCYYMMDD
    """

    invoice_id: str
    issue_date: str
    name: Optional[Name] = None
    type_code: str = "380"
    included_note: Optional[IncludedNote] = None
    copy_indicator: str = ""  # should be "true" | "false"
    language_ids: Sequence[str] = field(default_factory=list)
    complete_date: str = ""
    effective_specified_period: str = ""

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
        if self.effective_specified_period:
            EffectiveSpecifiedPeriod(self.effective_specified_period).render(node)
