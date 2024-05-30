"""
ApplicableHeaderTradeAgreement related nodes.
"""

from dataclasses import dataclass, field
from typing import Optional, Sequence

from ..nodes.cii import cii_node
from ..nodes.common import (
    ID,
    Name,
    ValueClass,
)
from ..nodes.documents import (
    ReferencedDocumentType_1,
    ReferencedDocumentType_2,
    ReferencedDocumentType_6,
    ReferencedDocumentType_8,
)
from ..nodes.tradeparty import (
    BuyerAgentTradeParty,
    BuyerTaxRepresentativeTradeParty,
    BuyerTradeParty,
    ProductEndUserTradeParty,
    SalesAgentTradeParty,
    SellerTaxRepresentativeTradeParty,
    SellerTradeParty,
)


@cii_node("ram")
class AdditionalReferencedDocument(ReferencedDocumentType_8):
    """
    Additional Supporting Documents
    """


@cii_node("qdt")
class DeliveryTypeCode(ValueClass):
    """Delivery condition (Code)"""


@dataclass
@cii_node("ram")
class ApplicableTradeDeliveryTerms:
    """
    Details of the delivery conditions.

    required:
    `delivery_type_code`: Delivery condition (Code)
    """

    delivery_type_code: DeliveryTypeCode


@cii_node("ram")
class BuyerOrderReferencedDocument(ReferencedDocumentType_2):
    """
    Details about the associated order
    """


@cii_node("udt")
class BuyerReference(ValueClass):
    """
    An identifier assigned by the buyer used for internal routing purposes.
    """


@cii_node("ram")
class ContractReferencedDocument(ReferencedDocumentType_6):
    """
    Details of the associated contract
    """


@cii_node("ram")
class QuotationReferencedDocument(ReferencedDocumentType_2):
    """QuotationReferencedDocument"""


@cii_node("ram")
class SellerOrderReferencedDocument(ReferencedDocumentType_2):
    """
    Details about the associated order confirmation
    """


@dataclass
@cii_node("ram")
class SpecifiedPouringProject:
    """
    Details about a project reference

    required:
    `id`: Project reference ID
    `name`: Project name
    """

    id: ID
    name: Name


@cii_node("ram")
class UltimateCustomerOrderReferencedDocument(ReferencedDocumentType_1):
    """UltimateCustomerOrderReferencedDocument"""


@dataclass
@cii_node("ram")
class ApplicableHeaderTradeAgreement:
    """
    Grouping of contract information

    required:
    `seller`: Detailed information about the seller
    `buyer`: Detailed information about the buyer

    optional:
    `buyer_reference`: Buyer reference (provided from the buyer)
    `sales_agent_trade_party`: The sales agent
    `buyer_tax_reprensentative_trade_party`: Buyer tax representative party
    `seller_tax_reprensentative_trade_party`: Seller tax representative party
    `product_end_user_trade_party`: Detailed information about the deviating end user
    `applicable_trade_delivery_terms`: Details of the delivery conditions
    `seller_order_referenced_document`: Details about the associated order confirmation
    `buyer_order_referenced_document`: Details about the associated order
    `quotation_referenced_document`: QuotationReferencedDocument
    `contract_referenced_document`: Details of the associated contract
    `additional_referenced_documents`: Sequence of Additional Supporting Documents
    `specified_procuring_project`: Details about a project reference
    `ultimate_customer_order_referended_documents`: Sequence of UltimateCustomerOrderReferencedDocuments
    """

    seller: SellerTradeParty
    buyer: BuyerTradeParty
    buyer_reference: Optional[BuyerReference] = None
    sales_agent_trade_party: Optional[SalesAgentTradeParty] = None
    buyer_tax_reprensentative_trade_party: Optional[BuyerTaxRepresentativeTradeParty] = None
    seller_tax_reprensentative_trade_party: Optional[SellerTaxRepresentativeTradeParty] = None
    product_end_user_trade_party: Optional[ProductEndUserTradeParty] = None
    applicable_trade_delivery_terms: Optional[ApplicableTradeDeliveryTerms] = None
    seller_order_referenced_document: Optional[SellerOrderReferencedDocument] = None
    buyer_order_referenced_document: Optional[BuyerOrderReferencedDocument] = None
    quotation_referenced_document: Optional[QuotationReferencedDocument] = None
    contract_referenced_document: Optional[ContractReferencedDocument] = None
    additional_referenced_documents: Optional[Sequence[AdditionalReferencedDocument]] = field(default_factory=list)
    buyer_agent_trade_party: Optional[BuyerAgentTradeParty] = None
    specified_procuring_project: Optional[SpecifiedPouringProject] = None
    ultimate_customer_order_referended_documents: Optional[Sequence[UltimateCustomerOrderReferencedDocument]] = field(
        default_factory=list
    )
