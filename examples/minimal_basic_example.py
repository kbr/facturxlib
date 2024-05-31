"""
minimal_basic_example.py

Example file for the BASIC profile with the required nodes.

All financial numbers must be provided as strings, because the library
does no automatic conversion or calculation. This ensurees to keep all
data in sync with the original calculation.

"""


from facturxlib.basic import (
    build_minimal_basic_invoice,
    BasicLineItem,
    BasicTradeParty,
)


def run_minimal_basic_example():

    # define running invoice number and date and date of delivery
    # which is mandatory in Germany:
    invoice_id = "123/2024"
    invoice_issue_date = "20240502"
    delivery_occurence_date = "20240430"

    # provide the seller data:
    seller = BasicTradeParty(
        name="Seller Company",
        line_one="Trade Street 42",
        postcode="40123",
        city_name="Düsseldorf",  # mind the umlaut
        country_id="DE",
        phone="+49 211 123456",
        email="seller@example.com",
        specified_tax_registration="DE 65 123 456",
        specified_tax_registration_scheme="VA"
    )

    # build the buyer address.
    # the identifier is a seller define customer number.
    buyer = BasicTradeParty(
        name="Buyer GmbH & Co KG",
        line_one="Buyer Lane 1",
        postcode="12345",
        city_name="Buxtehude",
        country_id="DE",
        identifier="10423"
    )

    # build a list of items sold to the buyer:
    basic_line_items = [
        BasicLineItem.from_minimal_data(
            line_id="1",
            name="Power Supply 800 Watt",
            net_price="247.90"
        ),
        BasicLineItem.from_minimal_data(
            line_id="2",
            name="Cable set type M",
            net_price="16.39"
        ),
        BasicLineItem.from_minimal_data(
            line_id="3",
            name="Fuse 10 Ampere",
            net_price="3.78"
        )
    ]

    # build the invoice by providing the above defined data
    # and the
    result = build_minimal_basic_invoice(
        invoice_id=invoice_id,
        invoice_issue_date=invoice_issue_date,
        delivery_occurence_date=delivery_occurence_date,
        buyer=buyer,
        seller=seller,
        basic_line_items=basic_line_items,
        line_total_amount="268.07",
        rate_applicable_percent="19.00",
        tax_total_amount="50.93",
        grand_total_amount="319.00"
    )

    print(result)


if __name__ == "__main__":
    run_minimal_basic_example()
