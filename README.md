# facturxlib

Library to create e-invoices according to the factur-x specification 1.01.06 (and also ZUGFeRD 2.2 without the pdf-reprensentation). The library provides the buildung blocks to create a Cross Industry Invoice (CII or e-invoice) according to EN16931-3-3 and provide the resulting data as XML.

Information about the structur and the documentation of this format as well as schematron-data (for output validation) are available here `https://fnfe-mpe.org/factur-x/factur-x_en/` and here `https://www.ferd-net.de/standards/zugferd-2.2/zugferd-2.2.html`. (These documents are published by their own license and therefor not included here.)

The format is based on XML-Nodes. The library supports all nodes that are required to build an e-invoice according to the EXTENDED profile. For convenience there is an API to support the BASIC profile with all required and optional arguments.

For the common usecase by smaller companies to just provide the seller-
and buyer-addresses and a list of sold items with a common tax-rate, the
class `MinimalInvoice` can simplifiy the creation of an e-invoice even
more.


## Installation and Dependencies

Install this library by `pip install facturxlib`.

The `facturxlib` library has no dependencies beside the standard-library.


## Example

The following example makes use of the most basic interface to produce an e-invoice with a minimal required dataset. It consist of a seller- and buyer-address and a list of sold items all with the same tax rate:

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
    phone="+49 211 123456789",
    email="seller@example.com",
    specified_tax_registration="DE 65 123 456",
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

# provide the header with the running invoice number, the invoice date
# and date of delivery which is optional by the profile-definition
# but mandatory in Germany (date-format: CCYYMMDD):
header = MinimalInvoiceHeader(
    invoice_id = "123/2024",
    invoice_issue_date = "20240502",
    delivery_occurence_date = "20240430",
)

# build a list of items sold to the buyer:
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
    line_total_amount="268.07",
    rate_applicable_percent="19.00",
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

In the example all numeric data must be given as strings. This is because the library takes all data "as is" and makes no calculations. This way there can be no deviations between the output and the bookkeeping-tool providing the input.

## Output validation

The output are financial data for fiscal use and must be correct. To check the correctness the "AWV – Arbeitsgemeinschaft für wirtschaftliche Verwaltung e. V." (`https://www.ferd-net.de`) provides schematron-data for testing the output (i.e. by means of `saxon` (`saxonica.com`)). "Le Forum National de la Facture Electronique et des Marchés Publics Electroniques (FNFE-MPE)" (`https://fnfe-mpe.org`) provides the same schematron-data.

The example above produces a valid output according to the **EN16931-CII-validation** schematron.

In case you change the structure of the input data to provide more information in the invoice, you should apply the **EN16931-CII-validation** schematron before using the modified input. Even if the output is valid XML it could be that the output may not be correct according to the defined business rules of the profile (BASIC or other).

**The input determines the correctness of the output, even if the library does not raise an error.**

## What next?

See the `examples` folder for the example files. The function `build_basic_invoice` (in the `facturxlib.basic` module) accepts optional arguments to provide more data in an e-invoice. Keep in mind to validate the output after every change you may apply.

For using another profile than BASIC, there is currently no helper function like `build_basic_invoice`. But the library defines all required nodes to build instances of `ExchangedDocumentContext`, `ExchangedDocument` and `SupplyChainTradeTransaction` which are the required input for the `facturx.build_invoice` function which is the main entry-point of the library.


## License

Like the schematron-files for the e-invoice verification the facturxlib-library  is published under the **European Union Public License (EUPL-1.2)** (`https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12`) or (`https://opensource.org/license/eupl-1-2`). This licencese is compatible with most other FOSS licenses and available in all official languages of the european community.
