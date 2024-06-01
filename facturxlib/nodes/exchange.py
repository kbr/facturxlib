"""
Implements the ExchangedDocumentContext and ExchangedDocument nodes as
well as specific sub-nodes.

"""

from dataclasses import dataclass, field
from typing import Optional, Sequence

from .common import (
    ID,
    CopyIndicator,
    DateTimeString,
    IncludedNote,
    Indicator,
    LanguageID,
    Name,
    TypeCode,
    cii_node,
)

DEFAULT_GUIDELINE_SPECIFICATION = "urn:cen.eu:en16931:2017"
DEFAULT_INVOICE_TYPE_CODE = "380"  # Commercial invoice


@dataclass
@cii_node("ram")
class IssueDateTime:
    """
    Invoice date

    required:
    `date_time_string`: the invoice date as "CCYYMMDD"
    """

    date_time_string: DateTimeString


@dataclass
@cii_node("ram")
class CompleteDateTime:
    """
    Contractual due date of the invoice

    required:
    `date_time_string`: the date as "CCYYMMDD"
    """

    date_time_string: DateTimeString


@dataclass
@cii_node("ram")
class EffectiveSpecifiedPeriod:
    """
    Contractual due date of the invoice.
    Information only required if the contractual due date differs from
    due date of the payment (i.e. for SEPA direct debit).

    required:
    `complete_date_time`: Contractual due date of the invoice
    """

    complete_date_time: CompleteDateTime


@dataclass
@cii_node("ram")
class BusinessProcessSpecifiedDocumentContextParameter:
    """
    Represents Grouping of business process information.

    required:
    `id`: Identifies the context of a business process where the
            transaction is taking place, thus allowing the buyer to
            process the invoice in an appropriate manner.
    """

    id: ID


@dataclass
@cii_node("ram")
class GuidelineSpecifiedDocumentContextParameter:
    """
    Grouping of application recommendation information

    required:
    `id`: Specification Identifier. Here, either compliance or conformance
            of the instance is expressed. Compliant invoices express the
            following: urn:cen.eu:en16931:2017. Invoices compliant with
            a user specification may return the user specification at
            this point. No identification scheme may be used.
    """

    id: ID


@dataclass
@cii_node("ram")
class TestIndicator:
    """
    Test indicator. The Indicator type may be used when implementing a
    new system in order to mark the invoice as „trial invoice“.

    required:
    `indicator`: boolean: "true" | "false"
    """

    indicator: Indicator


@dataclass
@cii_node("rsm")
class ExchangedDocumentContext:
    """
    An aggregation of business terms containing information about the
    business process regarding the rules which are applicable to the
    invoicing document. Grouping of message based properties

    required:
    `guideline_specified_document_context_parameter`: Specification Identifier.
            Compliant invoices express the following:
            urn:cen.eu:en16931:2017.


    optional:
    `test_indicator`: The Indicator type may be used when implementing
            a new system in order to mark the invoice as „trial invoice“.
    `business_process_specified_document_context_parameter`:
            Grouping of business context information. If given, the
            value is given by the buyer and MUST be in the format
            'urn:fdc:peppol.eu:2017:poacc:billing:NN:1.0' where NN
            indicates the process number.
    """

    guideline_specified_document_context_parameter: GuidelineSpecifiedDocumentContextParameter
    business_process_specified_document_context_parameter: Optional[
        BusinessProcessSpecifiedDocumentContextParameter
    ] = None
    test_indicator: Optional[TestIndicator] = None

    _render_sequence = """\
        test_indicator
        business_process_specified_document_context_parameter
    """

    @classmethod
    def from_basic_profile(cls, specification_identifier=DEFAULT_GUIDELINE_SPECIFICATION, business_process_id=None):
        """
        Return an instance with data according to the BASIC profile.
        """
        guideline = GuidelineSpecifiedDocumentContextParameter(id=ID(value=specification_identifier))
        business = None
        if business_process_id:
            business = BusinessProcessSpecifiedDocumentContextParameter(id=business_process_id)
        return cls(
            guideline_specified_document_context_parameter=guideline,
            business_process_specified_document_context_parameter=business,
        )


@dataclass
@cii_node("rsm")
class ExchangedDocument:
    """
    Grouping of characteristics that affect the entire document.

    required:
    id: A unique Identifier for the invoice (aka invoice number).
            This can be a string like "106" or "023/2024".
            The format is defined by the seller and must be unique.
    `type_code`: Document name (Code) like
            "380" : Commercial invoice
            "381" : Credit notification
            "384" : Invoice correction
    `issue_date_time`: invoice date, format: "CCYYMMDD"

    optional:
    `name`: Document name (free text)
    `copy_indicator`: boolean whether it is a copy
    `language_ids`: Sequence of language identifiers.
    `included_notes`: Sequence of included notes.
    `effective_specified_period`: Contractual due date of the invoice.
            Information only required if the contractual due date
            differs from due date of the payment (i.e. for SEPA direct
            debit). Format: CCYYMMDD
    """

    id: ID
    type_code: TypeCode
    issue_date_time: IssueDateTime
    name: Optional[Name] = None
    copy_indicator: Optional[CopyIndicator] = None
    language_ids: Optional[Sequence[LanguageID]] = field(default_factory=list)
    included_notes: Optional[Sequence[IncludedNote]] = field(default_factory=list)
    effective_specified_period: Optional[EffectiveSpecifiedPeriod] = None

    _render_sequence = """\
        id
        name
        type_code
        issue_date_time
        copy_indicator
        language_ids
        included_notes
        effective_specified_period
    """

    @classmethod
    def from_basic_profile(cls, invoice_id, issue_date_time, type_code=DEFAULT_INVOICE_TYPE_CODE, included_notes=None):
        """
        Return an Instance based on data supported by the BASIC profile.

        required:
        `invoice_id`: A unique Identifier for the invoice (aka invoice number).
        `issue_date_time`: invoice date, format: "CCYYMMDD"

        optional:
        `type_code`: defaults to "urn:cen.eu:en16931:2017"
        `included_notes`: list of IncludedNote instances.
        """
        issue_date_time = IssueDateTime(date_time_string=DateTimeString(value=issue_date_time))
        if included_notes is None:
            included_notes = []
        return cls(
            id=ID(value=invoice_id),
            issue_date_time=issue_date_time,
            type_code=TypeCode(value=type_code),
            included_notes=included_notes,
        )
