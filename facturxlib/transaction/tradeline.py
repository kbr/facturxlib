"""
Implementation for the IncludedSupplyChainTradeLineItem node
"""

from dataclasses import dataclass
from typing import Optional

from ..common import (
    cii_node,
    BasisQuantity,
    BilledQuantity,
    CalculatedAmount,
    CategoryCode,
    ChargeAmount,
    LineID,
    Name,
    RateApplicablePercent,
    TypeCode,
)


@dataclass
@cii_node("ram")
class AssociatedDocumentLineDocument:
    """
    Grouping of general position information.
    """

    line_id: LineID

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""
        return cls(line_id=LineID(line.line_id))


@dataclass
@cii_node("ram")
class SpecifiedTradeProduct:
    """
    Aggregation of information about the product or the service provided
    """

    name: Name

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""
        return cls(name=Name(line.name))


@dataclass
@cii_node("ram")
class NetPriceProductTradePrice:
    """
    Detailed information on the net price of the item.
    The net price includes all surchages and discounts, except for VAT.
    """

    charge_amount: ChargeAmount
    basis_quantity: Optional[BasisQuantity] = None

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""
        if line.basis_quantity:
            basis_quantity = BasisQuantity(line.basis_quantity, line.unit_code)
        else:
            basis_quantity = None
        return cls(charge_amount=ChargeAmount(line.charge_amount), basis_quantity=basis_quantity)


@dataclass
@cii_node("ram")
class SpecifiedLineTradeAgreement:
    """
    Detailed information on the price.
    Aggregation of the contract information at line level
    """

    net_product_trade_price: NetPriceProductTradePrice

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""
        return cls(net_product_trade_price=NetPriceProductTradePrice.from_basic_profile(line))


@dataclass
@cii_node("ram")
class SpecifiedLineTradeDelivery:
    """Grouping of delivery details on line level"""

    billed_quantity: BilledQuantity


@dataclass
@cii_node("ram")
class ApplicableTradeTax:
    """
    Line VAT information.
    This section must be used even in the BASIC profile, if the invoice
    needs to show more than one tax type. It is used by
    `SpecifiedLineTradeSettlement`. (This class is different from the
    `tradesettlement.ApplicableTradeTax` by attributes and the their
    cardinality.)

    `calculated_amount`: optional but required if different VATs are used
            in a single invoice.
    `category_code`: required, defaults to standard rate "S"
    `type_code`: required, but fixed to "VAT"
    `rate_applicable_percent`: optional tax percentage, but should be used
            at least when `calculated_amount` is required.
    """

    calculated_amount: Optional[CalculatedAmount] = None  # Note: can be required
    category_code: CategoryCode = CategoryCode("S")  # required with default of "S"
    type_code: TypeCode = TypeCode("VAT")
    rate_applicable_percent: Optional[RateApplicablePercent] = None

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""
        return cls(
            calculated_amount=CalculatedAmount(line.calculated_amount),
            category_code=CategoryCode(line.category_code),
            type_code=TypeCode(line.type_code),
            rate_applicable_percent=RateApplicablePercent(line.rate_applicable_percent),
        )


@dataclass
@cii_node("ram")
class SpecifiedLineTradeSettlement:
    """Grouping of billing information at line level"""

    applicable_trade_tax: ApplicableTradeTax

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""

        return cls(applicable_trade_tax=ApplicableTradeTax.from_basic_profile(line))


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
    specified_line_trade_delivery: SpecifiedLineTradeDelivery
    specified_line_trade_settlement: SpecifiedLineTradeSettlement

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""
        return cls(
            associated_document_line_document=AssociatedDocumentLineDocument.from_basic_profile(line),
            specified_trade_product=SpecifiedTradeProduct.from_basic_profile(line),
            specified_line_trade_agreement=SpecifiedLineTradeAgreement.from_basic_profile(line),
            specified_line_trade_delivery=SpecifiedLineTradeDelivery(
                billed_quantity=BilledQuantity(line.billed_quantity, line.unit_code)
            ),
            specified_line_trade_settlement=SpecifiedLineTradeSettlement.from_basic_profile(line),
        )
