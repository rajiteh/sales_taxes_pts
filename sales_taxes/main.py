#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Program entry point"""
from __future__ import print_function
from decimal import Decimal, ROUND_DOWN
from contextlib import contextmanager
from sales_taxes.cart import Cart
from sales_taxes.product import (ProductSource, ProductCategory, Product)
from sales_taxes.tax_definition import TaxDefinitionFactory
import re
import sys

INPUT_REGEX = '^(?P<quantity>[0-9]+)\s+' \
              '(?P<name>(?:.*(?P<imported>imported?))?.+)\s+at\s+' \
              '(?P<price>[0-9]*\.?[0-9]+)$'


def main():
    """Program entry point.

    Syntax: `cat input.txt | script.py`
    Where `input.txt` conatains well formatted order details.


    Parses the input strings, construct the :type:`Cart` and prints out the
    shopping list.

        :return: exit status
        :rtype: int
    """

    cart = Cart()

    # Specify tax definitions applied to the items in the cart
    cart.add_tax_definition(TaxDefinitionFactory.
                            create_definition('BasicTaxDefinition'))
    cart.add_tax_definition(TaxDefinitionFactory.
                            create_definition('ImportTaxDefinition'))

    with get_input_handle() as handle:
        for line in handle:
            quantity, product_spec = parse_order(line)
            product = Product(**product_spec)
            cart.add_item(product, quantity)
    receipt_printer(cart)
    return 0


@contextmanager
def get_input_handle(filename=None):
    """Detect the input method and retrieve a handler.

    Method will return a file handler (if a filename is supplied) or the
    standard input handler.

    :return: an input handler to iterate order details from
    :rtype: Iterable
    """
    if filename:
        file = open(filename, 'r')
        try:
            yield file
        finally:
            file.close()
    else:
        yield sys.stdin


def parse_order(line):
    """Parses a properly formatted order string.

    Uses regex group matching to identify the information in the order string.

    :param line: formatted string describing the order item
    :type line: str
    :return: quantity of the order, dict object containing product details
    :rtype: tuple
    """
    m = re.match(INPUT_REGEX, line)
    try:
        quantity = int(m.group('quantity'))
        # Remove 'imported' from the product name capture for cleaner printing
        name = re.sub("\s*imported\s*", ' ', m.group('name')).strip()
        product_source = ProductSource.IMPORTED if m.group('imported')\
            else ProductSource.LOCAL

        details = dict(name=name,
                       product_source=product_source,
                       price=Decimal(m.group('price')).quantize(Decimal('.01'), rounding=ROUND_DOWN),
                       product_category=fuzzy_categorize(m.group('name')))
    except AttributeError:
        raise Exception("Incorrect input format. Cannot parse.")
    return quantity, details


def fuzzy_categorize(name):
    """Matches product names to their respective product categories

     Fuzzy matching product names to product categories by checking for
     specific keywords.

    :param name: product name
    :type name: str
    :return: Product category for the provided product name
    :rtype: ProductCategory
    """
    mappings = {
        ProductCategory.BOOKS: ('book',),
        ProductCategory.FOODS: ('chocolate',),
        ProductCategory.MEDICAL: ('headache pill',)
    }
    for category, keywords in mappings.items():
        for keyword in keywords:
            if keyword in name:
                return category
    return ProductCategory.OTHER


def receipt_printer(cart, output=sys.stdout):
    """Prints a cart summary.

    :param cart: cart to print the summary from
    :param output: output handler (defaults to standard output)
    :type cart: Cart
    :return:
    """
    for ci in cart.get_items():
        output.write("{}\n".format(ci))
    output.write("Sales Taxes: {}\n".format(cart.get_taxes()))
    output.write("Total: {}\n".format(cart.get_net_total()))


if __name__ == '__main__':
    sys.path.append('../')
    main()
