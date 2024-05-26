"""
Module for the SpecifiedLineTradeDelivery node.

"""

from dataclasses import dataclass
from typing import Optional

from facturxlib.nodes.cii import cii_node
from facturxlib.nodes.common import (
    ActualDeliverySupplyChainEvent,
    BilledQuantity,
    QuantityClass,
)

from facturxlib.nodes.documents import ReferencedDocumentType_5

from facturxlib.nodes.tradeparty import (
    ShipToTradeParty,
    UltimateShipToTradeParty,
)


@cii_node("ram")
class DespatchAdviceReferencedDocument(ReferencedDocumentType_5):
    """
    Detailed information on the corresponding despatch advice
    """


@cii_node("ram")
class ReceivingAdviceReferencedDocument(ReferencedDocumentType_5):
    """
    Detailed information on the corresponding goods receipt
    """


@cii_node("ram")
class DeliveryNoteReferencedDocument(ReferencedDocumentType_5):
    """
    Detailed information about the corresponding delivery note
    """


@cii_node("udt")
class ChargeFreeQuantity(QuantityClass):
    """
    Amount, without charge
    measurement unit as "unitCode" attribute.
    """


@cii_node("udt")
class PackageQuantity(QuantityClass):
    """
    Package quantity
    measurement unit as "unitCode" attribute.
    """


@dataclass
@cii_node("ram")
class SpecifiedLineTradeDelivery:
    """
    Grouping of delivery details on line level

    required:
    `billed_quantity`: Invoiced quantity

    optional:
    `charge_free_quantity`: Amount, without charge
    `package_quantity`: Package quantity
    `ship_to_trade_party`: Detailed information on the deviating goods recipient
    `ultimate_ship_to_trade_party`: Detailed information on the deviating final recipient
    `actual_delivery_supply_chain_event`: Detailed information about the actual delivery
    `despatch_advice_referenced_document`: Detailed information on the corresponding despatch advice
    `receiving_advice_referenced_document`: Detailed information on the corresponding goods receipt
    `delivery_note_referenced_document`: Detailed information about the corresponding delivery note
    """

    billed_quantity: BilledQuantity
    charge_free_quantity: Optional[ChargeFreeQuantity] = None
    package_quantity: Optional[PackageQuantity] = None
    ship_to_trade_party: Optional[ShipToTradeParty] = None
    ultimate_ship_to_trade_party: Optional[UltimateShipToTradeParty] = None
    actual_delivery_supply_chain_event: Optional[ActualDeliverySupplyChainEvent] = None
    despatch_advice_referenced_document: Optional[DespatchAdviceReferencedDocument] = None
    receiving_advice_referenced_document: Optional[ReceivingAdviceReferencedDocument] = None
    delivery_note_referenced_document: Optional[DeliveryNoteReferencedDocument] = None
