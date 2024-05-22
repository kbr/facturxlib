"""
ApplicableHeaderTradeSettlement related nodes.
"""

from dataclasses import dataclass, field
from typing import Optional, Sequence


from ..nodes.common import (
    cii_node,
    AllowanceTotalAmount,
    BasisAmount,
    CalculatedAmount,
    CategoryCode,
    ChargeTotalAmount,
    DuePayableAmount,
    GrandTotalAmount,
    LineTotalAmount,
    RateApplicablePercent,
    RoundingAmount,
    TaxBasisTotalAmount,
    TaxTotalAmount,
    TotalPrepaidAmount,
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

    line_total_amount: str
    tax_basis_total_amount: Sequence[tuple[str, str]]
    grand_total_amount: Sequence[tuple[str, str]]
    total_prepaid_amount: str
    due_payable_amount: str
    tax_total_amount: Optional[Sequence[tuple[str, str]]] = field(default_factory=list)
    charge_total_amount: str = ""
    allowance_total_amount: str = ""
    rounding_amount: str = ""

    def render(self, parent):
        node = self.get_node(parent)

        LineTotalAmount(self.line_total_amount).render(node)
        if self.charge_total_amount:
            ChargeTotalAmount(self.charge_total_amount).render(node)
        if self.allowance_total_amount:
            AllowanceTotalAmount(self.allowance_total_amount).render(node)
        for value, unit in self.tax_basis_total_amount:
            TaxBasisTotalAmount(value, unit).render(node)
        for value, unit in self.tax_total_amount:
            TaxTotalAmount(value, unit).render(node)
        if self.rounding_amount:
            RoundingAmount(self.rounding_amount).render(node)
        for value, unit in self.grand_total_amount:
            GrandTotalAmount(value, unit).render(node)
        TotalPrepaidAmount(self.total_prepaid_amount).render(node)
        DuePayableAmount(self.due_payable_amount).render(node)


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
