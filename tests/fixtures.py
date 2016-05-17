# -*- coding: utf-8 -*-
import pytest
from sales_taxes.product import Product, ProductCategory, ProductSource
from sales_taxes.tax_definition import TaxDefinitionFactory
from sales_taxes.cart import Cart
from decimal import Decimal

@pytest.fixture(scope="module")
def product_book(price=Decimal(10)):
    return Product("some name",
                   price,
                   ProductSource.LOCAL,
                   ProductCategory.BOOKS)


@pytest.fixture(scope="module")
def product_taxable(price=Decimal(10), source=ProductSource.LOCAL):
    return Product("some name",
                   price,
                   source,
                   ProductCategory.OTHER)


@pytest.fixture(scope='module')
def standard_cart():
    cart = Cart()

    # Specify tax definitions applied to the items in the cart
    cart.add_tax_definition(TaxDefinitionFactory.
                            create_definition('BasicTaxDefinition'))
    cart.add_tax_definition(TaxDefinitionFactory.
                            create_definition('ImportTaxDefinition'))
    return cart
