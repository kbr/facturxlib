#
#  this file is part of the factorxlib package
#  (c) 2024 Klaus Bremer
#
#  License: to be defined
#
"""
Definition of all tradeparty types
"""

from dataclasses import dataclass, field
from typing import Optional, Sequence

from .cii import cii_node
from .common import (
    ID,
    DefinedTradeContact,
    Description,
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

    required:
    `name`: trade party name
    `postal_address`: instance of `PostalTradeAddress`.

    optional:
    `id`: deviating id
    `global_id`: deviating global id
    `description`: text node if further description is needed.
    `specified_tax_registration`: VAT ID or local Tax ID
    """

    name: Name
    postal_address: PostalTradeAddress
    id: Optional[ID] = None
    global_id: Optional[GlobalID] = None
    description: Optional[Description] = None
    specified_legal_organization: Optional[SpecifiedLegalOrganization] = None
    defined_trade_contact: Optional[Sequence[DefinedTradeContact]] = field(default_factory=list)
    specified_tax_registration: Optional[SpecifiedTaxRegistration] = None

    @classmethod
    def from_basic_trade_party(cls, basic_trade_party):
        """
        Returns an instance initialized with the data from a
        `BasicTradeParty` instance. This class is defined in
        `facturxlib.basic`.
        """
        id = basic_trade_party.identifier
        if not id:
            id = None  # replace boolean False with None
        specified_tax_registration = None
        if basic_trade_party.specified_tax_registration and basic_trade_party.specified_tax_registration_scheme:
            specified_tax_registration = SpecifiedTaxRegistration(
                value=basic_trade_party.specified_tax_registration,
                scheme_id=basic_trade_party.specified_tax_registration_scheme,
            )

        return cls(
            name=Name(basic_trade_party.name),
            postal_address=PostalTradeAddress.from_basic_trade_party(basic_trade_party),
            id=id,
            defined_trade_contact=[DefinedTradeContact.from_basic_trade_party(basic_trade_party)],
            specified_tax_registration=specified_tax_registration,
        )


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
