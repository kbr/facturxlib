from dataclasses import dataclass, field
from typing import Optional, Sequence


from ..common import cii_node
from .tradeagreement import ApplicableHeaderTradeAgreement
from .tradedelivery import ApplicableHeaderTradeDelivery
from .tradeline import IncludedSupplyChainTradeLineItem
from .tradesettlement import ApplicableHeaderTradeSettlement


# @cii_node("ram")
# class TransAction:
#     _tag_name = "SupplyChainTradeTransAction"
#


@dataclass
@cii_node("ram")
class SupplyChainTradeTransAction:
    """
    Provides the transaction interface. Required arguments are for the
    nodes of the BASIC profile with a cardinality of at least 1. With
    the additional `lines` argument basic invoices can get created.

    `net_total`: invoice total net price ("#.00")
    `tax_total`: invoice total taxes ("#.00")
    `grand_total`: invoice total (sum of `net_total` and `tax_total`)("#.00")
    `lines`: sequence of `IncludedSupplyChainTradeLineItem` instances (the sold items).
    """

    applicable_header_trade_agreement: ApplicableHeaderTradeAgreement
    applicable_header_trade_delivery: ApplicableHeaderTradeDelivery
    applicable_header_trade_settlement: ApplicableHeaderTradeSettlement
    line_items: Optional[Sequence[IncludedSupplyChainTradeLineItem]] = field(default_factory=list)

    def render(self, parent):
        """
        Overload the render method because in the order of nodes the
        line-items should come first and are not renderable as a list.
        """
        node = self.get_node(parent)
        for line_item in self.line_items:
            line_item.render(node)
        self.applicable_header_trade_agreement.render(node)
        self.applicable_header_trade_delivery.render(node)
        self.applicable_header_trade_settlement.render(node)
