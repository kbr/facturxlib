"""
ApplicableHeaderTradeAgreement related nodes.
"""

from dataclasses import dataclass

from ..common import (
    cii_node,
    BaseTradeParty,
)


@cii_node("ram")
class BuyerTradeParty(BaseTradeParty):
    """
    Detailed information about the seller (=service provider)
    """


@cii_node("ram")
class SellerTradeParty(BaseTradeParty):
    """Detailed information about the buyer (=recipient)."""


@dataclass
@cii_node("ram")
class ApplicableHeaderTradeAgreement:
    """
    Grouping of contract information
    """

    seller: SellerTradeParty
    buyer: BuyerTradeParty

    def render(self, parent):
        node = self.get_node(parent)
        for tag in self.__dict__.values():
            tag.render(node)
