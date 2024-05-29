"""
Interface for the BASIC profile.
"""

from dataclasses import dataclass, field
from typing import Optional, Sequence

from .facturx import build_invoice

from .nodes.common import (
    cii_node,  # for testing
    ActualDeliverySupplyChainEvent,
    DuePayableAmount,
    GrandTotalAmount,
    IncludedNote,
    LineTotalAmount,
    ReceivableSpecifiedTradeAccountingAccount,
    TaxBasisTotalAmount,
    TaxTotalAmount,
)

from .nodes.tradeparty import (
    BuyerTradeParty,
    SellerTradeParty,
    ShipToTradeParty,
)

from .nodes.exchange import (
    DEFAULT_GUIDELINE_SPECIFICATION,
    DEFAULT_INVOICE_TYPE_CODE,
    ExchangedDocument,
    ExchangedDocumentContext,
)

from .transaction.supplychain import SupplyChainTradeTransAction
from .transaction.tradeagreement import (
    ApplicableHeaderTradeAgreement,
    BuyerReference,
    BuyerOrderReferencedDocument,
    ContractReferencedDocument,
)

from .transaction.tradedelivery import (
    ApplicableHeaderTradeDelivery,
    DespatchAdviceReferencedDocument,
)

from .transaction.tradesettlement import (
    ApplicableTradeTax,
    ApplicableHeaderTradeSettlement,
    BillingSpecifiedPeriod,
    InvoiceCurrencyCode,
    InvoiceReferencedDocument,
    SpecifiedTradeAllowanceCharge,
    SpecifiedTradePaymentTerms,
    SpecifiedTradeSettlementHeaderMonetarySummation,
    SpecifiedTradeSettlementPaymentMeans,
)


DEFAULT_INVOICE_CURRENCY = "EUR"


@cii_node("ram")
class MockNode:
    # for development
    pass


@dataclass
class BasicTradeParty:
    """
    Basic data about a trade party.

    required arguments:
    `name`: Name of trade party ("Example GmbH")
    `country_id`: country code like "DE" or "FR"

    optional arguments:
    `postcode`: plz or zip
    `line_one`, `line_two`, `line_three`: factur-x accepts up to three distinct
            lines for the postal address.
    `city_name`: city name
    `country_sub_division_name`: if there is any, add it here.
    `specified_tax_registration`: the local seller/buyer tax number or the VAT ID
    `specified_tax_registration_scheme`: code for the tax number:
            "FC" for fiscal number
            "VA"  for VAT registration number
    `phone`: phone number for contact
    `fax`: fax number for contact
    `email`: email address
    `identifier`: identifier of a party (i.e. "Kundennummer" applied to a buyer)

    All arguments are strings.
    """

    name: str
    country_id: str
    postcode: str = ""
    line_one: str = ""
    line_two: str = ""
    line_three: str = ""
    city_name: str = ""
    country_sub_division_name: str = ""
    specified_tax_registration: str = ""
    specified_tax_registration_scheme: str = ""
    phone: str = ""
    fax: str = ""
    email: str = ""
    identifier: str = ""


