"""
Module for the SpecifiedTradeProduct node.

"""

from dataclasses import dataclass, field
from typing import Optional, Sequence

from facturxlib.nodes.common import (
    cii_node,
    Description,
    GlobalID,
    ID,
    Name,
    QuantityClass,
    TypeCode,
    ValueClass,
)


@cii_node("udt")
class BuyerAssignedID(ValueClass):
    """Buyer item number"""


@cii_node("udt")
class SellerAssignedID(ValueClass):
    """Seller item number"""


@cii_node("udt")
class IndustryAssignedID(ValueClass):
    """Industry item number"""


@cii_node("udt")
class Value(ValueClass):
    """Item Attribute Value"""


@cii_node("udt")
class UnitQuantity(QuantityClass):
    """
    Included amount with an optional
    measurement unit as "unitCode" attribute.
    """


@cii_node("udt")
class ValueMeasure(QuantityClass):
    """
    Item Attribute Value (numerical measurand) with an optional
    measurement unit as "unitCode" attribute.
    """


@dataclass
@cii_node("ram")
class ApplicableProductCharacteristic:
    """
    Detailinformation about product properties.

    required:
    `description`: The name of a product’s attribute or property i.e. like „colour“
    `value`: The value of the attribute or the property of the item i.e. „Red“

    optional:
    `type_code`: Item Attribute Type (Code)
    `value_measure`: Item Attribute Value (numerical measurand) with an
            optional Measurement Unit as "unitCode" attribute.
    ``
    """

    description: Description
    value: Value
    type_code: Optional[TypeCode] = None
    value_measure: Optional[ValueMeasure] = None


@cii_node("udt")
class ClassCode(ValueClass):
    """
    A code for the classification of an item according to type or kind or nature.
    """

    def __init__(self, value, list_id=None, list_version_id=None):
        super().__init__(value)
        self._node_attributes = {
            "listID": list_id,
            "listVersionID": list_version_id,
        }


@cii_node("udt")
class ClassName(ValueClass):
    """Classification name"""


@dataclass
@cii_node("ram")
class DesignatedProductClassification:
    """
    Detailed information on the item classification.

    optional:
    `class_code`: A code for the classification of an item according
            to type or kind or nature.
    `class_name`: Classification name.
    """

    class_code: Optional[ClassCode] = None
    class_name: Optional[ClassName] = None


@cii_node("udt")
class BatchID(ValueClass):
    """batch id"""


@cii_node("udt")
class SupplierAssignedSerialID(ValueClass):
    """supplier assigned serial id"""


@dataclass
@cii_node("ram")
class IndividualTradeProductInstance:
    """IndividualTradeProductInstance"""

    batch_id: Optional[BatchID] = None
    supplier_assigned_serial_id: Optional[SupplierAssignedSerialID] = None


@dataclass
@cii_node("ram")
class OriginTradeCountry:
    """
    Detailed information on the item origin.

    `id`: The code specifying the product’s country of origin
    """

    id: Optional[ID] = None


@dataclass
@cii_node("ram")
class IncludedReferencedProduct:
    """
    Detailed information on the included items.

    required:
    `name`: item name

    optional:
    `id`: sequence of ids
    `global_id`: sequence of global item id and scheme identifier
    `seller_assigned_id`: An identification of the item assigned by the seller
    `buyer_assigned_id`: An identification of the item assigned by the buyer
    `industry_assigned_id`: An industry assigned identification number
    `description`: Item description
    """

    name: Name
    id: Optional[Sequence[ID]] = field(default_factory=list)
    global_id: Optional[Sequence] = field(default_factory=list)
    seller_assigned_id: Optional[SellerAssignedID] = None
    buyer_assigned_id: Optional[BuyerAssignedID] = None
    industry_assigned_id: Optional[IndustryAssignedID] = None
    description: Optional[Description] = None
    unit_quantity: Optional[UnitQuantity] = None


@dataclass
@cii_node("ram")
class SpecifiedTradeProduct:
    """
    Item information:
    Aggregation of information about the product or the service provided

    required:
    `name`: an articles name

    optional:
    `id`: not further specified product id
    `global_id`: The identification of articles based on a registered scheme
    `seller_assigned_id`: An identification of the item assigned by the seller
    `buyer_assigned_id`: An identification of the item assigned by the buyer
    `description`: more detailed description of an item
    `applicable_product_characteritics`: Sequence of product properties.
    `designated_product_classifications`: Sequence of detailed information
            on the item classification.
    `individual_trade_product_instances`: batch- and serial-ids
    `included_referenced_product`: Detailed information on the included items
    """

    name: Name
    id: Optional[ID] = None
    global_id: Optional[GlobalID] = None
    seller_assigned_id: Optional[SellerAssignedID] = None
    buyer_assigned_id: Optional[BuyerAssignedID] = None
    description: Optional[Description] = None
    applicable_product_characteritics: Optional[Sequence[ApplicableProductCharacteristic]] = field(default_factory=list)
    designated_product_classifications: Optional[Sequence[DesignatedProductClassification]] = field(
        default_factory=list
    )
    individual_trade_product_instances: Optional[Sequence[IndividualTradeProductInstance]] = field(default_factory=list)
    origin_trade_country: Optional[OriginTradeCountry] = None
    included_referenced_product: Optional[IncludedReferencedProduct] = None

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""
        return cls(name=Name(line.name))
