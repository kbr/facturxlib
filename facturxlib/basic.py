#
#  this file is part of the factorxlib package
#  (c) 2024 Klaus Bremer
#
#  License: to be defined
#
"""
Interface for the BASIC profile.

The function `build_basic_invoice` takes all required and optional
arguments to build the XML according to the BASIC profile. In case not
all arguments are used the function `build_minimal_basic_invoice`
provides a simpler interface.

For the common usecase of smaller companies to just provide the seller-
and buyer-addresses and a list of sold items with a common tax rate, the
class `MinimalInvoice` can simplifiy the creation of an e-invoice even
more.
"""

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Optional, Sequence

from .facturx import build_invoice
from .nodes.common import (
    ActualDeliverySupplyChainEvent,
    DuePayableAmount,
    GrandTotalAmount,
    IncludedNote,
    LineTotalAmount,
    ReceivableSpecifiedTradeAccountingAccount,
    TaxBasisTotalAmount,
    TaxTotalAmount,
)
from .nodes.exchange import (
    DEFAULT_GUIDELINE_SPECIFICATION,
    DEFAULT_INVOICE_TYPE_CODE,
    ExchangedDocument,
    ExchangedDocumentContext,
)
from .nodes.tradeparty import (
    BuyerTradeParty,
    SellerTradeParty,
    ShipToTradeParty,
    SellerTaxRepresentativeTradeParty,
)
from .transaction.supplychain import SupplyChainTradeTransaction
from .transaction.tradeagreement import (
    ApplicableHeaderTradeAgreement,
    BuyerOrderReferencedDocument,
    BuyerReference,
    ContractReferencedDocument,
)
from .transaction.tradedelivery import (
    ApplicableHeaderTradeDelivery,
    DespatchAdviceReferencedDocument,
)
from .transaction.tradeline import IncludedSupplyChainTradeLineItem
from .transaction.tradesettlement import (
    ApplicableHeaderTradeSettlement,
    ApplicableTradeTax,
    BillingSpecifiedPeriod,
    InvoiceCurrencyCode,
    InvoiceReferencedDocument,
    SpecifiedTradeAllowanceCharge,
    SpecifiedTradePaymentTerms,
    SpecifiedTradeSettlementHeaderMonetarySummation,
    SpecifiedTradeSettlementPaymentMeans,
)

DEFAULT_INVOICE_CURRENCY = "EUR"
DEFAULT_QUANTITY_UNIT_CODE = "H87"  # code for an item
DEFAULT_TAX_CATEGORY_CODE = "S"
DEFAULT_TAX_TYPE_CODE = "VAT"


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


