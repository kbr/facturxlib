"""
Some shorthand imports to set up a factur-x invoice with BASIC profile
are defined here.
"""

__version__ = "1.0"


# disable ruff "imported but unused" error
# ruff: noqa: F401


from .facturx import build_invoice
from .nodes.exchange import (
    ExchangedDocument,
    ExchangedDocumentContext,
)
from .transaction.basic import (
    PureBasicTransAction,
    PureLineItem,
    PurePostalAdress,
)
