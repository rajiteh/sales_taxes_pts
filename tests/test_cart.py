# -*- coding: utf-8 -*-
from pytest import raises
# The parametrize function is generated, so this doesn't work:
#
#     from pytest.mark import parametrize
#
import pytest

parametrize = pytest.mark.parametrize

from sales_taxes import metadata
from sales_taxes.cart import Cart
from unittest.mock import Mock
from sales_taxes.rounding_policy import StandardRoundingPolicy
from sales_taxes.tax_definition import BasicTaxDefinition, ImportTaxDefinition
from tests.fixtures import *
from decimal import Decimal


class TestCart(object):

    def test_init(self):
        cart = Cart()
        # must have the default policy
        assert cart._rounding_policy.__class__ == StandardRoundingPolicy

    def test_add_item(self):
        cart = standard_cart()
        item = product_taxable()
        cart.add_item(item)

        # added product should be in the cart
        assert len(cart._cart_items) == 1
        assert cart._cart_items[0].product == item

    def test_add_tax_definition(self):
        cart = Cart()
        item = product_taxable(Decimal(10), ProductSource.IMPORTED)
        cart.add_item(item)

        # Shouldnt calculate taxes
        assert cart.get_taxes() == Decimal(0)

        cart.add_tax_definition(BasicTaxDefinition())
        # Should calculate only local taxes
        assert cart.get_taxes() == Decimal(1)

        cart.add_tax_definition(ImportTaxDefinition())
        # Should calculate import and local taxes
        assert cart.get_taxes() == Decimal(1.5)

    def test_get_items(self):
        cart = Cart()
        item = product_taxable()
        item2 = product_taxable(Decimal(5))
        cart.add_item(item)
        cart.add_item(item2)

        # items should be identical
        p = [cartitem.product for cartitem in cart.get_items()]
        assert item in p
        assert item2 in p

    def test_get_taxes(self):
        cart = standard_cart()
        product = product_taxable(Decimal(10))
        product2 = product_taxable(Decimal(20))
        cart.add_item(product)
        cart.add_item(product2)

        # total taxes should be calculated
        assert cart.get_taxes() == Decimal(3)

    def test_get_sub_total(self):
        cart = standard_cart()
        product = product_taxable(Decimal(10))
        product2 = product_taxable(Decimal(20))
        cart.add_item(product)
        cart.add_item(product2)

        # proper sub total should be calculated
        assert cart.get_sub_total() == Decimal(30)

    def test_get_net_total(self):
        cart = standard_cart()
        product = product_taxable(Decimal(10))
        product2 = product_taxable(Decimal(20))
        cart.add_item(product)
        cart.add_item(product2)

        # proper net total should be calculated
        assert cart.get_net_total() == Decimal(33)

    def test__get_item_or_none(self):
        cart = standard_cart()
        product = product_book()
        product_2 = product_taxable()

        cart.add_item(product_2)

        # returns none on non-existent product
        assert cart._get_item_or_none(product) is None

        cart.add_item(product, 5)
        cart_item = cart._get_item_or_none(product)

        # returns the product and quantity on existent product
        assert cart_item.quantity == 5
        assert cart_item.product == product

    def test__calculate_taxes(self):
        cart = standard_cart()
        item = product_book(Decimal(10))
        cart.add_item(item)

        # Book should not have taxes
        assert cart._cart_items[0].tax == Decimal(0)

        cart = standard_cart()
        item = product_taxable(Decimal(20))
        cart.add_item(item)

        # should be basic taxed
        assert cart._cart_items[0].tax == Decimal(2)

        cart = standard_cart()
        item = product_taxable(Decimal(20), ProductSource.IMPORTED)
        cart.add_item(item)

        # should be import and basic taxed
        assert cart._cart_items[0].tax == Decimal(3)

    def test__recalculate(self):
        cart = standard_cart()
        p1 = product_taxable(Decimal(10))
        cart.add_item(p1)
        p2 = product_taxable(Decimal(20))

        cart._calculate_taxes = Mock(side_effect=AssertionError)
        try:
            cart.add_item(p2)
        except:
            pass

        # it should revert to last cart state
        assert len(cart._cart_items) == 1
        assert cart._cart_items[0].product == p1
        assert cart.get_net_total() == 11

    def test__cart_item(self):
        cart = standard_cart()
        p = product_taxable(Decimal(10))
        ci = cart.CartItem(p, 1)

        # initializes with 0 tax
        assert ci.tax == Decimal(0)

        ci.tax = 1
        # tax and total calculations
        assert ci.sub_total == Decimal(10)
        assert ci.net_total == Decimal(11)
