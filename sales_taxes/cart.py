# -*- coding: utf-8 -*-
from copy import deepcopy
from .rounding_policy import (RoundingPolicyFactory, BaseRoundingPolicy)
from .tax_definition import BaseTaxDefinition
from .product import Product
import decimal


class Cart(object):
    """

    """
    class CartItem(object):
        def __init__(self, product, quantity):
            assert isinstance(product, Product)
            self.product = product
            self.quantity = quantity
            self.tax = decimal.Decimal(0)

        @property
        def sub_total(self):
            return self.quantity * self.product.price

        @property
        def net_total(self):
            return self.sub_total + self.tax

        def __str__(self):
            return "{} {}: {}".format(self.quantity,
                                      self.product, self.net_total)

    def __init__(self, rounding_policy=RoundingPolicyFactory.
                 create_policy('StandardRoundingPolicy')):
        assert isinstance(rounding_policy, BaseRoundingPolicy)
        self._tax_definitions = []
        self._cart_items = []
        self._rounding_policy = rounding_policy

    def _calculate_taxes(self):
        for ci in self._cart_items:
            tax = decimal.Decimal(0)
            for td in self._tax_definitions:
                _t = td.apply(ci.product) * ci.quantity
                _t_rounded = self._rounding_policy.apply(_t)
                tax += _t_rounded
            ci.tax = tax

    def _get_item_or_none(self, _product):
        for ci in self._cart_items:
            if ci.product == _product:
                return ci
        return None

    def get_items(self):
        return deepcopy(self._cart_items)

    def get_taxes(self):
        return sum(ci.tax for ci in self._cart_items)

    def get_sub_total(self):
        return sum(ci.sub_total for ci in self._cart_items)

    def get_net_total(self):
        return sum(ci.net_total for ci in self._cart_items)

    def _recalculate(fn, *args, **kwargs):
        def _wrapped(self, *args, **kwargs):
            pre_cart_state = deepcopy(self._cart_items)
            try:
                fn(self, *args, **kwargs)
                self._calculate_taxes()
            except (AssertionError, NotImplementedError):
                # TODO: Granular exception handling
                self._cart_items = pre_cart_state
                raise
        return _wrapped


    @_recalculate
    def add_tax_definition(self, tax_definition):
        assert isinstance(tax_definition, BaseTaxDefinition)
        self._tax_definitions.append(tax_definition)

    @_recalculate
    def add_item(self, _product, quantity=1):
        assert isinstance(_product, Product)
        assert quantity > 0

        item = self._get_item_or_none(_product)
        if item is None:
            item = self.CartItem(product=_product, quantity=0)
            self._cart_items.append(item)

        item.quantity += quantity
