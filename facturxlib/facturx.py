"""
EN16931-3-3 conform implementation to build a Factor-X invoice.

"""

import xml.etree.ElementTree as ET
from dataclasses import (
    dataclass,
    field,
)

from .exchange import (
    ExchangedDocument,
    ExchangedDocumentContext,
)
from .transaction.supplychain import TransAction


DEFAULT_XML_HEADER = "<?xml version='1.0' encoding='UTF-8' ?>"


@dataclass
class CrossIndustryInvoiceData:
    """
    Data container for the CII representation of an invoice.
    """

    transaction: TransAction
    exchanged_document: ExchangedDocument
    exchanged_document_context: ExchangedDocumentContext = field(default_factory=ExchangedDocumentContext)


class CrossIndustryInvoice:
    """
    Class to build a CII according to EN16931-3-3
    """

    def __init__(self, xml_header=DEFAULT_XML_HEADER):
        self.xml_header = xml_header
        self.node = ET.Element("rsm:CrossIndustryInvoice")
        self.node.set("xmlns:xs", "http://www.w3.org/2001/XMLSchema")
        self.node.set("xmlns:qdt", "urn:un:unece:uncefact:data:standard:QualifiedDataType:100")
        self.node.set("xmlns:udt", "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100")
        self.node.set("xmlns:rsm", "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100")
        self.node.set(
            "xmlns:ram",
            "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        )

    def render(self, invoice_data: CrossIndustryInvoiceData):
        """
        Renders a cross industry invoice with the given data.
        args is a namespace-like datastructure with the CII-schema data.
        """
        invoice_data.exchanged_document_context.render(self.node)
        invoice_data.exchanged_document.render(self.node)
        invoice_data.transaction.render(self.node)  # type: ignore[attr-defined]
        ET.indent(self.node)
        content = ET.tostring(self.node, encoding="unicode")
        if self.xml_header:
            return f"{self.xml_header}\n{content}"
        return content
