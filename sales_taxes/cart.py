# -*- coding: utf-8 -*-
from copy import deepcopy
from .rounding_policy import (RoundingPolicyFactory, BaseRoundingPolicy)
from .tax_definition import BaseTaxDefinition
from .product import Product
import decimal


class Cart(object):
    """Encapsulates shopping cart logic, tax application, and rounding

    Shopping cart contains a list of :type:`CartItem` objects containing
    information about the each item. :type:`Cart` is also responsible for
    calculating the taxes per item, and rounding currency values.

    """
    class CartItem(object):
        """Represents an entry in shopping cart.

        Contains data about the product, the quantity, the tax, and calculation
        of totals per entry.

        """
        def __init__(self, product, quantity):
            """Initialize with basic information about an item.

            :param product: the product added to the cart
            :param quantity: quantity of the product
            :type product: Product
            :type quantity: int
            :return:
            """
            assert isinstance(product, Product)
            self.product = product
            self.quantity = quantity
            self.tax = decimal.Decimal(0)

        @property
        def sub_total(self):
            """Calculates the sub total

            Calculates the sub total buy multiplying quantity with product
            price.

            :return: sub total of this cart entry without tax
            :rtype: decimal.Decimal
            """
            return self.quantity * self.product.price

        @property
        def net_total(self):
            """Calculates the net total (includes tax)

            Calculates the net total by adding the tax amount to sub total.

            :return:  net total of this cart entry
            :rtype: decimal.Decimal
            """
            return self.sub_total + self.tax

        def __str__(self):
            return "{} {}: {}".format(self.quantity,
                                      self.product, self.net_total)

    def __init__(self, rounding_policy=RoundingPolicyFactory.
                 create_policy('StandardRoundingPolicy')):
        """Initializing a cart object with a tax rounding policy.

        :param rounding_policy: Tax rounding policy for this cart.
        :type rounding_policy: BaseRoundingPolicy
        :return:
        """
        assert isinstance(rounding_policy, BaseRoundingPolicy)
        self._tax_definitions = []
        self._cart_items = []
        self._rounding_policy = rounding_policy

    def _calculate_taxes(self):
        """Calculates taxes for each cart item

        Iterates through all cart items and apply each configured tax rule and
        rounding rule.

        :return:
        """
        for ci in self._cart_items:
            tax = decimal.Decimal(0)
            for td in self._tax_definitions:
                _t = td.apply(ci.product) * ci.quantity
                _t_rounded = self._rounding_policy.apply(_t)
                tax += _t_rounded
            ci.tax = tax

    def _get_item_or_none(self, _product):
        """Retrieves a cart item if exists or else returns None

        :param _product: product contained in the cart item
        :type _product: Product
        :return: cart item containing the product or None
        :rtype: Cart.CartItem
        """
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
        """Recalculate cart taxes.

        A decorator method to recalculate cart state whenever state is changed.
        Ensures that cart is always in a valid state by accounting for runtime
        errors and reverting back to original cart state if the operation
        failed.

        :param args:
        :param kwargs:
        :return:
        """
        def _wrapped(self, *args, **kwargs):
            pre_cart_state = deepcopy(self._cart_items)
            pre_cart_tax = deepcopy(self._tax_definitions)
            try:
                fn(self, *args, **kwargs)
                self._calculate_taxes()
            except (AssertionError, NotImplementedError):
                # TODO: Granular exception handling
                self._cart_items = pre_cart_state
                self._tax_definitions = pre_cart_tax
                raise
        return _wrapped


    @_recalculate
    def add_tax_definition(self, tax_definition):
        """Adds a tax definition to be considered for item tax calculation

        :param tax_definition: Tax definition to be added
        :type tax_definition: BaseTaxDefinition
        :return:
        """
        assert isinstance(tax_definition, BaseTaxDefinition)
        self._tax_definitions.append(tax_definition)

    @_recalculate
    def add_item(self, _product, quantity=1):
        """Adds a product to the cart.

        A new cart item will be created with the given quantity or existing
        product's cart item quantity will be increased  by the given amount.

        :param _product: Product that requires quantity change
        :type _product: Product
        :param quantity: Amount of change that is needed in quantity
        :type quantity: int
        :return:
        """
        assert isinstance(_product, Product)
        assert quantity > 0

        item = self._get_item_or_none(_product)
        if item is None:
            item = self.CartItem(product=_product, quantity=0)
            self._cart_items.append(item)

        item.quantity += quantity
