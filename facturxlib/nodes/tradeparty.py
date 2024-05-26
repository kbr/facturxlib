"""
Definition of all tradeparty types
"""

from dataclasses import dataclass, field
from typing import Optional, Sequence

from .cii import cii_node

from .common import (
    DefinedTradeContact,
    Description,
    ID,
    GlobalID,
    Name,
    PostalTradeAddress,
    SpecifiedLegalOrganization,
    SpecifiedTaxRegistration,
)


@dataclass
class BaseTradeParty:
    """
    Base implementation for all TradePartys
    Subclasses must apply the @cii_node decorator to make the
    `render`-method work.

    required:
    `name`: trade party name
    `postal_address`: instance of `PostalTradeAddress`.

    optional:
    `id`: deviating id
    `global_id`: deviating global id
    `description`: text node if further description is needed.
    `specified_tax_registration`
    """

    name: Name
    postal_address: PostalTradeAddress
    id: Optional[ID] = None
    global_id: Optional[GlobalID] = None
    description: Optional[Description] = None
    specified_legal_organization: Optional[SpecifiedLegalOrganization] = None
    defined_trade_contact: Optional[Sequence[DefinedTradeContact]] = field(default_factory=list)
    specified_tax_registration: Optional[SpecifiedTaxRegistration] = None


@cii_node("ram")
class BuyerAgentTradeParty(BaseTradeParty):
    """BuyerAgentTradeParty"""


@cii_node("ram")
class BuyerTaxRepresentativeTradeParty(BaseTradeParty):
    """Buyer tax representative party"""


@cii_node("ram")
class BuyerTradeParty(BaseTradeParty):
    """Detailed information about the buyer (=recipient)."""


@cii_node("ram")
class InvoicerTradeParty(BaseTradeParty):
    """InvoicerTradeParty"""


@cii_node("ram")
class InvoiceeTradeParty(BaseTradeParty):
    """Detailed information about the deviating invoice recipient"""


@cii_node("ram")
class PayeeTradeParty(BaseTradeParty):
    """Detailed contact information about the Payee"""


@cii_node("ram")
class PayerTradeParty(BaseTradeParty):
    """PayerTradeParty"""


@cii_node("ram")
class ProductEndUserTradeParty(BaseTradeParty):
    """Detailed information about the deviating end user."""


@cii_node("ram")
class SalesAgentTradeParty(BaseTradeParty):
    """SalesAgentTradeParty"""


@cii_node("ram")
class SellerTaxRepresentativeTradeParty(BaseTradeParty):
    """Seller tax representative party"""


@cii_node("ram")
class SellerTradeParty(BaseTradeParty):
    """
    Detailed information about the seller (=service provider)
    """


@cii_node("ram")
class ShipFromTradeParty(BaseTradeParty):
    """
    Identification of the deviating sender
    """


@cii_node("ram")
class ShipToTradeParty(BaseTradeParty):
    """
    Detailed information on the deviating goods recipient
    """


@cii_node("ram")
class UltimateShipToTradeParty(BaseTradeParty):
    """
    Detailed information about the final or deviating final recipient
    (see context specific domcumentation)
    """
