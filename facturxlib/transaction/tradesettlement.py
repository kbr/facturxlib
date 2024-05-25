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

    required:
    `line_total_amount`: Sum of all invoice line net amounts in the invoice
    `tax_basis_total_amount`: The total amount of the invoice without VAT.
    `grand_total_amount`: Invoice total amount with VAT
    `due_payable_amount`: The outstanding amount that is requested to be paid.

    optional:
    `charge_total_amount`: Sum of all surcharges on document level in the invoice
    `allowance_total_amount`: Sum of discounts on document level in the invoice
    `tax_total_amounts`: Sequence of tax total amounts (cardinality 0..2)
    `rounding_amount`: The amount to be added to the invoice total to round
            the amount to be paid. In some European countries the
            calculated invoice total amount are rounded to 5 cents. The
            resulting difference of the amount can be depicted in the
            element RoundingAmount by the different receipt totals. The
            rounding rules of the particular country have to be
            respected since those rules are not consistent in Europe.
    """

    line_total_amount: LineTotalAmount
    tax_basis_total_amount: TaxBasisTotalAmount
    grand_total_amount: GrandTotalAmount
    due_payable_amount: DuePayableAmount
    charge_total_amount: Optional[ChargeTotalAmount] = None
    allowance_total_amount: Optional[AllowanceTotalAmount] = None
    tax_total_amounts: Optional[Sequence[TaxTotalAmount]] = field(default_factory=list)
    rounding_amount: Optional[RoundingAmount] = None
    total_prepaid_amount: Optional[TotalPrepaidAmount] = None

    _render_selection = """\
        line_total_amount
        charge_total_amount
        allowance_total_amount
        tax_basis_total_amount
        tax_total_amounts
        rounding_amount
        grand_total_amount
        total_prepaid_amount
        due_payable_amount
    """
    _suppress_nodes_with_empty_values = """\
        charge_total_amount
        allowance_total_amount
        rounding_amount
    """


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
    """
    Grouping of payment and billing information

    required:
    `invoice_currency_code`: currency code of the invoice i.e. "EUR"
    `applicable_trade_tax`: Sequence of VAT Breakdowns (ApplicableTradeTax)
    `specified_trade_settlement_header_monetary_summation`:
            Detailed information about document totals
    """

    invoice_currency_code: InvoiceCurrencyCode
    applicable_trade_taxes: Sequence[ApplicableTradeTax]
    specified_trade_settlement_header_monetary_summation: SpecifiedTradeSettlementHeaderMonetarySummation
