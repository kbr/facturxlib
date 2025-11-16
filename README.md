# facturxlib

Library to create e-invoices according to the factur-x specification 1.01.06 (and also ZUGFeRD 2.2 without the pdf-representation). The library provides the buildung blocks to create a Cross Industry Invoice (CII or e-invoice) according to EN16931-3-3 and provide the resulting data as XML.

Information about the structur and the documentation of this format as well as schematron-data (for output validation) are available here `https://fnfe-mpe.org/factur-x/factur-x_en/` and here `https://www.ferd-net.de/standards/zugferd-2.2/zugferd-2.2.html`.

The format is based on XML-Nodes. The library supports all nodes that are required to build an e-invoice according to the EXTENDED profile. For convenience there is an API to support the BASIC profile with all required and optional arguments.

For the common usecase to just provide the seller- and buyer-addresses and a list of sold items with a common tax-rate, the class `MinimalInvoice` can simplifiy the creation of an e-invoice even more.


## Installation and Dependencies

Install can be done by pip: `pip install facturxlib`.

The `facturxlib` library has no dependencies beside the Python standard-library.


## Example

The following example shows how to create an e-invoice with a minimal required dataset. It consist of a seller- and buyer-address and a list of sold items, all with the same tax rate.

(All data are fictional and provided as strings, including numerical values. This is because the library takes all data "as is" and makes no calculations. The input-data are exactly the output-data.)

```
# import the required classes:
from facturxlib.basic import (
    BasicLineItem,
    BasicTradeParty,
    MinimalInvoice,
    MinimalInvoiceHeader,
    MinimalInvoiceTotal,
)


# provide the seller address:
seller = BasicTradeParty(
    name="Seller Company",
    line_one="Trade Street 42",
    postcode="40123",
    city_name="Düsseldorf",  # mind the umlaut (it works)
    country_id="DE",
    phone="+49 211 0123456789",
    email="seller@example.com",
    specified_tax_registration="DE 12 345 678",
    specified_tax_registration_scheme="VA"
)


# provide the buyer address:
buyer = BasicTradeParty(
    name="Buyer GmbH & Co KG",
    line_one="Buyer Lane 1",
    postcode="21614",
    city_name="Buxtehude",
    country_id="DE",
    identifier="10423"  # this is a seller-defined customer number
)


# provide the header with a unique invoice number, the invoice date
# and date of delivery which is optional by the profile-definition
# but mandatory in Germany (date-format: CCYYMMDD):
header = MinimalInvoiceHeader(
    invoice_id = "123/2024",
    invoice_issue_date = "20240502",
    delivery_occurence_date = "20240430",
)


# build a list of items sold to the buyer.
# `line_id` is an incrementing position number starting at 1.
basic_line_items = [
    BasicLineItem.from_minimal_data(
        line_id="1",
        name="Power Supply 800 Watt",
        charge_amount="247.90",
    ),
    BasicLineItem.from_minimal_data(
        line_id="2",
        name="Cable set type M",
        charge_amount="16.39",
    ),
    BasicLineItem.from_minimal_data(
        line_id="3",
        name="Fuse 10 Ampere",
        charge_amount="3.78",
    )
]


# sum the totals and provide the `due_date` as this is required
# if the `grand_total_amount` is larger than 0.
total = MinimalInvoiceTotal(
    line_total_amount="268.07",  # sum of the line item charge_amounts
    rate_applicable_percent="19.00",  # tax rate in percent (not "0.19")
    tax_total_amount="50.93",
    grand_total_amount="319.00",
    due_date="20240516"
)


# forward the building-blocks to the MinimalInvoice class
# and build the invoice:
minimal_invoice = MinimalInvoice(
    seller=seller,
    buyer=buyer,
    header=header,
    basic_line_items=basic_line_items,
    total=total
)
invoice = minimal_invoice.build()


# print the resulting XML to stdout (or write it to a file):
print(invoice)
```


## Output validation

The output are business data for fiscal use and must be correct by the numbers and the XML-format. Responsibility for the numbers is up to the user, to check the latter the specification sources (`ferd-net.de` and  `fnfe-mpe.org`) provide schematron-data to test the generated XML e-invoice (i.e. by means of `saxon`).

The example above produces a valid output according to the **EN16931-CII-validation** schematron.

In case the structure of the input data is changed to provide more information in the invoice, the **EN16931-CII-validation** schematron should again be applied to the output. Even if the output is valid XML it could be that the e-invoice may not be correct according to the defined business rules of the used profile (BASIC or other).

**The input determines the correctness of the output, even if the library does not raise an error. It is up to the user to provide qualified input-data and test the output for correctness.**

## Next steps

See the `examples` folder for example files. The function `build_basic_invoice` (in the `facturxlib.basic` module) accepts optional arguments to provide more data in an e-invoice. **Keep in mind to validate the output after every applied change**.

For using another profile than BASIC, there is currently no helper function like `build_basic_invoice`. But the library defines all required nodes to build instances of `ExchangedDocumentContext`, `ExchangedDocument` and `SupplyChainTradeTransaction` which are the required input for the `facturx.build_invoice` function, which is the main entry-point of the library.

## License

MIT
