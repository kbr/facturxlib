# facturxlib

Library to create e-invoices according to the factur-x specification 1.01.06 (ZUGFeRD 2.2). The library provides the buildung blocks to set up a Cross Industry Invoice (CII) schema according to EN16931-3-3 and export this as XML.

The structur and documentation of this format is avialable here `http://fnfe-mpe.org/factur-x/factur-x_en/` and here `https://www.ferd-net.de/standards/zugferd-2.2/zugferd-2.2.html`

The format is based on XML-Nodes. All nodes are supported to build CIIs according to the EXTENDED profile. For convenience there is an API to support the BASIC profile with all required and optional information. Also a minimal API is provided to support just the required information, what can be sufficient for simple invoices.




See the `examples` folder for the example files.

The library does not do any calculation and all arguments used by the library must be provided as strings. These arguments are used "as is" to keep the output in sync with the original data.



