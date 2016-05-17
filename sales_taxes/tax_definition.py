# -*- coding: utf-8 -*-
import decimal
from .product import (Product, ProductSource, ProductCategory)


class TaxDefinitionFactory(object):
    @staticmethod
    def create_definition(td_name):
        tax_definitions = {
            'BasicTaxDefinition': BasicTaxDefinition,
            'ImportTaxDefinition': ImportTaxDefinition
        }
        return tax_definitions[td_name]()


class BaseTaxDefinition(object):

    def __init__(self, multiplier=decimal.Decimal(0)):
        self._multiplier = multiplier

    def apply(self, product):
        assert isinstance(product, Product)
        return self._calculate_product_tax(product)

    def _calculate_product_tax(self, product):
        raise NotImplementedError('Method must be overridden.')


class BasicTaxDefinition(BaseTaxDefinition):

    EXEMPTIONS = (
        ProductCategory.BOOKS,
        ProductCategory.FOODS,
        ProductCategory.MEDICAL
    )

    def __init__(self):
        multiplier = decimal.Decimal('0.10')
        super(BasicTaxDefinition, self).__init__(multiplier)

    def _calculate_product_tax(self, product):
        if product.product_category in self.EXEMPTIONS:
            return decimal.Decimal(0)
        else:
            return product.price * self._multiplier


class ImportTaxDefinition(BaseTaxDefinition):

    def __init__(self):
        multiplier = decimal.Decimal('0.05')
        super(ImportTaxDefinition, self).__init__(multiplier)

    def _calculate_product_tax(self, product):
        if product.product_source == ProductSource.IMPORTED:
            return product.price * self._multiplier
        else:
            return decimal.Decimal(0)
