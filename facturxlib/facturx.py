"""
EN16931-3-3 conform implementation to build a Factor-X invoice.

"""

import xml.etree.ElementTree as ET
from dataclasses import (
    dataclass,
    field,
)

from .common import IncludedNote
from .exchange import (
    ExchangedDocument,
    ExchangedDocumentContext,
)


DEFAULT_XML_HEADER = "<?xml version='1.0' encoding='UTF-8' ?>"


@dataclass
class CrossIndustryInvoiceData:
    """
    Data container for the CII representation of an invoice.
    """

    exchanged_document: ExchangedDocument
    exchanged_document_context: ExchangedDocumentContext = field(default_factory=ExchangedDocumentContext)

    def __post_init__(self):
        pass


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
        ET.indent(self.node)
        content = ET.tostring(self.node, encoding="unicode")
        if self.xml_header:
            return f"{self.xml_header}\n{content}"
        return content


if __name__ == "__main__":
    # test data

    exchanged_document_context = ExchangedDocumentContext(
        indicator="false",
        business_process_id="A1",
    )
    exchanged_document = ExchangedDocument(
        invoice_id="010/2024",
        issue_date="20240510",
        included_note=IncludedNote(content="Late Shipping"),
    )

    invoice_data = CrossIndustryInvoiceData(
        exchanged_document_context=exchanged_document_context,
        exchanged_document=exchanged_document,
    )
    # test call
    cii = CrossIndustryInvoice()
    xml_data = cii.render(invoice_data)
    print()
    print(xml_data)
    print()
