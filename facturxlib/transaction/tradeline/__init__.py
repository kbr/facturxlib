from dataclasses import dataclass

from facturxlib.nodes.common import (
    cii_node,
    BilledQuantity,
)


from .agreement import SpecifiedLineTradeAgreement
from .delivery import SpecifiedLineTradeDelivery
from .document import AssociatedDocumentLineDocument
from .product import SpecifiedTradeProduct
from .settlement import SpecifiedLineTradeSettlement


@dataclass
@cii_node("ram")
class IncludedSupplyChainTradeLineItem:
    """
    An aggregation of business terms containing information about
    individual invoice positions. For every position in the invoice
    there must be an IncludedSupplyChainTradeLineItem-node.
    """

    associated_document_line_document: AssociatedDocumentLineDocument
    specified_trade_product: SpecifiedTradeProduct
    specified_line_trade_agreement: SpecifiedLineTradeAgreement
    specified_line_trade_delivery: SpecifiedLineTradeDelivery
    specified_line_trade_settlement: SpecifiedLineTradeSettlement

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""
        return cls(
            associated_document_line_document=AssociatedDocumentLineDocument.from_basic_profile(line),
            specified_trade_product=SpecifiedTradeProduct.from_basic_profile(line),
            specified_line_trade_agreement=SpecifiedLineTradeAgreement.from_basic_profile(line),
            specified_line_trade_delivery=SpecifiedLineTradeDelivery(
                billed_quantity=BilledQuantity(line.billed_quantity, line.unit_code)
            ),
            specified_line_trade_settlement=SpecifiedLineTradeSettlement.from_basic_profile(line),
        )
