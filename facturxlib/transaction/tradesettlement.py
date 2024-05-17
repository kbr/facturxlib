"""
ApplicableHeaderTradeSettlement related nodes.
"""

from dataclasses import dataclass, field
from typing import Optional, Sequence


from ..common import (
    cii_node,
    BasisAmount,
    CalculatedAmount,
    CategoryCode,
    GrandTotalAmount,
    RateApplicablePercent,
    TaxBasisTotalAmount,
    TaxTotalAmount,
    TypeCode,
)


@cii_node("qdt")
class InvoiceCurrencyCode:
    """represents a tag specifying a currency code like "EUR"."""

    def __init__(self, value):
        self._value = value


@dataclass
@cii_node("ram")
class SpecifiedTradeSettlementHeaderMonetarySummation:
    """
    Detailed information about document totals
    """

    tax_basis_total_amount: Sequence[tuple[str, str]]
    grand_total_amount: Sequence[tuple[str, str]]
    tax_total_amount: Optional[Sequence[tuple[str, str]]] = field(default_factory=list)

    def render(self, parent):
        node = self.get_node(parent)

        for value, unit in self.tax_basis_total_amount:
            TaxBasisTotalAmount(value, unit).render(node)
        for value, unit in self.tax_total_amount:
            TaxTotalAmount(value, unit).render(node)
        for value, unit in self.grand_total_amount:
            GrandTotalAmount(value, unit).render(node)


@dataclass
@cii_node("ram")
class ApplicableTradeTax:
    """
    VAT Breakdown
    Detailed information on tax data. A group of business terms
    providing information about VAT breakdown by different categories,
    rates and exemption reasons.

    `calculated_amount`: the applied tax
    `type_code`: VAT type code (fixed value = "VAT")
    `basis_amount`: (aka net price)
    `category_code`: Coded indication of a sales tax category
            (i.e. "S" for standard rate or "AE" for VAT reverse charge)
    """

    calculated_amount: CalculatedAmount
    type_code: TypeCode
    basis_amount: BasisAmount
    category_code: CategoryCode
    rate_applicable_percent: RateApplicablePercent


@dataclass
@cii_node("ram")
class ApplicableHeaderTradeSettlement:
    """Grouping of payment and billing information"""

    invoice_currency_code: str
    applicable_trade_taxes: Sequence[ApplicableTradeTax]
    specified_trade_settlement_header_monetary_summation: SpecifiedTradeSettlementHeaderMonetarySummation

    def render(self, parent):
        node = self.get_node(parent)

        InvoiceCurrencyCode(self.invoice_currency_code).render(node)
        for trade_tax in self.applicable_trade_taxes:
            # breakpoint()
            trade_tax.render(node)
        self.specified_trade_settlement_header_monetary_summation.render(node)
