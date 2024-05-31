"""
test_basic.py

Example file for the BASIC profile with all required nodes.

All financial numbers must be provided as strings, because the library
does no automatic conversion or calculation. This ensurees to keep all
data in sync with the original calculation.

"""


from facturxlib.basic import (
    build_basic_invoice,
    ApplicableTradeTax,
    BasicLineItem,
    BasicTradeParty,
    GrandTotalAmount,
    TaxBasisTotalAmount,
    TaxTotalAmount,
)


def run_basic_example():

    invoice_id = "123/2024"
    invoice_issue_date = "20240502"
    delivery_occurence_date = "20240430"

    seller = BasicTradeParty(
        name="Seller Company",
        line_one="Trade Street 42",
        postcode="40123",
        city_name="Düsseldorf",  # mind the umlauts
        country_id="DE",
        phone="+49 211 123456",
        email="seller@example.com",
        specified_tax_registration="DE 65 123 456",
        specified_tax_registration_scheme="VA"
    )

    buyer = BasicTradeParty(
        name="Buyer GmbH & Co KG",
        line_one="Buyer Lane 1",
        postcode="12345",
        city_name="Buxtehude",
        country_id="DE",
        identifier="10423"  # five digits customer id (aka. Kundennummer)
    )

    basic_line_items = [
        BasicLineItem(
            line_id="1",
            name="Potato Chips (750 gr. package)",
            charge_amount="1.95",
            basis_quantity="100",
            billed_quantity="100",
            line_total_amount="195.00",
            rate_applicable_percent="19.00",
        ),
        BasicLineItem(
            line_id="2",
            name="Curley Fries (500 gr. package)",
            charge_amount="1.75",
            basis_quantity="100",
            billed_quantity="100",
            line_total_amount="175.00",
            rate_applicable_percent="19.00",
        )
    ]


    # the BASIC profile allows for multiple trade taxes differing
    # with the ivoice currency.
    applicable_trade_taxes = [
        ApplicableTradeTax.from_basic_profile(
            basis_amount="370.00",
            rate_applicable_percent="19.00",
            calculated_amount="70.30",
            category_code="S",
            type_code="VAT",
        )
    ]

    result = build_basic_invoice(
        invoice_id=invoice_id,
        invoice_issue_date=invoice_issue_date,
        delivery_occurence_date=delivery_occurence_date,
        buyer=buyer,
        seller=seller,
        basic_line_items=basic_line_items,
        applicable_trade_taxes=applicable_trade_taxes,
        line_total_amount="370.00",
        tax_basis_total_amount=TaxBasisTotalAmount("370.00"),
        tax_total_amounts=[TaxTotalAmount("70.30", currency_id="EUR")],  # example for optional currency
        grand_total_amount=GrandTotalAmount("440.30"),
        due_payable_amount="440.30"
    )

    print(f"\n{result}\n")


if __name__ == "__main__":
    run_basic_example()