def build_basic_invoice(
    invoice_id: str,
    invoice_issue_date: str,
    buyer: BasicTradeParty,
    seller: BasicTradeParty,
    applicable_trade_taxes: Sequence[ApplicableTradeTax],
    line_total_amount: str,
    tax_basis_total_amount: TaxBasisTotalAmount,
    tax_total_amounts: Sequence[TaxTotalAmount],
    grand_total_amount: GrandTotalAmount,
    due_payable_amount: str,
    delivery_occurence_date: Optional[str] = None,
    invoice_currency_code: str = DEFAULT_INVOICE_CURRENCY,
    invoice_type_code: str = DEFAULT_INVOICE_TYPE_CODE,
    document_included_notes: Optional[IncludedNote] = None,
    document_guideline_specification: str = DEFAULT_GUIDELINE_SPECIFICATION,
    document_business_process_id: Optional[str] = None,
    agreement_buyer_reference: Optional[BuyerReference] = None,
    agreement_buyer_order_referenced_document: Optional[BuyerOrderReferencedDocument] = None,
    agreement_contract_referenced_document: Optional[ContractReferencedDocument] = None,
    delivery_ship_to_trade_party: Optional[ShipToTradeParty] = None,
    delivery_actual_delivery_supply_chain_event: Optional[ActualDeliverySupplyChainEvent] = None,
    delivery_despatch_advice_referenced_document: Optional[DespatchAdviceReferencedDocument] = None,
    specified_trade_settlement_payment_means: Optional[Sequence[SpecifiedTradeSettlementPaymentMeans]] = field(
        default_factory=list
    ),
    billing_specified_period: Optional[BillingSpecifiedPeriod] = None,
    specified_trade_allowance_charges: Optional[Sequence[SpecifiedTradeAllowanceCharge]] = field(default_factory=list),
    specified_trade_payment_terms: Optional[Sequence[SpecifiedTradePaymentTerms]] = field(default_factory=list),
    invoice_referenced_document: Optional[InvoiceReferencedDocument] = None,
    receivable_specified_trade_accounting_accounts: Optional[
        Sequence[ReceivableSpecifiedTradeAccountingAccount]
    ] = field(default_factory=list),
):
    """
    Wrapper to build a CrossIndustryInvoice from data according to the
    BASIC profile, abstracting the most of the node hierarchies.


    required:
    `invoice_id`: number of the invoice like "123" or "123/2024"
    `invoice_issue_date`: date formatted as "CCYYMMDD"
    `buyer`: buyer information as BasicTradeParty
    `seller`: seller information as BasicTradeParty
    `applicable_trade_taxes`: Sequence of ApplicableTradeTax instances
    `line_total_amount`: Invoice net total
    `tax_basis_total_amount`: total amount to apply taxes on
            as TaxBasisTotalAmount because of optional currency information.
    `tax_total_amounts`: Sequence of the total of the taxes as TaxTotalAmount
             because of optional currency information.
    `grand_total_amount`: the total of the invoice including taxes
            as GrandTotalAmount  because of optional currency information.
    `due_payable_amount`: the amount due for payment as string (like "0.00")

    required/optional:
    `delivery_occurence_date`: this value (as "CCYYMMDD") is optional
            but mandatory in Germany. It can be given here or on line
            level. If it is given here, the value will override an
            optional `delivery_actual_delivery_supply_chain_event`
            argument.
    `invoice_currency`: required and preset with "EUR" as default.

    required with default values:
    `invoice_type_code`: defaults to commercial invoice ("380")
    `document_guideline_specifikation`: defaults to "urn:cen.eu:en16931:2017"

    optional:
    `document_included_notes`: included notes on document level
    `document_business_process_id`: if given may allowing the buyer to
            process the invoice in an appropriate manner.
    `agreement_buyer_reference`: a BuyerReference instance
            (An identifier assigned by the buyer used for internal routing purposes.)
    `agreement_buyer_order_referenced_document`:
            a BuyerOrderReferencedDocument instance with details of the associated order
    `agreement_contract_referenced_document`:
            a ContractReferencedDocument instance with details of the associated contract
    `delivery_ship_to_trade_party`:
            Detailed information on the deviating goods recipient
    `delivery_actual_delivery_supply_chain_event`:
            Detailed information about the actual delivery
    `delivery_despatch_advice_referenced_document`:
            Detailed information on the corresponding despatch advice

    additional optional subnodes without required attributes:
    `specified_trade_settlement_payment_means`:
            Sequence of SpecifiedTradeSettlementPaymentMeans
    `billing_specified_period`: Detailed information about the invoicing period
    `specified_trade_allowance_charges`: Document level allowances / charges.
    `specified_trade_payment_terms`:
            Sequence of detailed information about payment terms
    `invoice_referenced_document`: Preceding Invoice Reference
    `receivable_specified_trade_accounting_accounts`:
            Sequence of detailed information on the accounting reference
    """
    exchanged_document_context = ExchangedDocumentContext.from_basic_profile(
        specification_identifier=document_guideline_specification, business_process_id=document_business_process_id
    )
    exchanged_document = ExchangedDocument.from_basic_profile(
        invoice_id=invoice_id,
        issue_date_time=invoice_issue_date,
        type_code=invoice_type_code,
        included_notes=document_included_notes,
    )

    applicable_header_trade_agreement = ApplicableHeaderTradeAgreement(
        buyer=BuyerTradeParty.from_basic_trade_party(buyer),
        seller=SellerTradeParty.from_basic_trade_party(seller),
        buyer_reference=agreement_buyer_reference,
        buyer_order_referenced_document=agreement_buyer_order_referenced_document,
        contract_referenced_document=agreement_contract_referenced_document,
    )

    if delivery_occurence_date:
        delivery_actual_delivery_supply_chain_event = ActualDeliverySupplyChainEvent(delivery_occurence_date)

    applicable_header_trade_delivery = ApplicableHeaderTradeDelivery(
        ship_to_trade_party=delivery_ship_to_trade_party,
        actual_delivery_supply_chain_event=delivery_actual_delivery_supply_chain_event,
        despatch_advice_referenced_document=delivery_despatch_advice_referenced_document,
    )

    specified_trade_settlement_header_monetary_summation = SpecifiedTradeSettlementHeaderMonetarySummation(
        line_total_amount=LineTotalAmount(line_total_amount),
        tax_basis_total_amount=tax_basis_total_amount,
        tax_total_amounts=tax_total_amounts,
        grand_total_amount=grand_total_amount,
        due_payable_amount=DuePayableAmount(due_payable_amount),
    )

    applicable_header_trade_settlement = ApplicableHeaderTradeSettlement(
        invoice_currency_code=InvoiceCurrencyCode(invoice_currency_code),
        applicable_trade_taxes=applicable_trade_taxes,
        specified_trade_settlement_header_monetary_summation=specified_trade_settlement_header_monetary_summation,
        specified_trade_settlement_payment_means=specified_trade_settlement_payment_means,
        billing_specified_period=billing_specified_period,
        specified_trade_allowance_charges=specified_trade_allowance_charges,
        specified_trade_payment_terms=specified_trade_payment_terms,
        receivable_specified_trade_accounting_accounts=receivable_specified_trade_accounting_accounts,
    )

    supply_chain_trade_transaction = SupplyChainTradeTransAction(
        applicable_header_trade_agreement=applicable_header_trade_agreement,
        applicable_header_trade_delivery=applicable_header_trade_delivery,
        applicable_header_trade_settlement=applicable_header_trade_settlement,
        line_items=[],
    )

    return build_invoice(
        exchanged_document_context=exchanged_document_context,
        exchanged_document=exchanged_document,
        supply_chain_trade_transaction=supply_chain_trade_transaction,
    )
