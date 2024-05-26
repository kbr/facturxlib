"""
Module for the AssociatedDocumentLineDocument node.

"""

from dataclasses import dataclass
from typing import Optional

from facturxlib.nodes.cii import cii_node
from facturxlib.nodes.common import (
    IncludedNote,
    LineID,
    LineStatusCode,
    LineStatusReasonCode,
    ParentLineID,
)


@dataclass
@cii_node("ram")
class AssociatedDocumentLineDocument:
    """
    Grouping of general position information.

    required:
    `line_id`: unambiguous identifier for the respective position
            within the invoice (the line number).

    optional:
    `parent_line_id`: Parent Line ID (just what the name says)
    `line_status_code`: Indicating whether an item includes the prices
            which must be taken into account when calculating the
            invoice amount, or whether it only contains information.
    `line_status_reason_code`: Complements the type to clarify whether
            the invoice item is one of the following:
                - Detail (default positioning)
                - Subtotal
                - Solely information
            When using the field LineStatusCode, the field
            LineStatusReasonCode must apply the following codes:
                - Detail
                - Aggregation
                - Information
    `included_note`: Detailed information about the free text of the line item.
    """

    line_id: LineID
    parent_line_id: Optional[ParentLineID] = None
    line_status_code: Optional[LineStatusCode] = None
    line_status_reason_code: Optional[LineStatusReasonCode] = None
    included_note: Optional[IncludedNote] = None

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""
        return cls(line_id=LineID(line.line_id))
