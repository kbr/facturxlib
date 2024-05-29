"""
Some shorthand imports to set up a factur-x invoice with BASIC profile
are defined here.
"""

__version__ = "0.1.0-alpha"


# disable ruff "imported but unused" error
# ruff: noqa: F401


from .nodes.exchange import (
    ExchangedDocument,
    ExchangedDocumentContext,
)

from .facturx import build_invoice

from .transaction.basic import (
    PurePostalAdress,
    PureBasicTransAction,
    PureLineItem,
)
