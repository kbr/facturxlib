"""
ApplicableHeaderTradeSettlement related nodes.
"""

from dataclasses import dataclass, field
from typing import Optional, Sequence

from ..nodes.cii import cii_node
from ..nodes.common import (
    ActualAmount,
    AllowanceTotalAmount,
    BasisAmount,
    BasisPeriodMeasure,
    BasisQuantity,
    BillingSpecifiedPeriodBase,
    CalculatedAmount,
    CalculationPercent,
    CategoryCode,
    ChargeIndicator,
    ChargeTotalAmount,
    Description,
    DateTimeString,
    DuePayableAmount,
    ExemptionReason,
    ExemptionReasonCode,
    GrandTotalAmount,
    ID,
    IncludedTradeTax,
    LineTotalAmount,
    RateApplicablePercent,
    Reason,
    ReasonCode,
    ReceivableSpecifiedTradeAccountingAccount,
    RoundingAmount,
    TaxBasisTotalAmount,
    TaxTotalAmount,
    TotalPrepaidAmount,
    TypeCode,
    ValueClass,
)
from ..nodes.documents import ReferencedDocumentType_4
from ..nodes.tradeparty import (
    InvoicerTradeParty,
    InvoiceeTradeParty,
    PayeeTradeParty,
    PayerTradeParty,
)


@cii_node("udt")
class AccountName(ValueClass):
    """Payment account name."""


@cii_node("udt")
class ActualDiscountAmount(ValueClass):
    """Payment discount amount."""


@cii_node("udt")
class ActualPenaltyAmount(ValueClass):
    """Payment penalty amount."""


@cii_node("udt")
class AllowanceChargeBasisAmount(ValueClass):
    """Total amount of charges / allowances on document level"""


@cii_node("udt")
class AppliedAmount(ValueClass):
    """Service fee amount"""


@dataclass
@cii_node("udt")
class BasisDateTime:
    """
    Maturity Reference Date.

    required:
    `date_time_string`: Maturity Reference Date, Value
    """

    date_time_string: DateTimeString


@cii_node("udt")
class BICID(ValueClass):
    """Payment service provider identifier."""


@cii_node("udt")
class ConversionRate(ValueClass):
    """Bank assigned creditor identifier."""


@cii_node("xs")
class DateTime(ValueClass):
    """
    Unocumented. Used in `ConversionRateDateTime` aside to the
    `DateTimeString` node.
    xs:dateTime defaults to ISO 8601 : "YYYY-MM-DDThh:mm:ss"
    """


@cii_node()
class DateString(DateTimeString):
    """Tax due date, Value"""


@dataclass
@cii_node("udt")
class ConversionRateDateTime:
    """
    Exchange rate date.

    required:
    `date_time_string`: DateTimeString (value: "CCYYMMDD")
    `date_time`: string as ISO 8601 : "YYYY-MM-DDThh:mm:ss" to store also the time
    """

    date_time_string: DateTimeString
    date_time: DateTime


@cii_node("udt")
class CardholderName(ValueClass):
    """The name of the payment card holder."""


@cii_node("udt")
class CreditorReferenceID(ValueClass):
    """Bank assigned creditor identifier."""


@cii_node("udt")
class DirectDebitMandateID(ValueClass):
    """Mandate reference for SEPA payment."""


@dataclass
@cii_node("udt")
class DueDateDateTime:
    """
    Payment due date.

    required:
    `date_time_string`: The date when the payment is due
    """

    date_time_string: DateTimeString


@cii_node("qdt")
class DueDateTypeCode(ValueClass):
    """Tax due date, code."""


@dataclass
@cii_node("qdt")
class FormattedReceivedDateTime:
    """
    Date of advanced payment.

    required:
    `date_time_string`: Date of advanced payment, value ("CCYYMMDD")
    """

    date_time_string: DateTimeString


@cii_node("udt")
class IBANID(ValueClass):
    """Direct debit: Debited account identifier"""


@cii_node("udt")
class Information(ValueClass):
    """Payment means text"""


@cii_node("udt")
class InvoiceIssuerReference(ValueClass):
    """Remittance Seller reference number."""


@cii_node("qdt")
class InvoiceCurrencyCode(ValueClass):
    """represents a tag specifying a currency code like "EUR"."""


@cii_node("ram")
class InvoiceReferencedDocument(ReferencedDocumentType_4):
    """Preceding Invoice Reference"""


