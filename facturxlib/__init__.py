"""
this is the scr package with the module facturx.py as entry-point.

The CII-tags are implemented as classes and dataclasses.
Some tags with same names do not have the same set of enlosed tags or cardinality. To avoid confusion and because the amount of classes, the package is structured into further sub-packages. The long names are representing sequence-tags, for better handling the __init__.py modules are providing shordhand imports:

    - common
    - supplychaintradelineitems
        - document
        - product

"""

__version__ = "0.1.0-alpha"


# disable ruff "imported but unused" error
# ruff: noqa: F401

from .common import (
    CopyIndicator,
    IncludedNote,
)

from .exchange import (
    ExchangedDocument,
    ExchangedDocumentContext,
)

from .facturx import (
    CrossIndustryInvoice,
    CrossIndustryInvoiceData,
)

from .transaction.supplychain import (
    SupplyChainTradeTransAction,
    PurePostalAdress,
    PureBasicTransAction,
    PureLineItem,
)

# from .transaction.tradeagreement import (
#     SellerTradeParty,
# )
