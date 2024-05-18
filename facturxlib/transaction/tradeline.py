"""
Implementation for the IncludedSupplyChainTradeLineItem node
"""

from dataclasses import dataclass
from typing import Optional

from ..common import (
    cii_node,
    BasisQuantity,
    ChargeAmount,
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
class NetPriceProductTradePrice:
    """
    Detailed information on the net price of the item.
    The net price includes all surchages and discounts, except for VAT.
    """
    charge_amount: ChargeAmount
    basis_quantity: Optional[BasisQuantity] = None




@dataclass
@cii_node("ram")
class SpecifiedLineTradeAgreement:
    """
    Detailed information on the price.
    Aggregation of the contract information at line level
    """
    net_product_trade_price: NetPriceProductTradePrice

    @classmethod
    def from_base_profile(cls, charge_amount, basis_quantity=None, unit_code="H87"):
        if basis_quantity:
            basis_quantity = BasisQuantity(basis_quantity, unit_code=unit_code)
        return cls(
            net_product_trade_price=NetPriceProductTradePrice(
                charge_amount=ChargeAmount(charge_amount),
                basis_quantity=basis_quantity
            )
        )


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
    specified_line_trade_agreement: SpecifiedLineTradeAgreement

    @classmethod
    def from_basic_profile(cls, line_id, name, charge_amount, billed_quantity, line_total_amount,
        basis_quantity=None, unit_code="H87"
    ):
        return cls(
            associated_document_line_document=AssociatedDocumentLineDocument(LineID(line_id)),
            specified_trade_product=SpecifiedTradeProduct(name=Name(name)),
            specified_line_trade_agreement=SpecifiedLineTradeAgreement.from_base_profile(
                charge_amount=charge_amount,
                basis_quantity=basis_quantity,
                unit_code=unit_code,
            )
        )
