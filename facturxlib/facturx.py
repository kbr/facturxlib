#
#  this file is part of the factorxlib package
#  (c) 2024 Klaus Bremer
#
#  License: to be defined
#
"""
EN16931-3-3 conform implementation to build a Factor-X invoice.

"""

import xml.etree.ElementTree as ET
from dataclasses import dataclass

from .nodes.exchange import (
    ExchangedDocument,
    ExchangedDocumentContext,
)
from .transaction.supplychain import SupplyChainTradeTransaction

DEFAULT_XML_HEADER = "<?xml version='1.0' encoding='UTF-8' ?>"


@dataclass
class CrossIndustryInvoice:
    """
    Class to build an invoice according to EN16931-3-3

    required:
    `exchanged_document_context`:  Process Control
    `exchanged_document`: Grouping of characteristics that affect the entire document
    `supply_chain_trade_transaction`: Grouping of information about the business transaction
    """

    exchanged_document_context: ExchangedDocumentContext
    exchanged_document: ExchangedDocument
    supply_chain_trade_transaction: SupplyChainTradeTransaction

    _node_attributes = {
        "xmlns:xs": "http://www.w3.org/2001/XMLSchema",
        "xmlns:qdt": "urn:un:unece:uncefact:data:standard:QualifiedDataType:100",
        "xmlns:udt": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
        "xmlns:rsm": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
        "xmlns:ram": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
    }

    def render(self, xml_header=DEFAULT_XML_HEADER):
        """
        Render the root-node. Because there is no parent the magic of
        cii_node is not avilable.
        Returns a string with the invoice as xml according to EN16931-3-3.
        """
        root_node = ET.Element(f"rsm:{self.__class__.__name__}")
        for attribute, value in self._node_attributes.items():
            root_node.set(attribute, value)
        for group in (self.exchanged_document_context, self.exchanged_document, self.supply_chain_trade_transaction):
            group.render(root_node)
        ET.indent(root_node)
        content = ET.tostring(root_node, encoding="unicode")
        if xml_header:
            return f"{xml_header}\n{content}"
        return content


def build_invoice(
    exchanged_document_context: ExchangedDocumentContext,
    exchanged_document: ExchangedDocument,
    supply_chain_trade_transaction: SupplyChainTradeTransaction,
    xml_header=DEFAULT_XML_HEADER,
):
    """
    Convenience wrapper to instanciate CrossIndustryInvoice and return
    the rendered invoice as xml-string.

    required:
    `exchanged_document_context`:  Process Control
    `exchanged_document`: Grouping of characteristics that affect the entire document
    `supply_chain_trade_transaction`: Grouping of information about the business transaction

    optional:
    `xml_header`: the header to use for the invoice.
            Defaults to "<?xml version='1.0' encoding='UTF-8' ?>"
    """
    cii = CrossIndustryInvoice(
        exchanged_document_context=exchanged_document_context,
        exchanged_document=exchanged_document,
        supply_chain_trade_transaction=supply_chain_trade_transaction,
    )
    return cii.render(xml_header=xml_header)
