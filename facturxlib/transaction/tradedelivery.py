"""
ApplicableHeaderTradeDelivery related nodes.
"""

from dataclasses import dataclass, field
from typing import Optional, Sequence


from ..nodes.common import (
    cii_node,
    ActualDeliverySupplyChainEvent,
    BaseTradeParty,
    ValueClass,
)

from ..nodes.documents import (
    ReferencedDocumentType_1,
    ReferencedDocumentType_2,
)


@cii_node("ram")
class DeliveryNoteReferencedDocument(ReferencedDocumentType_2):
    """
    Detailed information about the corresponding delivery note
    """


@cii_node("ram")
class DespatchAdviceReferencedDocument(ReferencedDocumentType_1):
    """
    Detailed information on the corresponding despatch advice
    """


@cii_node("qdt")
class ModeCode(ValueClass):
    """Delivery method (Code)"""


@dataclass
@cii_node("ram")
class SpecifiedLogisticsTransportMovement:
    """
    Detailed information about the delivery method

    required:
    `mode_code`: Delivery method (Code)
    """

    mode_code: ModeCode


@dataclass
@cii_node("ram")
class RelatedSupplyChainConsignment:
    """
    Detailed information on the consignment or dispatch

    optional:
    `specified_logistics_transport_movements`: Sequence of
            detailed information about the delivery method
    """

    specified_logistics_transport_movements: Optional[Sequence[SpecifiedLogisticsTransportMovement]] = field(
        default_factory=list
    )


@cii_node("ram")
class ReceivingAdviceReferencedDocument(ReferencedDocumentType_2):
    """
    Detailed information about the associated goods receipt
    """


@cii_node("ram")
class ShipFromTradeParty(BaseTradeParty):
    """
    Identification of the deviating sender
    """


@cii_node("ram")
class ShipToTradeParty(BaseTradeParty):
    """
    A group of business terms providing information about where and when
    the goods and services invoiced are delivered.
    """


@cii_node("ram")
class UltimateShipToTradeParty(BaseTradeParty):
    """
    Detailed information about the final recipient
    """


@dataclass
@cii_node("ram")
class ApplicableHeaderTradeDelivery:
    """
    Grouping of delivery details

    optional:
    `related_supply_chain_consignment`: Detailed information on the consignment or dispatch
    `ship_to_trade_party`: Delivery Information
    `ultimate_ship_to_trade_party`: Detailed information about the final recipient
    `ship_from_trade_party`: Identification of the deviating sender
    `actual_delivery_supply_chain_event`: Detailed information about the
            actual delivery ( in Germany mandatory if not given at line level)
    `despatch_advice_referenced_document`: Detailed information on the corresponding despatch advice
    `receiving_advice_referenced_document`: Detailed information about the associated goods receipt
    `delivery_note_referenced_document`: Detailed information about the corresponding delivery note
    """

    related_supply_chain_consignment: Optional[RelatedSupplyChainConsignment] = None
    ship_to_trade_party: Optional[ShipToTradeParty] = None
    ultimate_ship_to_trade_party: Optional[UltimateShipToTradeParty] = None
    ship_from_trade_party: Optional[ShipFromTradeParty] = None
    actual_delivery_supply_chain_event: Optional[ActualDeliverySupplyChainEvent] = None
    despatch_advice_referenced_document: Optional[DespatchAdviceReferencedDocument] = None
    receiving_advice_referenced_document: Optional[ReceivingAdviceReferencedDocument] = None
    delivery_note_referenced_document: Optional[DeliveryNoteReferencedDocument] = None
