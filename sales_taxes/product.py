# -*- coding: utf-8 -*-
from . import helpers
import decimal
ProductSource = helpers.enum('ProductSource', 'LOCAL', 'IMPORTED')
ProductCategory = helpers.enum('ProductCategory',
                               'BOOKS', 'FOODS', 'MEDICAL', 'OTHER')


class Product(object):

    def __init__(self, name, price, product_source, product_category):
        assert isinstance(price, decimal.Decimal)

        self.name = name
        self.price = price
        self.product_source = product_source
        self.product_category = product_category

    def __str__(self):
        return "{}{}".format("imported "
                             if self.product_source == ProductSource.IMPORTED
                             else "", self.name)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return \
                self.name == other.name and\
                self.product_source == other.product_source and\
                self.price == other.price and\
                self.product_category == other.product_category
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