@dataclass
class BasicLineItem:
    """
    Dataset for a line item according to the BASIC profile.

    required:
    `line_id`: aka. position number. First item starts with 1.
    `name`: Name of the item (free text)
    `charge_amount`: net price of a single item
    `basis_quantity`: item base quantity as string
    `line_total_amount`: net price of all items (charge_amount * billed_quantity)

    required by BASIC profile and preset with default values:
    `type_code`: tax type code, defaults to "VAT"
    `category_code`: tax category code, defaults to "S" (standard rate)

    optional:
    `billed_quantity`: number of items billed.
    `billed_quantity_unit_code`: billed item quantiy unitcode as string, defaults to Item.
    `basis_quantity_unit_code`: item quantiy unitcode as string, defaults to Item.
    `global_id`: The identification of articles based on a registered scheme
    `global_id_scheme_id`: the according scheme, required if a global_id is given.
    `specified_trade_allowance_charges`: a sequence of SpecifiedTradeAllowanceCharge instances

    """

    line_id: str
    name: str
    charge_amount: str
    basis_quantity: str
    line_total_amount: str

    billed_quantity: Optional[str] = None
    billed_quantity_unit_code: str = DEFAULT_QUANTITY_UNIT_CODE
    basis_quantity_unit_code: str = DEFAULT_QUANTITY_UNIT_CODE
    rate_applicable_percent: Optional[str] = None
    type_code: str = DEFAULT_TAX_TYPE_CODE
    category_code: str = DEFAULT_TAX_CATEGORY_CODE

    global_id: Optional[str] = None
    global_id_scheme_id: Optional[str] = None
    specified_trade_allowance_charges: Optional[Sequence[SpecifiedTradeAllowanceCharge]] = field(default_factory=list)

    @classmethod
    def from_partial_data(
        cls,
        line_id: str,
        name: str,
        charge_amount: str,
        rate_applicable_percent: str,
        basis_quantity: str = "1",
        line_total_amount: str = "",
        billed_quantity: Optional[str] = None,
        billed_quantity_unit_code: str = DEFAULT_QUANTITY_UNIT_CODE,
        basis_quantity_unit_code: str = DEFAULT_QUANTITY_UNIT_CODE,
        type_code: str = DEFAULT_TAX_TYPE_CODE,
        category_code: str = DEFAULT_TAX_CATEGORY_CODE,
        global_id: Optional[str] = None,
        global_id_scheme_id: Optional[str] = None,
        specified_trade_allowance_charges: Optional[Sequence[SpecifiedTradeAllowanceCharge]] = field(
            default_factory=list
        ),
    ):
        """
        Constructor based on partial required data.
        `line_id`, `name`, `charge_amount` and `rate_applicable_percent`
        are required. `basis_quantity` is set to 1 and if not value is
        given to `billed_quantity` it is set to the value from
        `basis_quantity`. If `line_total_amount` is not given it is set
        to the value from `charge_amount` assuming basis- and billed
        quantity are set to 1. It is up to the application to consistent
        arguments. All other arguments stay on the default-values
        defined at class level.
        """
        if not line_total_amount:
            line_total_amount = charge_amount
        if not billed_quantity:
            billed_quantity = basis_quantity

        return cls(
            line_id=line_id,
            name=name,
            charge_amount=charge_amount,
            rate_applicable_percent=rate_applicable_percent,
            basis_quantity=basis_quantity,
            line_total_amount=line_total_amount,
            billed_quantity=billed_quantity,
            billed_quantity_unit_code=billed_quantity_unit_code,
            basis_quantity_unit_code=basis_quantity_unit_code,
            type_code=type_code,
            category_code=category_code,
            global_id=global_id,
            global_id_scheme_id=global_id_scheme_id,
            specified_trade_allowance_charges=specified_trade_allowance_charges,
        )

    @classmethod
    def from_minimal_data(cls, line_id: str, name: str, charge_amount: str, **kwargs):
        """
        Variant of `from_partial_data` that allows to ommit the
        `rate_applicable_percent` argument. This can be used in
        combination with the `build_minimal_basic_invoice` function
        which checks for the missing argument and substitutes it with
        the `rate_applicable_percent` argument given there. This can be
        used as a shortcut the create simple invoices where all items
        have the same tax-rate.
        """
        if "rate_applicable_percent" not in kwargs:
            kwargs["rate_applicable_percent"] = None
        return cls.from_partial_data(line_id=line_id, name=name, charge_amount=charge_amount, **kwargs)


@dataclass
class MinimalInvoiceHeader:
    """
    Convenience dataclass for the required header of a minimal BASIC
    profile invoice.
    """

    invoice_id: str
    invoice_issue_date: str
    delivery_occurence_date: str


@dataclass
class MinimalInvoiceTotal:
    """
    Convenience dataclass for the required totals of a minimal BASIC
    profile invoice.
    """

    line_total_amount: str
    rate_applicable_percent: str
    tax_total_amount: str
    grand_total_amount: str
    due_date: str


