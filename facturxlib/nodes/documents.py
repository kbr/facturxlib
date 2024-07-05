#
#  this file is part of the factorxlib package
#  (c) 2024 Klaus Bremer
#
#  License: to be defined
#
"""
Base classes for documents.

The document attribute definition by facturx is a bit weird:

- Documents sharing the same attributes and cardinalities can have
different names, depending on where they are used.

- Documents with the same name can have different attributes with
different cardinalities, depending on where they are used.

To make this unambigious alls different document-types are defined here
with references, where they are used.

All documents are optional but may have required attributes if the
documents are used. The `BuyerOrderReferencedDocument` is supported by
the BASIC profile. All other document-types are supported by the EN
16931 (comfort) rep. EXTENDED profile. For some classes all attributes
are optional, what makes no real sense. In this cases refer to the
factur-x documentation for more details.

There are eight types of documents:

type 1 for:
    ApplicableHeaderTradeDelivery.DespatchAdviceReferencedDocument
    ApplicableHeaderTradeAgreement.UltimateCustomerOrderReferencedDocument
    SpecifiedLineTradeAgreement.QuotationReferencedDocument
    SpecifiedLineTradeAgreement.BuyerOrderReferencedDocument

type 2 for:
    ApplicableHeaderTradeDelivery.DespatchAdviceReferencedDocument
    ApplicableHeaderTradeAgreement.UltimateCustomerOrderReferencedDocument
    SpecifiedLineTradeAgreement.QuotationReferencedDocument
    SpecifiedLineTradeAgreement.BuyerOrderReferencedDocument

type 3 for:
    SpecifiedLineTradeSettlement.AdditionalReferencedDocument

type 4 for:
    SpecifiedLineTradeSettlement.InvoiceReferencedDocument
    ApplicableHeaderTradeSettlement.InvoiceReferencedDocument

type 5 for:
    SpecifiedLineTradeAgreement.ContractReferencedDocument
    SpecifiedLineTradeDelivery.DeliveryNoteReferencedDocument
    SpecifiedLineTradeDelivery.ReceivingAdviceReferencedDocument
    SpecifiedLineTradeDelivery.DespatchAdviceReferencedDocument
    IncludedSupplyChainTradeLineItem.UltimateCustomerOrderReferencedDocument

type 6 for:
    ApplicableHeaderTradeAgreement.ContractReferencedDocument

type 7 for:
    ApplicableHeaderTradeAgreement.AdditionalReferencedDocument

type 8 for:
    SpecifiedLineTradeAgreement.AdditionalReferencedDocument

All subclasses should be decorated by @cii_node to be renderable.
"""

from dataclasses import dataclass
from typing import Optional, Sequence

from .common import (
    URIID,
    AttachmentBinaryObject,
    FormattedIssueDateTime,
    IssuerAssignedID,
    LineID,
    Name,
    ReferenceTypeCode,
    TypeCode,
)


@dataclass
class ReferencedDocumentType_1:
    """
    Referenced document type 1:

    Document type with all optional attributes. This is the superclass for:

    ApplicableHeaderTradeDelivery.DespatchAdviceReferencedDocument
    ApplicableHeaderTradeAgreement.UltimateCustomerOrderReferencedDocument
    SpecifiedLineTradeAgreement.QuotationReferencedDocument
    SpecifiedLineTradeAgreement.BuyerOrderReferencedDocument

    """

    issuer_assigned_id: Optional[IssuerAssignedID] = None
    formatted_issue_date_time: Optional[FormattedIssueDateTime] = None


@dataclass
class ReferencedDocumentType_2:
    """
    Referenced document type 2:

    Like Document type 1 but `issuer_assigned_id` is required.
    This is the superclass for:

    ApplicableHeaderTradeDelivery.DespatchAdviceReferencedDocument
    ApplicableHeaderTradeAgreement.UltimateCustomerOrderReferencedDocument
    SpecifiedLineTradeAgreement.QuotationReferencedDocument
    SpecifiedLineTradeAgreement.BuyerOrderReferencedDocument

    """

    issuer_assigned_id: IssuerAssignedID
    formatted_issue_date_time: Optional[FormattedIssueDateTime] = None


@dataclass
class ReferencedDocumentType_3:
    """
    Referenced document type 3:
    `issuer_assigned_id` is required, all else optional.

    This is the Superclass for:
    `SpecifiedLineTradeSettlement.AdditionalReferencedDocument`

    """

    type_code: TypeCode
    issuer_assigned_id: Optional[IssuerAssignedID] = None
    formatted_issue_date_time: Optional[FormattedIssueDateTime] = None


@dataclass
class ReferencedDocumentType_4:
    """
    Referenced document type 4:
    `issuer_assigned_id` is required, all else are optional.

    This is the Superclass for:
    `SpecifiedLineTradeSettlement.InvoiceReferencedDocument`
    `ApplicableHeaderTradeSettlement.InvoiceReferencedDocument`
    """

    issuer_assigned_id: IssuerAssignedID
    type_code: Optional[TypeCode] = None
    formatted_issue_date_time: Optional[FormattedIssueDateTime] = None


@dataclass
class ReferencedDocumentType_5:
    """
    Referenced document type 5:

    Like type 3 but with a LineID instead of the TypeCode and all
    attributes are optional.

    This is the superclass for:
    SpecifiedLineTradeAgreement.ContractReferencedDocument
    SpecifiedLineTradeDelivery.DeliveryNoteReferencedDocument
    SpecifiedLineTradeDelivery.ReceivingAdviceReferencedDocument
    SpecifiedLineTradeDelivery.DespatchAdviceReferencedDocument
    IncludedSupplyChainTradeLineItem.UltimateCustomerOrderReferencedDocument

    """

    issuer_assigned_id: Optional[IssuerAssignedID] = None
    line_id: Optional[LineID] = None
    formatted_issue_date_time: Optional[FormattedIssueDateTime] = None


@dataclass
class ReferencedDocumentType_6:
    """
    Referenced document type 6:

    This is the superclass for:
    ApplicableHeaderTradeAgreement.ContractReferencedDocument

    """

    issuer_assigned_id: Optional[IssuerAssignedID] = None
    reference_type_code: Optional[ReferenceTypeCode] = None
    formatted_issue_date_time: Optional[FormattedIssueDateTime] = None


@dataclass
class ReferencedDocumentType_7:
    """
    Referenced document type 7:

    This is the superclass for:
    ApplicableHeaderTradeAgreement.AdditionalReferencedDocument

    """

    issuer_assigned_id: IssuerAssignedID
    type_code: TypeCode
    uri_id: Optional[URIID] = None
    name: Optional[Name] = None
    attachment_binary_object: Optional[AttachmentBinaryObject] = None
    reference_type_code: Optional[ReferenceTypeCode] = None
    formatted_issue_date_time: Optional[FormattedIssueDateTime] = None


@dataclass
class ReferencedDocumentType_8:
    """
    Referenced document type 8:

    `type_code`: required
    `names`: the `name` attribute has an unbound cardinality,
        so names must be a sequences of Name-nodes.

    This is the superclass for:
    SpecifiedLineTradeAgreement.AdditionalReferencedDocument

    """

    type_code: TypeCode
    issuer_assigned_id: Optional[IssuerAssignedID] = None
    uri_id: Optional[URIID] = None
    line_id: Optional[LineID] = None
    names: Optional[Sequence[Name]] = None
    attachment_binary_object: Optional[AttachmentBinaryObject] = None
    reference_type_code: Optional[ReferenceTypeCode] = None
    formatted_issue_date_time: Optional[FormattedIssueDateTime] = None
