"""
minimal_basic_example.py

Example file for the BASIC profile with the required nodes.

All financial numbers must be provided as strings, because the library
does no automatic conversion or calculation. This ensurees to keep all
data in sync with the original calculation.
"""


from facturxlib.basic import (
    BasicLineItem,
    BasicTradeParty,
    MinimalInvoice,
    MinimalInvoiceHeader,
    MinimalInvoiceTotal,
)


def run_minimal_basic_example():

    # provide the seller address:
    seller = BasicTradeParty(
        name="Seller Company",
        line_one="Trade Street 42",
        postcode="40123",
        city_name="Düsseldorf",  # mind the umlaut
        country_id="DE",
        phone="+49 211 123456789",
        email="seller@example.com",
        specified_tax_registration="DE 65 123 456",
        specified_tax_registration_scheme="VA"
    )

    # provide the buyer address.
    # the identifier could be a seller-defined customer number.
    buyer = BasicTradeParty(
        name="Buyer GmbH & Co KG",
        line_one="Buyer Lane 1",
        postcode="12345",
        city_name="Buxtehude",
        country_id="DE",
        identifier="10423"
    )

    # provide the header with running invoice number, date
    # and date of delivery which is mandatory in Germany.
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

    # sum the totals and provide `due_date` as this is required
    # if the `grand_total_amount` is larger than 0.
    total = MinimalInvoiceTotal(
        line_total_amount="268.07",
        rate_applicable_percent="19.00",
        tax_total_amount="50.93",
        grand_total_amount="319.00",
        due_date = "20240516"
    )

    # forard the minimal data blocks to the MinimalInvoice class
    # and build the invoice:
    minimal_invoice = MinimalInvoice(
        seller=seller,
        buyer=buyer,
        header=header,
        basic_line_items=basic_line_items,
        total=total
    )
    invoice = minimal_invoice.build()


    print(invoice)


if __name__ == "__main__":
    run_minimal_basic_example()
