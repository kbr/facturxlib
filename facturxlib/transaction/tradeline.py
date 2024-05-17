"""
Implementation for the IncludedSupplyChainTradeLineItem node
"""

from dataclasses import dataclass

from ..common import (
    cii_node,
    LineID,
    Name,
)


@dataclass
@cii_node("ram")
class AssociatedDocumentLineDocument:
    """
    Grouping of general position information.
    """

    line_id: LineID


@dataclass
@cii_node("ram")
class SpecifiedTradeProduct:
    """
    Aggregation of information about the product or the service provided
    """

    name: Name


@dataclass
@cii_node("ram")
class SpecifiedLineTradeAgreement:
    """
    Detailed information on the price.
    Aggregation of the contract information at line level
    """


@dataclass
@cii_node("ram")
class IncludedSupplyChainTradeLineItem:
    """
    An aggregation of business terms containing information about
    individual invoice positions. For every position in the invoice
    there must be an IncludedSupplyChainTradeLineItem-node.
    """

    associated_document_line_document: AssociatedDocumentLineDocument
    specified_trade_product: SpecifiedTradeProduct
