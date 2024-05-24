"""
Implementation for the IncludedSupplyChainTradeLineItem node.
The direct subnodes are:

    - AssociatedDocumentLineDocument
    - SpecifiedTradeProduct
    - SpecifiedLineTradeAgreement
    - SpecifiedLineTradeDelivery
    - SpecifiedLineTradeSettlement
    - SpecifiedTradeAllowanceCharge
    - SpecifiedTradeSettlementLineMonetarySummation
    - InvoiceReferencedDocument
    - AdditionalReferencedDocument
    - ReceivableSpecifiedTradeAccountingAccount

"""

from dataclasses import dataclass, field
from typing import Optional, Sequence

from ..nodes.common import (
    cii_node,
    ActualDeliverySupplyChainEvent,
    ActualAmount,
    AllowanceTotalAmount,
    BaseTradeParty,
    BasisAmount,
    BasisQuantity,
    BilledQuantity,
    BillingSpecifiedPeriodBase,
    CalculatedAmount,
    CalculationPercent,
    CategoryCode,
    ChargeAmount,
    ChargeTotalAmount,
    ChargeIndicator,
    Description,
    ExemptionReason,
    ExemptionReasonCode,
    GlobalID,
    GrandTotalAmount,
    ID,
    IncludedNote,
    IncludedTradeTax,
    LineID,
    LineStatusCode,
    LineStatusReasonCode,
    LineTotalAmount,
    Name,
    ParentLineID,
    QuantityClass,
    Reason,
    ReasonCode,
    RateApplicablePercent,
    ReceivableSpecifiedTradeAccountingAccount,
    TaxTotalAmount,
    TypeCode,
    ValueClass,
)