@dataclass
class MinimalInvoice:
    """
    Wrapper to hold the minimal dataset for an invoice supporting the
    BASIC profile. This is a utility class to make it easier for simple
    scenarios to set up the building blocks:

    - `seller` the seller-tradeparty
    - `buyer` the buyer-tradeparty
    - `header` the minimal header data
    - `basic_line_items` a list of line-items
    - `total` the invoice total data

    After instanciation just call `build` to get the invoice as xml.
    `build` is a wrapper for the function call
    `build_minimal_basic_invoice` which in turn is a wrapper for
    `build_basic_invoice`.
    """

    seller: BasicTradeParty
    buyer: BasicTradeParty
    header: MinimalInvoiceHeader
    basic_line_items: Sequence[BasicLineItem]
    total: MinimalInvoiceTotal

    def build(self):
        """
        Returns the invoice as string in XML format.
        """
        return build_minimal_basic_invoice(
            invoice_id=self.header.invoice_id,
            invoice_issue_date=self.header.invoice_issue_date,
            buyer=self.buyer,
            seller=self.seller,
            basic_line_items=self.basic_line_items,
            line_total_amount=self.total.line_total_amount,
            rate_applicable_percent=self.total.rate_applicable_percent,
            tax_total_amount=self.total.tax_total_amount,
            grand_total_amount=self.total.grand_total_amount,
            due_date=self.total.due_date,
        )


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
    basic_line_items: Optional[Sequence[BasicLineItem]] = field(default_factory=list),
    delivery_occurence_date: Optional[str] = None,
    invoice_currency_code: str = DEFAULT_INVOICE_CURRENCY,
    invoice_type_code: str = DEFAULT_INVOICE_TYPE_CODE,
    document_included_notes: Optional[IncludedNote] = None,
    document_guideline_specification: str = DEFAULT_GUIDELINE_SPECIFICATION,
    document_business_process_id: Optional[str] = None,
    agreement_buyer_reference: Optional[BuyerReference] = None,
    agreement_buyer_order_referenced_document: Optional[BuyerOrderReferencedDocument] = None,
    agreement_contract_referenced_document: Optional[ContractReferencedDocument] = None,
    agreement_seller_tax_representative_trade_party: Optional[SellerTaxRepresentativeTradeParty] = None,
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
            level. But the VAT relevant date of delivery and achievement
            must be specified on the level of document (that means
            here). If it is given here, the value will override an
            optional `delivery_actual_delivery_supply_chain_event`
            argument.
    `invoice_currency`: required and preset with "EUR" as default.

    required with default values:
    `invoice_type_code`: defaults to commercial invoice ("380")
    `document_guideline_specifikation`: defaults to "urn:cen.eu:en16931:2017"

    optional:
    `basic_line_items`: Sequence of BasicLineItems. This is optional by definition,
            even if an invoice makes rarely sense without line-items.
    `document_included_notes`: included notes on document level
    `document_business_process_id`: if given may allowing the buyer to
            process the invoice in an appropriate manner.
    `agreement_buyer_reference`: a BuyerReference instance
            (An identifier assigned by the buyer used for internal routing purposes.)
    `agreement_buyer_order_referenced_document`:
            a BuyerOrderReferencedDocument instance with details of the associated order
    `agreement_contract_referenced_document`:
            a ContractReferencedDocument instance with details of the associated contract
    `agreement_seller_tax_representative_trade_party`:
            the seller’s tax representative.
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
        seller_tax_representative_trade_party=agreement_seller_tax_representative_trade_party,
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

    line_items = basic_line_items if basic_line_items else []
    if isinstance(line_items, Iterable):
        included_supply_chain_trade_line_items = [
            IncludedSupplyChainTradeLineItem.from_basic_line_item(line_item) for line_item in line_items
        ]
    else:
        included_supply_chain_trade_line_items = []

    supply_chain_trade_transaction = SupplyChainTradeTransaction(
        applicable_header_trade_agreement=applicable_header_trade_agreement,
        applicable_header_trade_delivery=applicable_header_trade_delivery,
        applicable_header_trade_settlement=applicable_header_trade_settlement,
        included_supply_chain_trade_line_items=included_supply_chain_trade_line_items,
    )

    return build_invoice(
        exchanged_document_context=exchanged_document_context,
        exchanged_document=exchanged_document,
        supply_chain_trade_transaction=supply_chain_trade_transaction,
    )