@cii_node("udt")
class LineTotalBasisAmount(ValueClass):
    """Goods value of the tax rate."""


@cii_node("udt")
class PaidAmount(ValueClass):
    """Advanced payment, value."""


@cii_node("udt")
class PartialPaymentAmount(ValueClass):
    """Partial payment amount."""


@cii_node("udt")
class PaymentReference(ValueClass):
    """Remittance information."""


@cii_node("udt")
class ProprietaryID(ValueClass):
    """National account number (not SEPA)."""


@cii_node("udt")
class SequenceNumeric(ValueClass):
    """
    Calculation sequence. Note: Up to level COMFORT only the final
    result of the calculation is given.
    """


@cii_node("qdt")
class SourceCurrencyCode(ValueClass):
    """Invoice currency"""


@cii_node("qdt")
class TargetCurrencyCode(ValueClass):
    """Local currency"""


@cii_node("qdt")
class TaxCurrencyCode(ValueClass):
    """VAT accounting currency code"""


@dataclass
@cii_node("ram")
class TaxApplicableTradeCurrencyExchange:
    """
    Specification of the invoice currency, local currency and exchange rate.

    required:
    `source_currency_code`: Invoice currency
    `target_currency_code`: Local currency
    `conversion_rate`: Exchange rate

    optional:
    `conversion_rate_date_time`: combination of date and date with time
    """

    source_currency_code: SourceCurrencyCode
    target_currency_code: TargetCurrencyCode
    conversion_rate: ConversionRate
    conversion_rate_date_time: Optional[ConversionRateDateTime] = None


@dataclass
@cii_node("udt")
class TaxPointDate:
    """
    The date when the VAT becomes accountable for the seller and for the
    buyer in so far as that date can be determined and differs from the
    date of issue of the invoice, according to the VAT directive.

    This does not apply in Germany. Use date of delivery instead.

    required:
    `date_string`: Tax due date, Value ("CCYYMMDD")
    """

    date_string: DateString


@dataclass
@cii_node("ram")
class ApplicableTradeSettlementFinancialCard:
    """
    Payment card information.

    required:
    `id`: Payment card number

    optional:
    `card_holder_name`: The name of the payment card holder
    """

    id: ID
    card_holder_name: Optional[CardholderName] = None


@dataclass
@cii_node("ram")
class PayerPartyDebtorFinancialAccount:
    """
    Buyer bank information.

    optional:
    `iban_id`: The account to be debited by the direct debit
    """

    iban_id: Optional[IBANID] = None


@dataclass
@cii_node("ram")
class PayeePartyCreditorFinancialAccount:
    """
    Credit Transfer

    optional:
    `iban_id`: A unique identifier of the financial payment account,
            at a payment service provider, to which payment should be made.
    `account_name`: The name of the payment account, at a payment
            service provider, to which the payment should be made. Only
            necessary, if it differs from seller or payment recipient.
    `proprietary_id`: National account number (not SEPA).
            Use IBANID for SEPA payments.
    """

    iban_id: Optional[IBANID] = None
    account_name: Optional[AccountName] = None
    proprietary_id: Optional[ProprietaryID] = None


@dataclass
@cii_node("ram")
class PayeeSpecifiedCreditorFinancialInstitution:
    """
    Seller bank information.

    required:
    `bic_id`: An identifier for the payment service provider where a
            payment account is located
    """

    bic_id: BICID


@dataclass
@cii_node("ram")
class SpecifiedTradeSettlementPaymentMeans:
    """
    Payment instructions

    required:
    `type_code`: Payment means type code. The means expressed as code,
            for how a payment is expected to be or has been settled. The
            entries from the UNTDID 4461 code list shall be used.
            Distinction should be made between SEPA- and non- SEPA
            payments and between credit payments, direct debits, card
            payments and other instruments, i.e.
            - 42 : Payment to bank account,
            - 48 : Payment by credit card

    optional:
    `information`: Payment means text, such as cash, credit transfer,
            direct debit, credit card etc.
    `applicable_trade_settlement_financial_card`: Payment card information.
    `payer_party_debtor_financial_account`: Buyer bank information
    `payee_party_creditor_financial_account`: Credit Transfer
    `payee_specific_creditor_financial_institution`: Seller bank information
    """

    type_code: TypeCode
    information: Information
    applicable_trade_settlement_financial_card: Optional[ApplicableTradeSettlementFinancialCard] = None
    payer_party_debtor_financial_account: Optional[PayerPartyDebtorFinancialAccount] = None
    payee_party_creditor_financial_account: Optional[PayeePartyCreditorFinancialAccount] = None
    payee_specific_creditor_financial_institution: Optional[PayeeSpecifiedCreditorFinancialInstitution] = None


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


