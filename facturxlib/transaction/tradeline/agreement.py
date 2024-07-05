#
#  this file is part of the factorxlib package
#  (c) 2024 Klaus Bremer
#
#  License: to be defined
#
"""
Module for the SpecifiedLineTradeAgreement node.

"""

from dataclasses import dataclass, field
from typing import Optional, Sequence

from facturxlib.nodes.cii import cii_node
from facturxlib.nodes.common import (
    ActualAmount,
    BasisAmount,
    BasisQuantity,
    CalculationPercent,
    ChargeAmount,
    ChargeIndicator,
    IncludedTradeTax,
    Reason,
    ReasonCode,
)
from facturxlib.nodes.documents import (
    ReferencedDocumentType_1,
    ReferencedDocumentType_5,
    ReferencedDocumentType_8,
)


@cii_node("ram")
class BuyerOrderReferencedDocument(ReferencedDocumentType_1):
    """Details of the associated order"""


@cii_node("ram")
class QuotationReferencedDocument(ReferencedDocumentType_1):
    """QuotationReferencedDocument"""


@cii_node("ram")
class ContractReferencedDocument(ReferencedDocumentType_5):
    """Detailed information on the associated contract"""


@cii_node("ram")
class AdditionalReferencedDocument(ReferencedDocumentType_8):
    """Details of an additional document reference"""


@cii_node("ram")
class UltimateCustomerOrderReferencedDocument(ReferencedDocumentType_5):
    """Details of an additional document reference"""


@dataclass
@cii_node("ram")
class AppliedTradeAllowanceCharge:
    """
    Detailed information on discounts and charges.
    required:
    `actual_amount`: The total discount substracted from the gross price
            which leads to the net price.
    optional:
    `charge_indicator`: Switch for charges and discounts.
    `basis_amount`: Discount / Charge base amount
    `reason_code`: Reason for allowance or charge (Code)
    `reason`: Reason for the charge/discount (free text)
    """

    actual_amount: ActualAmount
    charge_indicator: Optional[ChargeIndicator] = None
    calculation_percent: Optional[CalculationPercent] = None
    basis_amount: Optional[BasisAmount] = None
    reason_code: Optional[ReasonCode] = None
    reason: Optional[Reason] = None


@dataclass
@cii_node("ram")
class GrossPriceProductTradePrice:
    """
    Detailed information on the gross price of the item.

    required:
    `charge_amount`: item gross price

    optional:
    `basis_quantity`: item base quantity and optional unit_code
    `applied_trade_allowance_charges`: Detailed information on discounts and charges.
    """

    charge_amount: ChargeAmount
    basis_quantity: Optional[BasisQuantity] = None
    applied_trade_allowance_charges: Optional[Sequence[AppliedTradeAllowanceCharge]] = field(default_factory=list)


@dataclass
@cii_node("ram")
class NetPriceProductTradePrice:
    """
    Detailed information on the net price of the item.
    The net price includes all surchages and discounts, except for VAT.

    required:
    `charge_amount`: item net price

    optional:
    `basis_quantity`: item base quantity and optional unit_code
    `included_trade_tax`: Included tax for B2C
    """

    charge_amount: ChargeAmount
    basis_quantity: Optional[BasisQuantity] = None
    included_trade_tax: Optional[IncludedTradeTax] = None

    @classmethod
    def from_basic_line_item(cls, basic_line_item):
        """line is a BasicLineItem instance."""
        if basic_line_item.basis_quantity:
            basis_quantity = BasisQuantity(basic_line_item.basis_quantity, basic_line_item.basis_quantity_unit_code)
        else:
            basis_quantity = None
        return cls(charge_amount=ChargeAmount(basic_line_item.charge_amount), basis_quantity=basis_quantity)


@dataclass
@cii_node("ram")
class SpecifiedLineTradeAgreement:
    """
    Detailed information on the price.
    Aggregation of the contract information at line level

    required:
    `net_product_trade_price`: Detailed information on the net price of the item.

    optional:
    `buyer_order_referenced_document`: Details of the associated order
    `quotation_referenced_document`: QuotationReferencedDocument
    `contract_referenced_document`: Detailed information on the associated contract
    `additional_referenced_documents`: Sequence of details of an additional document reference
    `ultimate_customer_order_referenced_document`: Sequence of UltimateCustomerOrderReferencedDocument
    """

    net_product_trade_price: NetPriceProductTradePrice
    buyer_order_referenced_document: Optional[BuyerOrderReferencedDocument] = None
    quotation_referenced_document: Optional[QuotationReferencedDocument] = None
    contract_referenced_document: Optional[ContractReferencedDocument] = None
    additional_referenced_documents: Optional[Sequence[AdditionalReferencedDocument]] = field(default_factory=list)
    ultimate_customer_order_referenced_document: Optional[Sequence[UltimateCustomerOrderReferencedDocument]] = field(
        default_factory=list
    )

    @classmethod
    def from_basic_line_item(cls, basic_line_item):
        """line is a BasicLineItem instance."""
        return cls(net_product_trade_price=NetPriceProductTradePrice.from_basic_line_item(basic_line_item))
