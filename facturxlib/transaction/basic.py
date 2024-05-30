from dataclasses import dataclass, field
from typing import Optional, Sequence

from ..nodes.common import (
    ActualDeliverySupplyChainEvent,
    AllowanceTotalAmount,
    BasisAmount,
    CalculatedAmount,
    CategoryCode,
    ChargeTotalAmount,
    DuePayableAmount,
    GrandTotalAmount,
    LineTotalAmount,
    Name,
    PostalTradeAddress,
    RateApplicablePercent,
    RoundingAmount,
    SpecifiedTaxRegistration,
    TaxBasisTotalAmount,
    TaxTotalAmount,
    TotalPrepaidAmount,
    TypeCode,
)
from .supplychain import SupplyChainTradeTransAction
from .tradeagreement import (
    ApplicableHeaderTradeAgreement,
    BuyerTradeParty,
    SellerTradeParty,
)
from .tradedelivery import (
    ApplicableHeaderTradeDelivery,
)
from .tradeline import (
    IncludedSupplyChainTradeLineItem,
)
from .tradesettlement import (
    ApplicableHeaderTradeSettlement,
    ApplicableTradeTax,
    InvoiceCurrencyCode,
    SpecifiedTradeSettlementHeaderMonetarySummation,
)


@dataclass
class PurePostalAdress:
    """
    Collection class for a TradeParty with an address. Allows to provide
    the data without knowldge of the faxtur-x inner guts.

    required arguments:
    `name`: Name of trade party (buyer/seller etc.)
    `country_id`: country code like "DE" or "FR"

    optional arguments:
    `postcode`: plz or zip
    `line_one`, `line_two`, `line_three`: factur-x accepts up to three distinct
            lines for the postal address.
    `city_name`: city name
    `country_sub_division_name`: if there is any, add it here.
    `vat`: not required but highly recommended for the seller

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
    vat: str = ""


@dataclass
class PureLineItem:
    """
    Collection class for IncludedSupplyChainTradeLineItem representing a
    single invoiced product with net-price, number of items and so on.

    required arguments:
    `line_id`: line counter for the position as string.
               Normalwise starts with 1 (must provided by the application,
               the library makes no calculations) .
    `name`: description of the invoiced item
    `charge_amount`: net-price of the item
    `basis_quantity`: items base quantity (quantity defined by unit_code)
    `billed_quantity`: Invoiced quantity of items (quantity defined by unit_code)
    `line_total_amount`: Invoiced line net amount

    optional arguments:
    `occurence_date`: if given a datetime string of format CCYYMMDD.
                 This argument is optional by the specification but
                 mandatory in germany ("Leistungserbringung").
                 Can be specified here on line level.
    `unit_code`: dimension of the billed items. Defaults to "H87" aka items.
                 But could also be "MON" for monthly billing if a service is
                 charged.
    `category_code`: VAT type code on line level, i.e. "S" for standard rate
                 or "AE" for VAT reverse charge or "G" for free export item
                 without a charged tax. Defaults to "S".
    `calculated_amount`: calculated tax of the line item (required if multiple
                 tax-rates use in a single invoice).
    `type_code`: fixed value: "VAT"
    `rate_applicable_percent`: VAT percent rate as string (like "19.00")
    """

    line_id: str
    name: str
    charge_amount: str
    basis_quantity: str
    billed_quantity: str
    line_total_amount: str
    occurence_date: Optional[str] = None  # optional but mandatory in germany
    unit_code: str = "H87"
    category_code: str = "S"
    calculated_amount: Optional[str] = None
    type_code: str = "VAT"
    rate_applicable_percent: Optional[str] = None


@dataclass
class PureBasicTradeTax:
    """
    Collection class for an ApplicableTradeTax entry.
    """

    tax_basis_total_amount: str
    tax_total_amount: str
    percent_rate: str
    category_code: str = "S"
    type_code: str = "VAT"


@dataclass
class PureBasicTransAction:
    """
    Builds the complex SupplyChainTradeTransAction instance. Required
    arguments are for the nodes of the BASIC profile with a cardinality
    of at least 1. With the optional `lines` argument basic invoices
    can get created.

    required:
    `line_total_amount`: Total amount of all invoice lines (format: "#.00")
            If there are no tax-free invoice items this should be the same
            as `tax_basis_total_amount`.
    `tax_basis_total_amount`: Invoice total amount without VAT (format: "#.00")
    `tax_total_amount`: invoice total taxes ("#.00")
    `grand_total_amount`: invoice total (sum of `net_total` and `tax_total`)("#.00")
    `due_payable_amount`: Amount due for payment
    `seller`: a `PurePostalAdress` instance about the seller
    `buyer`: a `PurePostalAdress` instance about the buyer

    optional:
    `rate_applicabel_percent`: the tax rate to apply.
            This is optional but either this or the argument `trade_taxes`
            should be given to avoid missing data for an invoice with taxes.
    `invoice_currency`: defaults to "EUR"
    `total_prepaid_amount`: Sum of amount paid in advance (defaults to "0.00")
    `charge_total_amount`: total on surcharges on document level (defaults to "")
            (will not get rendered when empty).
    `allowance_total_amount`: Total amount of discounts.
    `rounding_amount`: The amount to be added to the invoice total to round the
            amount to be paid. In some European countries the calculated
            invoice total amount are rounded to 5 cents. The resulting
            difference of the amount can be depicted in the element
            RoundingAmount by the different receipt totals. The rounding
            rules of the particular country have to be respected since
            those rules are not consistent in Europe.
    `occurence_date`: if given a datetime string of format CCYYMMDD.
            Can be specified here on document level if not given by the
            line items. (The occurence date is mandatory in Germany.)
    `lines`: a squence of `PureLineItem` instances. Optional by the specification.
    `trade_taxes`: a sequence of `PureBasicTradeTax` instances.
            If no instance is given, the `net_total` and `tax_total` values
            are used according with the `PureBasicTradeTax` default settings.
            If the default settings do not apply, at least one entry of
            `PureBasicTradeTax` is required. Multiple entries are required if
            for i.e. more than a single percent_rate is used for the
            invoice-items (and therefor transaction).
    """

    line_total_amount: str
    tax_basis_total_amount: str
    tax_total_amount: str
    grand_total_amount: str
    due_payable_amount: str
    seller: PurePostalAdress
    buyer: PurePostalAdress
    invoice_currency: str = "EUR"
    total_prepaid_amount: str = "0.00"
    charge_total_amount: str = ""  # suppressed in output if not set
    allowance_total_amount: str = ""  # suppressed in output if not set
    rounding_amount: str = ""  # suppressed in output if not set
    occurence_date: Optional[str] = None  # optional but mandatory in germany
    rate_applicabel_percent: Optional[str] = None
    lines: Optional[Sequence[PureLineItem]] = field(default_factory=list)
    trade_taxes: Optional[Sequence[PureBasicTradeTax]] = field(default_factory=list)

    def build_transaction(self):
        # collect the line-items
        line_items = [IncludedSupplyChainTradeLineItem.from_basic_profile(line=line) for line in self.lines]

        # build the ApplicableHeaderTradeAgreement
        seller = SellerTradeParty(
            name=Name(self.seller.name),
            postal_address=PostalTradeAddress.from_pure_postal_address(self.seller),
            specified_tax_registration=SpecifiedTaxRegistration(self.seller.vat, "VAT"),
        )
        buyer = BuyerTradeParty(
            name=Name(self.buyer.name),
            postal_address=PostalTradeAddress.from_pure_postal_address(self.buyer),
            specified_tax_registration=SpecifiedTaxRegistration(self.buyer.vat, "VAT"),
        )
        applicable_header_trade_agreement = ApplicableHeaderTradeAgreement(
            seller=seller,
            buyer=buyer,
        )

        # build the ApplicableHeaderTradeDelivery
        actual_delivery_supply_chain_event = ActualDeliverySupplyChainEvent(occurence_date=self.occurence_date)
        applicable_header_trade_delivery = ApplicableHeaderTradeDelivery(
            actual_delivery_supply_chain_event=actual_delivery_supply_chain_event
        )

        # build the ApplicableHeaderTradeSettlement
        # for that the monetary summation is needed:

        #         charge_total_amount = ChargeTotalAmount(self.charge_total_amount) if self.charge_total_amount else None
        #         allowance_total_amount = AllowanceTotalAmount(self.allowance_total_amount) if self.allowance_total_amount else None
        #         rounding_amount = RoundingAmount(self.rounding_amount) if self.rounding_amount else None
        monetary_summation = SpecifiedTradeSettlementHeaderMonetarySummation(
            line_total_amount=LineTotalAmount(self.line_total_amount),
            tax_basis_total_amount=TaxBasisTotalAmount(self.tax_basis_total_amount, self.invoice_currency),
            grand_total_amount=GrandTotalAmount(self.grand_total_amount, self.invoice_currency),
            due_payable_amount=DuePayableAmount(self.due_payable_amount),
            charge_total_amount=ChargeTotalAmount(self.charge_total_amount),
            allowance_total_amount=AllowanceTotalAmount(self.allowance_total_amount),
            tax_total_amounts=[TaxTotalAmount(self.tax_total_amount, self.invoice_currency)],
            rounding_amount=RoundingAmount(self.rounding_amount),
            total_prepaid_amount=TotalPrepaidAmount(self.total_prepaid_amount),
        )
        # prepare the ApplicableTradeTax instances:
        if not self.trade_taxes:
            self.trade_taxes.append(
                PureBasicTradeTax(
                    tax_basis_total_amount=self.tax_basis_total_amount,
                    tax_total_amount=self.tax_total_amount,
                    percent_rate=self.rate_applicabel_percent,
                )
            )
        trade_taxes = []
        for item in self.trade_taxes:
            trade_taxes.append(
                ApplicableTradeTax(
                    calculated_amount=CalculatedAmount(item.tax_total_amount),
                    type_code=TypeCode(item.type_code),
                    basis_amount=BasisAmount(item.tax_basis_total_amount),
                    category_code=CategoryCode(item.category_code),
                    rate_applicable_percent=RateApplicablePercent(item.percent_rate),
                )
            )

        applicable_header_trade_settlement = ApplicableHeaderTradeSettlement(
            invoice_currency_code=InvoiceCurrencyCode(self.invoice_currency),
            applicable_trade_taxes=trade_taxes,
            specified_trade_settlement_header_monetary_summation=monetary_summation,
        )

        return SupplyChainTradeTransAction(
            line_items=line_items,
            applicable_header_trade_agreement=applicable_header_trade_agreement,
            applicable_header_trade_delivery=applicable_header_trade_delivery,
            applicable_header_trade_settlement=applicable_header_trade_settlement,
        )
