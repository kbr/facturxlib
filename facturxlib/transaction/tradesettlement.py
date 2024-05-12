"""
ApplicableHeaderTradeSettlement related nodes.
"""

from dataclasses import dataclass, field
from typing import Optional, Sequence


from ..common import (
    cii_node,
    GrandTotalAmount,
    TaxBasisTotalAmount,
    TaxTotalAmount,
)


@cii_node("qdt")
class InvoiceCurrencyCode:
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
class ApplicableHeaderTradeSettlement:
    """ """

    invoice_currency_code: str
    specified_trade_settlement_header_monetary_summation: SpecifiedTradeSettlementHeaderMonetarySummation

    def render(self, parent):
        node = self.get_node(parent)

        InvoiceCurrencyCode(self.invoice_currency_code).render(node)
        self.specified_trade_settlement_header_monetary_summation.render(node)