from ..nodes.documents import (
    ReferencedDocumentType_1,
    ReferencedDocumentType_3,
    ReferencedDocumentType_4,
    ReferencedDocumentType_5,
    ReferencedDocumentType_8,
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


# ==========================================================================
# SpecifiedTradeProduct: specific node and subnodes
#


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
class ChargeFreeQuantity(QuantityClass):
    """
    Amount, without charge
    measurement unit as "unitCode" attribute.
    """


@cii_node("udt")
class PackageQuantity(QuantityClass):
    """
    Package quantity
    measurement unit as "unitCode" attribute.
    """


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


# ==========================================================================
# SpecifiedLineTradeAgreement: specific node and subnodes
#


@cii_node("ram")
class BuyerOrderReferencedDocument(ReferencedDocumentType_1):
    """Details of the associated order"""


@cii_node("ram")
class QuotationReferencedDocument(ReferencedDocumentType_1):
    """QuotationReferencedDocument"""


@cii_node("ram")
class ContractReferencedDocument(ReferencedDocumentType_5):
    """Detailed information on the associated contract"""


@cii_node("ram")
class AdditionalReferencedDocument(ReferencedDocumentType_8):
    """Details of an additional document reference"""


@cii_node("ram")
class UltimateCustomerOrderReferencedDocument(ReferencedDocumentType_5):
    """Details of an additional document reference"""


@dataclass
@cii_node("ram")
class AppliedTradeAllowanceCharge:
    """
    Detailed information on discounts and charges.
    required:
    `actual_amount`: The total discount substracted from the gross price
            which leads to the net price.
    optional:
    `charge_indicator`: Switch for charges and discounts.
    `basis_amount`: Discount / Charge base amount
    `reason_code`: Reason for allowance or charge (Code)
    `reason`: Reason for the charge/discount (free text)
    """

    actual_amount: ActualAmount
    charge_indicator: Optional[ChargeIndicator] = None
    calculation_percent: Optional[CalculationPercent] = None
    basis_amount: Optional[BasisAmount] = None
    reason_code: Optional[ReasonCode] = None
    reason: Optional[Reason] = None


@dataclass
@cii_node("ram")
class GrossPriceProductTradePrice:
    """
    Detailed information on the gross price of the item.

    required:
    `charge_amount`: item gross price

    optional:
    `basis_quantity`: item base quantity and optional unit_code
    `applied_trade_allowance_charges`: Detailed information on discounts and charges.
    """

    charge_amount: ChargeAmount
    basis_quantity: Optional[BasisQuantity] = None
    applied_trade_allowance_charges: Optional[Sequence[AppliedTradeAllowanceCharge]] = field(default_factory=list)


@dataclass
@cii_node("ram")
class NetPriceProductTradePrice:
    """
    Detailed information on the net price of the item.
    The net price includes all surchages and discounts, except for VAT.

    required:
    `charge_amount`: item net price

    optional:
    `basis_quantity`: item base quantity and optional unit_code
    `included_trade_tax`: Included tax for B2C
    """

    charge_amount: ChargeAmount
    basis_quantity: Optional[BasisQuantity] = None
    included_trade_tax: Optional[IncludedTradeTax] = None

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""
        if line.basis_quantity:
            basis_quantity = BasisQuantity(line.basis_quantity, line.unit_code)
        else:
            basis_quantity = None
        return cls(charge_amount=ChargeAmount(line.charge_amount), basis_quantity=basis_quantity)


@dataclass
@cii_node("ram")
class SpecifiedLineTradeAgreement:
    """
    Detailed information on the price.
    Aggregation of the contract information at line level

    required:
    `net_product_trade_price`: Detailed information on the net price of the item.

    optional:
    `buyer_order_referenced_document`: Details of the associated order
    `quotation_referenced_document`: QuotationReferencedDocument
    `contract_referenced_document`: Detailed information on the associated contract
    `additional_referenced_documents`: Sequence of details of an additional document reference
    `ultimate_customer_order_referenced_document`: Sequence of UltimateCustomerOrderReferencedDocument
    """

    net_product_trade_price: NetPriceProductTradePrice
    buyer_order_referenced_document: Optional[BuyerOrderReferencedDocument] = None
    quotation_referenced_document: Optional[QuotationReferencedDocument] = None
    contract_referenced_document: Optional[ContractReferencedDocument] = None
    additional_referenced_documents: Optional[Sequence[AdditionalReferencedDocument]] = field(default_factory=list)
    ultimate_customer_order_referenced_document: Optional[Sequence[UltimateCustomerOrderReferencedDocument]] = field(
        default_factory=list
    )

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""
        return cls(net_product_trade_price=NetPriceProductTradePrice.from_basic_profile(line))


# ==========================================================================
# SpecifiedLineTradeDelivery: specific node and subnodes
#


@cii_node("ram")
class ShipToTradeParty(BaseTradeParty):
    """
    Detailed information on the deviating goods recipient
    """


@cii_node("ram")
class UltimateShipToTradeParty(BaseTradeParty):
    """
    Detailed information on the deviating final recipient
    """


@cii_node("ram")
class DespatchAdviceReferencedDocument(ReferencedDocumentType_5):
    """
    Detailed information on the corresponding despatch advice
    """


@cii_node("ram")
class ReceivingAdviceReferencedDocument(ReferencedDocumentType_5):
    """
    Detailed information on the corresponding goods receipt
    """


@cii_node("ram")
class DeliveryNoteReferencedDocument(ReferencedDocumentType_5):
    """
    Detailed information about the corresponding delivery note
    """


@dataclass
@cii_node("ram")
class SpecifiedLineTradeDelivery:
    """
    Grouping of delivery details on line level

    required:
    `billed_quantity`: Invoiced quantity

    optional:
    `charge_free_quantity`: Amount, without charge
    `package_quantity`: Package quantity
    `ship_to_trade_party`: Detailed information on the deviating goods recipient
    `ultimate_ship_to_trade_party`: Detailed information on the deviating final recipient
    `actual_delivery_supply_chain_event`: Detailed information about the actual delivery
    `despatch_advice_referenced_document`: Detailed information on the corresponding despatch advice
    `receiving_advice_referenced_document`: Detailed information on the corresponding goods receipt
    `delivery_note_referenced_document`: Detailed information about the corresponding delivery note
    """

    billed_quantity: BilledQuantity
    charge_free_quantity: Optional[ChargeFreeQuantity] = None
    package_quantity: Optional[PackageQuantity] = None
    ship_to_trade_party: Optional[ShipToTradeParty] = None
    ultimate_ship_to_trade_party: Optional[UltimateShipToTradeParty] = None
    actual_delivery_supply_chain_event: Optional[ActualDeliverySupplyChainEvent] = None
    despatch_advice_referenced_document: Optional[DespatchAdviceReferencedDocument] = None
    receiving_advice_referenced_document: Optional[ReceivingAdviceReferencedDocument] = None
    delivery_note_referenced_document: Optional[DeliveryNoteReferencedDocument] = None


# ==========================================================================
# SpecifiedLineTradeSettlement: specific node and subnodes
#


@cii_node("udt")
class TotalAllowanceChargeAmount(ValueClass):
    """
    Total amount of allowances / charges
    """


@dataclass
@cii_node("ram")
class SpecifiedTradeSettlementLineMonetarySummation:
    """
    Detailed information about item totals

    required:
    `line_total_amount`: Invoice line net amount

    optional:
    `charge_total_amount`: ChargeTotalAmount
    `allowance_total_amount`: AllowanceTotalAmount
    `tax_total_amount`: TaxTotalAmount
    `grand_total_amount`: GrandTotalAmount
    `total_allowance_charge_amount`: Total amount of allowances / charges
    """

    line_total_amount: LineTotalAmount
    charge_total_amount: Optional[ChargeTotalAmount] = None
    allowance_total_amount: Optional[AllowanceTotalAmount] = None
    tax_total_amount: Optional[TaxTotalAmount] = None
    grand_total_amount: Optional[GrandTotalAmount] = None
    total_allowance_charge_amount: Optional[TotalAllowanceChargeAmount] = None

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""
        return cls(line_total_amount=LineTotalAmount(line.line_total_amount))



@dataclass
@cii_node("ram")
class ApplicableTradeTax:
    """
    Line VAT information. A group of business definitions which contain
    information about VAT and apply to the invoice line items for goods
    and services on the invoice. This section must be used even in the
    BASIC profile, if the invoice needs to show more than one tax type.

    required:
    `type_code`: required, but fixed to "VAT"

    optional:
    `calculated_amount`: optional but required if different VATs are used
            in a single invoice.
    `category_code`: required, defaults to standard rate "S"
    `rate_applicable_percent`: optional tax percentage, but should be used
            at least when `calculated_amount` is required.
    `exemption_reason`: VAT exemption reason (free text)
    """

    calculated_amount: Optional[CalculatedAmount] = None  # Note: can be required
    category_code: CategoryCode = CategoryCode("S")  # required with default of "S"
    type_code: TypeCode = TypeCode("VAT")
    rate_applicable_percent: Optional[RateApplicablePercent] = None
    exemption_reason: Optional[ExemptionReason] = None
    exemption_reason_code: Optional[ExemptionReasonCode] = None

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""
        return cls(
            calculated_amount=CalculatedAmount(line.calculated_amount),
            category_code=CategoryCode(line.category_code),
            type_code=TypeCode(line.type_code),
            rate_applicable_percent=RateApplicablePercent(line.rate_applicable_percent),
        )


@cii_node("ram")
class BillingSpecifiedPeriod(BillingSpecifiedPeriodBase):
    """
    Invoice line billing period
    """



@dataclass
@cii_node("ram")
class SpecifiedTradeAllowanceCharge:
    """
    Details on allowances and charges on line level. A group of business
    terms providing information about the applicable discounts on the
    invoice line item. Details on surcharges and discounts.

    required:
    `actual_amount`: The amount of the discount / surcharge or discount without VAT

    optional:
    `charge_indicator`: Charges and Allowances line Indicator (boolean)
            In case of a discount (BG-27) the value of the
            ChargeIndicators has to be "false". In case of a surcharge
            (BG-28) the value of the ChargeIndicators has to be "true".
    `calculation_percent`: Discount / surcharge in percentage
    `basis_amount`: Base amount for the discount / surcharge
    `reason_code`: The invoice line discount / surcharge reason code
    `reason`: Discount or surcharge reason (free text)
    """

    actual_amount: ActualAmount
    charge_indicator: Optional[ChargeIndicator] = None
    calculation_percent: Optional[CalculationPercent] = None
    basis_amount: Optional[BasisAmount] = None
    reason_code: Optional[ReasonCode] = None
    reason: Optional[Reason] = None



@cii_node("ram")
class InvoiceReferencedDocument(ReferencedDocumentType_4):
    """
    No further description.
    """

@cii_node("ram")
class AdditionalReferencedDocumentTyp3(ReferencedDocumentType_3):
    """
    Object identifier at the invoice item level.
    Renamed as AdditionalReferencedDocumentTyp3 to avoid nameclashing
    """

    _tag_name = "AdditionalReferencedDocument"  # TODO: refactor module in subpackage




@dataclass
@cii_node("ram")
class SpecifiedLineTradeSettlement:
    """
    Grouping of billing information at line level

    required:
    `applicable_trade_tax`: Line VAT information
    `specified_trade_settlement_line_monetary_summation`:
            Detailed information about item totals

    optional:
    `billing_specified_period`: Invoice line billing period
    `specified_trade_allowance_charge`: Details on allowances and charges
            on line level
    `invoice_referenced_document`: InvoiceReferencedDocument
    `additional_referenced_documents`: Sequence of Object identifier at
            the invoice item level
    `receivable_specific_trade_accounting_accounts`: Sequence of Detailed
            information on the accounting reference
    """

    applicable_trade_tax: ApplicableTradeTax
    specified_trade_settlement_line_monetary_summation: SpecifiedTradeSettlementLineMonetarySummation
    billing_specified_period: Optional[BillingSpecifiedPeriod] = None
    specified_trade_allowance_charge: Optional[Sequence[SpecifiedTradeAllowanceCharge]] = field(default_factory=list)
    invoice_referenced_document: Optional[InvoiceReferencedDocument] = None
    additional_referenced_documents: Optional[Sequence[AdditionalReferencedDocumentTyp3]] = field(default_factory=list)
    receivable_specific_trade_accounting_accounts: Optional[Sequence[ReceivableSpecifiedTradeAccountingAccount]] = field(default_factory=list)

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""

        return cls(
            applicable_trade_tax=ApplicableTradeTax.from_basic_profile(line),
            specified_trade_settlement_line_monetary_summation=(
                SpecifiedTradeSettlementLineMonetarySummation.from_basic_profile(line)
            ),
        )



# ==========================================================================
# IncludedSupplyChainTradeLineItem:
# the parent node for all trade line subnodes
#


@dataclass
@cii_node("ram")
class IncludedSupplyChainTradeLineItem:
    """
    An aggregation of business terms containing information about
    individual invoice positions. For every position in the invoice
    there must be an IncludedSupplyChainTradeLineItem-node.
    """

    associated_document_line_document: AssociatedDocumentLineDocument
    specified_trade_product: SpecifiedTradeProduct
    specified_line_trade_agreement: SpecifiedLineTradeAgreement
    specified_line_trade_delivery: SpecifiedLineTradeDelivery
    specified_line_trade_settlement: SpecifiedLineTradeSettlement

    @classmethod
    def from_basic_profile(cls, line):
        """line is a `supplychain.PureLineItem` instance."""
        return cls(
            associated_document_line_document=AssociatedDocumentLineDocument.from_basic_profile(line),
            specified_trade_product=SpecifiedTradeProduct.from_basic_profile(line),
            specified_line_trade_agreement=SpecifiedLineTradeAgreement.from_basic_profile(line),
            specified_line_trade_delivery=SpecifiedLineTradeDelivery(
                billed_quantity=BilledQuantity(line.billed_quantity, line.unit_code)
            ),
            specified_line_trade_settlement=SpecifiedLineTradeSettlement.from_basic_profile(line),
        )
