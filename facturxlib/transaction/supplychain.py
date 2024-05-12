from dataclasses import dataclass
from typing import Optional


from ..common import (
    cii_node,
    Name,
    PostalTradeAddress,
    SpecifiedTaxRegistration,
)

from .tradeagreement import (
    ApplicableHeaderTradeAgreement,
    BuyerTradeParty,
    SellerTradeParty,
)

from .tradedelivery import (
    ApplicableHeaderTradeDelivery,
)
from .tradesettlement import (
    ApplicableHeaderTradeSettlement,
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
    Adapter class for the a TradeParty with address. Allows to provide
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
class PureBasicTransAction(TransAction):
    """
    Provides the transaction interface. Required arguments are for the
    nodes of the BASIC profile with a cardinality of at least 1. With
    the additional `lines` argument basic invoices can get created.

    `net_total`: invoice total net price ("#.00")
    `tax_total`: invoice total taxes ("#.00")
    `grand_total`: invoice total (sum of `net_total` and `tax_total`)("#.00")

    optional:
    `invoice_currency`: defaults to "EUR"
    `lines`: sequence of `IncludedSupplyChainTradeLineItem` instances (the sold items).
    `occurence_date`: if given a datetime string of format CCYYMMDD
                      This date is optional by the profile but mandatory in germany
    """

    net_total: str
    tax_total: str
    grand_total: str
    seller: PurePostalAdress
    buyer: PurePostalAdress
    invoice_currency: str = "EUR"
    occurence_date: Optional[str] = None  # optional but mandatory in germany

    #     lines: Optional[Sequence[IncludedSupplyChainTradeLineItem]] = field(default_factory=list)

    def render(self, parent):
        node = self.get_node(parent)

        seller = SellerTradeParty(
            name=Name(self.seller.name), postal_address=PostalTradeAddress.from_pure_postal_address(self.seller),
            specified_tax_registration=SpecifiedTaxRegistration(self.seller.vat, "VAT")
        )
        buyer = BuyerTradeParty(
            name=Name(self.buyer.name), postal_address=PostalTradeAddress.from_pure_postal_address(self.buyer),             specified_tax_registration=SpecifiedTaxRegistration(self.buyer.vat, "VAT")

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
        ApplicableHeaderTradeSettlement(
            invoice_currency_code=self.invoice_currency,
            specified_trade_settlement_header_monetary_summation=monetary_summation,
        ).render(node)
