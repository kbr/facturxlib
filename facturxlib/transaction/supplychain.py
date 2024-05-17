from dataclasses import dataclass, field
from typing import Optional, Sequence


from ..common import (
    cii_node,
    BasisAmount,
    CalculatedAmount,
    CategoryCode,
    LineID,
    Name,
    PostalTradeAddress,
    RateApplicablePercent,
    SpecifiedTaxRegistration,
    TypeCode,
)

from .tradeagreement import (
    ApplicableHeaderTradeAgreement,
    BuyerTradeParty,
    SellerTradeParty,
)

from .tradedelivery import (
    ApplicableHeaderTradeDelivery,
)

from .tradeline import (
    AssociatedDocumentLineDocument,
    IncludedSupplyChainTradeLineItem,
    SpecifiedLineTradeAgreement,
    SpecifiedTradeProduct,
)

from .tradesettlement import (
    ApplicableHeaderTradeSettlement,
    ApplicableTradeTax,
    SpecifiedTradeSettlementHeaderMonetarySummation,
)


@cii_node("ram")
class TransAction:
    _tag_name = "SupplyChainTradeTransAction"


@dataclass
class SupplyChainTradeTransAction(TransAction):
    """
    Provides the transaction interface. Required arguments are for the
    nodes of the BASIC profile with a cardinality of at least 1. With
    the additional `lines` argument basic invoices can get created.

    `net_total`: invoice total net price ("#.00")
    `tax_total`: invoice total taxes ("#.00")
    `grand_total`: invoice total (sum of `net_total` and `tax_total`)("#.00")
    `lines`: sequence of `IncludedSupplyChainTradeLineItem` instances (the sold items).
    """

    net_total: str
    tax_total: str
    grand_total: str
    invoice_currency: str = "EUR"

    #     lines: Optional[Sequence[IncludedSupplyChainTradeLineItem]] = field(default_factory=list)

    def render(self, parent):
        self.node = self.get_node(parent)
        self.node.text = "SupplyChainTradeTransAction dummy marker"


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
    `billed_quantity`: Invoiced quantity of items
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
    """

    line_id: str
    name: str
    charge_amount: str
    billed_quantity: str
    line_total_amount: str
    occurence_date: Optional[str] = None  # optional but mandatory in germany
    unit_code: str = "H87"
    category_code: str = "S"


@dataclass
class PureBasicTradeTax:
    """
    Collection class for an ApplicableTradeTax entry.
    """

    net_amount: str
    tax_amount: str
    percent_rate: str = "19.00"
    category_code: str = "S"
    type_code: str = "VAT"


@dataclass
class PureBasicTransAction(TransAction):
    """
    Provides the transaction interface. Required arguments are for the
    nodes of the BASIC profile with a cardinality of at least 1. With
    the additional `lines` argument basic invoices can get created.

    `net_total`: invoice total net price ("#.00")
    `tax_total`: invoice total taxes ("#.00")
    `grand_total`: invoice total (sum of `net_total` and `tax_total`)("#.00")
    `seller`: a `PurePostalAdress` instance about the seller
    `buyer`: a `PurePostalAdress` instance about the buyer

    optional:
    `invoice_currency`: defaults to "EUR"
    `occurence_date`: if given a datetime string of format CCYYMMDD.
                      Can be specified here on document level.
    `lines`: a squence of `PureLineItem` instances. Optional by the specification.
    `trade_taxes`: a sequence of `PureBasicTradeTax` instances.
            If no instance is given, the `net_total` and `tax_total` values
            are used according with the `PureBasicTradeTax` default settings.
            If the default settings do not apply at least one entry of
            `PureBasicTradeTax` is required. Multiple entries are required if
            for i.e. more than a single percent_rate is used for the
            invoice-items (and therefor transaction).

    """

    net_total: str
    tax_total: str
    grand_total: str
    seller: PurePostalAdress
    buyer: PurePostalAdress
    invoice_currency: str = "EUR"
    occurence_date: Optional[str] = None  # optional but mandatory in germany
    lines: Optional[Sequence[PureLineItem]] = field(default_factory=list)
    trade_taxes: Optional[Sequence[PureBasicTradeTax]] = field(default_factory=list)

    def render(self, parent):
        node = self.get_node(parent)

        for line in self.lines:
            line_item = IncludedSupplyChainTradeLineItem(
                associated_document_line_document=AssociatedDocumentLineDocument(line_id=LineID(line.line_id)),
                specified_trade_product=SpecifiedTradeProduct(name=Name(line.name)),
            )
            line_item.render(node)

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
        ApplicableHeaderTradeAgreement(
            seller=seller,
            buyer=buyer,
        ).render(node)

        ApplicableHeaderTradeDelivery(occurence_date=self.occurence_date).render(node)

        monetary_summation = SpecifiedTradeSettlementHeaderMonetarySummation(
            tax_basis_total_amount=[(self.net_total, self.invoice_currency)],
            tax_total_amount=[(self.tax_total, self.invoice_currency)],
            grand_total_amount=[(self.grand_total, self.invoice_currency)],
        )

        # prepare the ApplicableTradeTax instances:
        if not self.trade_taxes:
            self.trade_taxes.append(
                PureBasicTradeTax(
                    net_amount=self.net_total, tax_amount=self.tax_total
                )
            )
        trade_taxes = []
        for item in self.trade_taxes:
            trade_taxes.append(

                ApplicableTradeTax(
                    calculated_amount=CalculatedAmount(item.tax_amount),
                    type_code=TypeCode(item.type_code),
                    basis_amount=BasisAmount(item.net_amount),
                    category_code=CategoryCode(item.category_code),
                    rate_applicable_percent=RateApplicablePercent(item.percent_rate),
                )


#                 ApplicableTradeTax.from_pure_pure_basic_trade_tax(
#                     net_amount=item.net_amount,
#                     tax_amount=item.tax_amount,
#                     percent_rate=item.percent_rate,
#                     category_code=item.category_code,
#                     type_code=item.type_code
#                 )
            )

        ApplicableHeaderTradeSettlement(
            invoice_currency_code=self.invoice_currency,
            applicable_trade_taxes=trade_taxes,
            specified_trade_settlement_header_monetary_summation=monetary_summation,
        ).render(node)