@dataclass
@cii_node("ram")
class ApplicableTradeTax:
    """
    VAT Breakdown
    Detailed information on tax data. A group of business terms
    providing information about VAT breakdown by different categories,
    rates and exemption reasons.

    required:
    `calculated_amount`: the applied tax
    `type_code`: VAT type code (fixed value = "VAT")
    `basis_amount`: (aka net price)
    `category_code`: Coded indication of a sales tax category
            (i.e. "S" for standard rate or "AE" for VAT reverse charge)

    optional:
    `exemption_reason`: VAT exemption reason (free text)
    `line_total_basis_amount`: Goods value of the tax rate
    `allowance_charge_basis_amount`: Total amount of charges /
            allowances on document level.
    `exemption_reason_code`: VAT exemption reason code
    `tax_point_date`:  Tax due date.
            This does not apply in Germany. Use date of delivery instead.
    `due_date_type_code`: Code of the date when VAT becomes accountable
            for buyer and seller
    `rate_applicable_percent`: The VAT rate represented as percentage that
            applies for the relevant VAT category (19% -> "19.00")
    """

    calculated_amount: CalculatedAmount
    type_code: TypeCode
    basis_amount: BasisAmount
    category_code: CategoryCode

    exemption_reason: Optional[ExemptionReason] = None
    line_total_basis_amount: Optional[LineTotalBasisAmount] = None
    allowance_charge_basis_amount: Optional[AllowanceChargeBasisAmount] = None
    exemption_reason_code: Optional[ExemptionReasonCode] = None
    tax_point_date: Optional[TaxPointDate] = None
    due_date_type_code: Optional[DueDateTypeCode] = None
    rate_applicable_percent: Optional[RateApplicablePercent] = None

    # don't render empty default values given to the classmethod
    # `from_basic_profile`:
    _suppress_nodes_with_empty_values = """\
        exemption_reason
        exemption_reason_code
        rate_applicable_percent
        due_date_type_code
    """

    @classmethod
    def from_basic_profile(
        cls,
        basis_amount: str,
        calculated_amount: str,
        rate_applicable_percent: str = "",
        category_code="S",
        type_code: str = "VAT",
        exemption_reason: str = "",
        exemption_reason_code: str = "",
        due_date_type_code: str = "",
    ):
        """
        Convenience constructor to convert the given arguments from
        strings to the appropriate nodes.
        """
        return cls(
            calculated_amount=CalculatedAmount(calculated_amount),
            type_code=TypeCode(type_code),
            basis_amount=BasisAmount(basis_amount),
            category_code=CategoryCode(category_code),
            exemption_reason_code=ExemptionReasonCode(exemption_reason_code),
            exemption_reason=ExemptionReason(exemption_reason),
            rate_applicable_percent=RateApplicablePercent(rate_applicable_percent),
            due_date_type_code=DueDateTypeCode(due_date_type_code),
        )


@cii_node("ram")
class BillingSpecifiedPeriod(BillingSpecifiedPeriodBase):
    """
    Detailed information about the invoicing period

    optional arguments:
    `description`: Invoicing period description (free text)
    `start_date_time`: start of a period "CCYYMMDD"
    `end_date_time`: end of a period "CCYYMMDD"

    """

    description: Optional[Description] = None


@dataclass
@cii_node("ram")
class CategoryTradeTax:
    """
    Detailed information on tax information

    required:
    `type_code`: VAT type code for document level allowances / charges
    `category_code`: Coded information on applying sales tax category
            for surcharge or discount on document level.
            (example: AE = VAT reverse charge)

    optional:
    `rate_applicable_percent`: The VAT rate, represented as percentage
            that applies to the document level discount and surcharge
    """

    type_code: TypeCode
    category_code: CategoryCode
    rate_applicable_percent: Optional[RateApplicablePercent] = None