def build_minimal_basic_invoice(
    invoice_id: str,
    invoice_issue_date: str,
    buyer: BasicTradeParty,
    seller: BasicTradeParty,
    line_total_amount: str,
    rate_applicable_percent: str,
    tax_total_amount: str,
    grand_total_amount: str,
    basic_line_items: Sequence[BasicLineItem],
    delivery_occurence_date: Optional[str] = None,
    buyer_reference: Optional[str] = None,
    due_payable_amount: str = "",
    tax_basis_total_amount: str = "",
    tax_category_code: str = DEFAULT_TAX_CATEGORY_CODE,
    tax_type_code: str = DEFAULT_TAX_TYPE_CODE,
    invoice_currency_code: str = DEFAULT_INVOICE_CURRENCY,
    invoice_type_code: str = DEFAULT_INVOICE_TYPE_CODE,
    due_date: str = "",
    description: str = "",
):
    """
    Simplified version of `build_basic_invoice`. It makes the assumption
    that for all amounts the `invoice_currency_code` is used and that
    for all traded items there is just a single tax-rate given by
    `rate_applicable_percent`.
    Also there is just a seller- and a buyer-tradeparty involved and
    there are no attached documents.

    required:
    `invoice_id`: number of the invoice like "123" or "123/2024"
    `invoice_issue_date`: date formatted as "CCYYMMDD"
    `buyer`: buyer information as BasicTradeParty
    `seller`: seller information as BasicTradeParty
    `line_total_amount`: Invoice net total
    `rate_applicable_percent`: the invoice tax rate in percent, like "19.00".
    `tax_total_amount`: The total of the taxes.
    `grand_total_amount`: the total of the invoice including taxes.
    `basic_line_items`: Sequence of BasicLineItems. This is optional by definition,
            but it makes no sense to have an invoice without line-items.

    optional but mandatory in Germany:
    `delivery_occurence_date`: this value (as "CCYYMMDD") is optional
            but mandatory in Germany. It can be given here or on line
            level. But the VAT relevant date of delivery and achievement
            must be specified on the level of document (that means
            here). If it is given here, the value will override an
            optional `delivery_actual_delivery_supply_chain_event`
            argument.

    optional:
    `buyer_reference`: an id assigned by the buyer (like SAP number)
    `due_payable_amount`: the amount due for payment as string (like "0.00").
            If not given the value is taken from `grand_total_amount`.
    `tax_basis_total_amount`: total amount to apply taxes on (total net price).
            If not given the value is taken from `line_total_amount`
            which is the invoice net price.
    `tax_category_code`: defaults to "S" (standard rate)
    `tax_type_code`: defaults to "VAT" (fixed value)
    `invoice_currency`: required and preset with "EUR" as default.
    `invoice_type_code`: defaults to commercial invoice ("380")
    """
    the_buyer_reference = BuyerReference(buyer_reference) if buyer_reference else None

    # subsitute missing rate_applicable_percent values on BasicLineItem instances:
    for basic_line_item in basic_line_items:
        if basic_line_item.rate_applicable_percent is None:
            basic_line_item.rate_applicable_percent = rate_applicable_percent

    tax_basis_value = tax_basis_total_amount if tax_basis_total_amount else line_total_amount
    tax_basis_total = TaxBasisTotalAmount(value=tax_basis_value)

    applicable_trade_taxes = [
        ApplicableTradeTax.from_basic_profile(
            basis_amount=tax_basis_value,
            rate_applicable_percent=rate_applicable_percent,
            calculated_amount=tax_total_amount,
            category_code=tax_category_code,
            type_code=tax_type_code,
        )
    ]

    tax_totals = [TaxTotalAmount(value=tax_total_amount, currency_id=invoice_currency_code)]
    grand_total = GrandTotalAmount(value=grand_total_amount)

    if not due_payable_amount:
        due_payable_amount = grand_total_amount

    specified_trade_payment_terms = [
        SpecifiedTradePaymentTerms.from_basic_data(description=description, due_date=due_date)
    ]

    return build_basic_invoice(
        invoice_id=invoice_id,
        invoice_issue_date=invoice_issue_date,
        buyer=buyer,
        seller=seller,
        applicable_trade_taxes=applicable_trade_taxes,
        line_total_amount=line_total_amount,
        tax_basis_total_amount=tax_basis_total,
        tax_total_amounts=tax_totals,
        grand_total_amount=grand_total,
        due_payable_amount=due_payable_amount,
        basic_line_items=basic_line_items,
        delivery_occurence_date=delivery_occurence_date,
        agreement_buyer_reference=the_buyer_reference,
        invoice_currency_code=invoice_currency_code,
        invoice_type_code=invoice_type_code,
        specified_trade_payment_terms=specified_trade_payment_terms,
    )
