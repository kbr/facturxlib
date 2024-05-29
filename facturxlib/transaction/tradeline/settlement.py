"""
Module for the SpecifiedLineTradeSettlement node.

"""

from dataclasses import dataclass, field
from typing import Optional, Sequence

from facturxlib.nodes.common import (
    cii_node,
    ActualAmount,
    AllowanceTotalAmount,
    BasisAmount,
    BillingSpecifiedPeriodBase,
    CalculatedAmount,
    CalculationPercent,
    CategoryCode,
    ChargeTotalAmount,
    ChargeIndicator,
    ExemptionReason,
    ExemptionReasonCode,
    GrandTotalAmount,
    LineTotalAmount,
    Reason,
    ReasonCode,
    RateApplicablePercent,
    ReceivableSpecifiedTradeAccountingAccount,
    TaxTotalAmount,
    TypeCode,
    ValueClass,
)
from facturxlib.nodes.documents import (
    ReferencedDocumentType_3,
    ReferencedDocumentType_4,
)


@cii_node("udt")
class TotalAllowanceChargeAmount(ValueClass):
    """
    Total amount of allowances / charges
    """


@dataclass
@cii_node("ram")
class SpecifiedTradeSettlementLineMonetarySummation:
    """
    Detailed information about item totals

    required:
    `line_total_amount`: Invoice line net amount

    optional:
    `charge_total_amount`: ChargeTotalAmount
    `allowance_total_amount`: AllowanceTotalAmount
    `tax_total_amount`: TaxTotalAmount
    `grand_total_amount`: GrandTotalAmount
    `total_allowance_charge_amount`: Total amount of allowances / charges
    """

    line_total_amount: LineTotalAmount
    charge_total_amount: Optional[ChargeTotalAmount] = None
    allowance_total_amount: Optional[AllowanceTotalAmount] = None
    tax_total_amount: Optional[TaxTotalAmount] = None
    grand_total_amount: Optional[GrandTotalAmount] = None
    total_allowance_charge_amount: Optional[TotalAllowanceChargeAmount] = None

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""
        return cls(line_total_amount=LineTotalAmount(line.line_total_amount))


@dataclass
@cii_node("ram")
class ApplicableTradeTax:
    """
    Line VAT information. A group of business definitions which contain
    information about VAT and apply to the invoice line items for goods
    and services on the invoice. This section must be used even in the
    BASIC profile, if the invoice needs to show more than one tax type.

    required:
    `type_code`: required, but fixed to "VAT"

    optional:
    `calculated_amount`: optional but required if different VATs are used
            in a single invoice.
    `category_code`: required, defaults to standard rate "S"
    `rate_applicable_percent`: optional tax percentage, but should be used
            at least when `calculated_amount` is required.
    `exemption_reason`: VAT exemption reason (free text)
    """

    calculated_amount: Optional[CalculatedAmount] = None  # Note: can be required
    category_code: CategoryCode = CategoryCode("S")  # required with default of "S"
    type_code: TypeCode = TypeCode("VAT")
    rate_applicable_percent: Optional[RateApplicablePercent] = None
    exemption_reason: Optional[ExemptionReason] = None
    exemption_reason_code: Optional[ExemptionReasonCode] = None

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""
        return cls(
            calculated_amount=CalculatedAmount(line.calculated_amount),
            category_code=CategoryCode(line.category_code),
            type_code=TypeCode(line.type_code),
            rate_applicable_percent=RateApplicablePercent(line.rate_applicable_percent),
        )


@cii_node("ram")
class BillingSpecifiedPeriod(BillingSpecifiedPeriodBase):
    """
    Invoice line billing period
    """


@dataclass
@cii_node("ram")
class SpecifiedTradeAllowanceCharge:
    """
    Details on allowances and charges on line level. A group of business
    terms providing information about the applicable discounts on the
    invoice line item. Details on surcharges and discounts.

    required:
    `actual_amount`: The amount of the discount / surcharge or discount without VAT

    optional:
    `charge_indicator`: Charges and Allowances line Indicator (boolean)
            In case of a discount (BG-27) the value of the
            ChargeIndicators has to be "false". In case of a surcharge
            (BG-28) the value of the ChargeIndicators has to be "true".
    `calculation_percent`: Discount / surcharge in percentage
    `basis_amount`: Base amount for the discount / surcharge
    `reason_code`: The invoice line discount / surcharge reason code
    `reason`: Discount or surcharge reason (free text)
    """

    actual_amount: ActualAmount
    charge_indicator: Optional[ChargeIndicator] = None
    calculation_percent: Optional[CalculationPercent] = None
    basis_amount: Optional[BasisAmount] = None
    reason_code: Optional[ReasonCode] = None
    reason: Optional[Reason] = None


@cii_node("ram")
class InvoiceReferencedDocument(ReferencedDocumentType_4):
    """
    No further description.
    """


@cii_node("ram")
class AdditionalReferencedDocument(ReferencedDocumentType_3):
    """
    Object identifier at the invoice item level.
    """


@dataclass
@cii_node("ram")
class SpecifiedLineTradeSettlement:
    """
    Grouping of billing information at line level

    required:
    `applicable_trade_tax`: Line VAT information
    `specified_trade_settlement_line_monetary_summation`:
            Detailed information about item totals

    optional:
    `billing_specified_period`: Invoice line billing period
    `specified_trade_allowance_charge`: Details on allowances and charges
            on line level
    `invoice_referenced_document`: InvoiceReferencedDocument
    `additional_referenced_documents`: Sequence of Object identifier at
            the invoice item level
    `receivable_specific_trade_accounting_accounts`: Sequence of Detailed
            information on the accounting reference
    """

    applicable_trade_tax: ApplicableTradeTax
    specified_trade_settlement_line_monetary_summation: SpecifiedTradeSettlementLineMonetarySummation
    billing_specified_period: Optional[BillingSpecifiedPeriod] = None
    specified_trade_allowance_charge: Optional[Sequence[SpecifiedTradeAllowanceCharge]] = field(default_factory=list)
    invoice_referenced_document: Optional[InvoiceReferencedDocument] = None
    additional_referenced_documents: Optional[Sequence[AdditionalReferencedDocument]] = field(default_factory=list)
    receivable_specific_trade_accounting_accounts: Optional[Sequence[ReceivableSpecifiedTradeAccountingAccount]] = (
        field(default_factory=list)
    )

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""

        return cls(
            applicable_trade_tax=ApplicableTradeTax.from_basic_profile(line),
            specified_trade_settlement_line_monetary_summation=(
                SpecifiedTradeSettlementLineMonetarySummation.from_basic_profile(line)
            ),
        )