@dataclass
@cii_node("ram")
class AppliedTradeTax:
    """
    Detailed information on tax information

    optional:
    `type_code`: tax type code according to UNTDID 5153 if it is not "VAT".
            In this case the EXTENDED profile is required.
    `category_code`: Tax category
    `rate_applicable_percent`: The tax rate.
    """

    type_code: Optional[TypeCode] = None
    category_code: Optional[CategoryCode] = None
    rate_applicable_percent: Optional[RateApplicablePercent] = None


@dataclass
@cii_node("ram")
class SpecifiedTradeAllowanceCharge:
    """
    Document level allowances /charges.
    Discounts, like withheld taxes, can be stated in this group.

    required:
    `charge_indicator`: Allowances /charges document level Indicator,
            Value (a boolean: "true" | "false")
    `category_trade_tax`: Detailed information on tax information

    optional:
    `sequence_numeric`: Calculation sequence. Note: Up to level COMFORT
            only the final result of the calculation is given.
    `calculation_percent`: The percentage that may be used in conjunction
            with the document level discount base amount, to calculate
            the document level discount amount.
    `basis_amount`: The base amount that may be used in conjunction
            with the document level discount or surcharge percentage to
            calculate the document level charge amount.
    `actual_amount`: The amount of discount or surcharge without VAT
    `reason_code`: The reason for the document level surcharge or
            discount expressed as a code
    """

    charge_indicator: ChargeIndicator
    category_trade_tax: CategoryTradeTax
    sequence_numeric: Optional[SequenceNumeric] = None
    calculation_percent: Optional[CalculationPercent] = None
    basis_amount: Optional[BasisAmount] = None
    basis_quantity: Optional[BasisQuantity] = None
    actual_amount: Optional[ActualAmount] = None
    reason_code: Optional[ReasonCode] = None
    reason: Optional[Reason] = None


@dataclass
@cii_node("ram")
class SpecifiedLogisticsServiceCharge:
    """
    Detailed information on logistics service fees
    (Transport and packaging costs).

    required:
    `description`: Service fee description
    `applied_amount`: Service fee amount

    optional:
    `applied_trade_tax`: sequence of detailed information on tax information
    """

    description: Description
    applied_amount: AppliedAmount
    applied_trade_tax: Optional[Sequence[AppliedTradeTax]] = field(default_factory=list)


@dataclass
@cii_node("ram")
class ApplicableTradePaymentPenaltyTerms:
    """
    Detailed information about penalties.

    optional:
    `basis_date_time`: Maturity Reference Date
    `basis_period_measure`: Due date period
    `basis_amount`: Payment penalty base amount
    `calculation_percent`: Payment penalty percentage
    `actual_penalty_amount`: Payment penalty amount
    """

    basis_date_time: Optional[BasisDateTime] = None
    basis_period_measure: Optional[BasisPeriodMeasure] = None
    basis_amount: Optional[BasisAmount] = None
    calculation_percent: Optional[CalculationPercent] = None
    actual_penalty_amount: Optional[ActualPenaltyAmount] = None


@dataclass
@cii_node("ram")
class ApplicableTradePaymentDiscountTerms:
    """
    Detailed information about payment discounts

    optional:
    `basis_date_time`: Maturity Reference Date
    `basis_period_measure`: Maturity Period
    `basis_amount`: Payment discount base amount
    `calculation_percent`: Payment discount percentage

    """

    basis_date_time: Optional[BasisDateTime] = None
    basis_period_measure: Optional[BasisPeriodMeasure] = None
    basis_amount: Optional[BasisAmount] = None
    calculation_percent: Optional[CalculationPercent] = None
    actual_discount_amount: Optional[ActualDiscountAmount] = None


@dataclass
@cii_node("ram")
class SpecifiedTradePaymentTerms:
    """
    Detailed information about payment terms

    optional:
    `description`: A textual description of the payment terms that apply
            to the amount due for payment (including description of
            possible penalties).
    `due_date_date_time`: The date when the payment is due.
            The payment due date reflects the due date of the net
            payment. For partial payments it states the first net due
            date.
    `direct_debit_mandate_id`: Unique identifier assigned by the payee
            for referencing the direct debit mandate.
    `partial_payment_amount`: Partial payment amount.
    `applicable_trade_payment_penalty_terms`: Detailed information about penalties
    `payee_trade_partys`: Sequence of PayeeTradeParty
    """

    description: Optional[Description] = None
    due_date_date_time: Optional[DueDateDateTime] = None
    direct_debit_mandate_id: Optional[DirectDebitMandateID] = None
    partial_payment_amount: Optional[PartialPaymentAmount] = None
    applicable_trade_payment_penalty_terms: Optional[ApplicableTradePaymentPenaltyTerms] = None
    applicable_trade_payment_discount_terms: Optional[ApplicableTradePaymentDiscountTerms] = None
    payee_trade_partys: Optional[Sequence[PayeeTradeParty]] = field(default_factory=list)


