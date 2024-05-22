"""
ApplicableHeaderTradeDelivery related nodes.
"""

from dataclasses import dataclass
# from typing import Optional, Sequence


from ..nodes.common import (
    cii_node,
    ActualDeliverySupplyChainEvent,
)


@dataclass
@cii_node("ram")
class ApplicableHeaderTradeDelivery:
    """Grouping of delivery details"""

    occurence_date: str

    def render(self, parent):
        node = self.get_node(parent)

        ActualDeliverySupplyChainEvent(self.occurence_date).render(node)
