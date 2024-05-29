from dataclasses import dataclass, field
from typing import Optional, Sequence


from ..nodes.common import cii_node
from .tradeagreement import ApplicableHeaderTradeAgreement
from .tradedelivery import ApplicableHeaderTradeDelivery
from .tradeline import IncludedSupplyChainTradeLineItem
from .tradesettlement import ApplicableHeaderTradeSettlement


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

    _render_selection = """\
        line_items
        applicable_header_trade_agreement
        applicable_header_trade_delivery
        applicable_header_trade_settlement
    """