@dataclass
@cii_node("ram")
class SpecifiedAdvancePayment:
    """
    Included tax for advanced payment.

    required:
    `paid_amount`: Advanced payment, value
    `included_trade_taxes`: Sequence of Tax information on advanced payments

    optional:
    `formatted_received_date_time`: Date of advanced payment
    """

    paid_amount: PaidAmount
    included_trade_taxes: Sequence[IncludedTradeTax]
    formatted_received_date_time: Optional[FormattedReceivedDateTime] = None

    _render_selection = """\
        paid_amount
        formatted_received_date_time
        included_trade_taxes
    """


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

    optional:
    `creditor_reference_id`: Unique banking reference identifier of the
            payee or seller assigned by the payee or seller bank.
            Creditor-ID number for SEPA
    `payment_reference`: A textual value used to establish a link between
            the payment and the invoice, issued by the seller. This
            information element helps the seller to assign an incoming
            payment to the relevant payment process.
    `tax_currency_code`: The VAT total amount expressed in the accounting
            currency accepted or required in the country of the seller.
    `invoice_issuer_reference`: Given seller reference number for routing
            purposes after biliteral agreement
    `invoicer_trade_party`: InvoicerTradeParty
    `invoicee_trade_party`: Detailed information about the deviating
            invoice recipient
    `payee_trade_party`: Detailed contact information about the Payee
    `payer_trade_party`: PayerTradeParty
    `tax_applicable_trade_currency_exchange`: Specification of the invoice
            currency, local currency and exchange rate at a given time.
    `specified_trade_settlement_payment_means`: sequence of Payment instructions
    `billing_specified_period`: Detailed information about the invoicing period
    `specified_trade_allowance_charge`: Sequence of document level
            allowances and/or charges.
    `specified_trade_payment_terms`: Sequence of detailed information
            about payment terms
    `invoice_referenced_document`: A group of business terms providing
            information about a preceding invoices.
    `receivable_specified_trade_accounting_accounts`: Sequence of
            detailed information about the accounting reference
    """

    invoice_currency_code: InvoiceCurrencyCode
    applicable_trade_taxes: Sequence[ApplicableTradeTax]
    specified_trade_settlement_header_monetary_summation: SpecifiedTradeSettlementHeaderMonetarySummation
    creditor_reference_id: Optional[CreditorReferenceID] = None
    payment_reference: Optional[PaymentReference] = None
    tax_currency_code: Optional[TaxCurrencyCode] = None
    invoice_issuer_reference: Optional[InvoiceIssuerReference] = None
    invoicer_trade_party: Optional[InvoicerTradeParty] = None
    invoicee_trade_party: Optional[InvoiceeTradeParty] = None
    payee_trade_party: Optional[PayeeTradeParty] = None
    payer_trade_party: Optional[PayerTradeParty] = None
    tax_applicable_trade_currency_exchange: Optional[TaxApplicableTradeCurrencyExchange] = None
    specified_trade_settlement_payment_means: Optional[Sequence[SpecifiedTradeSettlementPaymentMeans]] = field(
        default_factory=list
    )
    billing_specified_period: Optional[BillingSpecifiedPeriod] = None
    specified_trade_allowance_charge: Optional[Sequence[SpecifiedTradeAllowanceCharge]] = field(default_factory=list)
    specified_logistics_service_charge: Optional[Sequence[SpecifiedLogisticsServiceCharge]] = field(
        default_factory=list
    )
    specified_trade_payment_terms: Optional[Sequence[SpecifiedTradePaymentTerms]] = field(default_factory=list)
    invoice_referenced_document: Optional[InvoiceReferencedDocument] = None
    receivable_specified_trade_accounting_accounts: Optional[Sequence[ReceivableSpecifiedTradeAccountingAccount]] = (
        field(default_factory=list)
    )
    specified_advanced_payments: Optional[Sequence[SpecifiedAdvancePayment]] = field(default_factory=list)
