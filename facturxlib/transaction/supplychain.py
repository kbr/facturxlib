#
#  this file is part of the factorxlib package
#  (c) 2024 Klaus Bremer
#
#  License: to be defined
#

from dataclasses import dataclass, field
from typing import Optional, Sequence

from ..nodes.common import cii_node
from .tradeagreement import ApplicableHeaderTradeAgreement
from .tradedelivery import ApplicableHeaderTradeDelivery
from .tradeline import IncludedSupplyChainTradeLineItem
from .tradesettlement import ApplicableHeaderTradeSettlement


@dataclass
@cii_node("rsm")
class SupplyChainTradeTransaction:
    """
    Root node for a factur-x invoice. Collects and renders all required subnodes.
    """

    applicable_header_trade_agreement: ApplicableHeaderTradeAgreement
    applicable_header_trade_delivery: ApplicableHeaderTradeDelivery
    applicable_header_trade_settlement: ApplicableHeaderTradeSettlement
    included_supply_chain_trade_line_items: Optional[Sequence[IncludedSupplyChainTradeLineItem]] = field(
        default_factory=list
    )

    _render_selection = """\
        included_supply_chain_trade_line_items
        applicable_header_trade_agreement
        applicable_header_trade_delivery
        applicable_header_trade_settlement
    """
