# -*- coding: utf-8 -*-
from pytest import raises
# The parametrize function is generated, so this doesn't work:
#
#     from pytest.mark import parametrize
#
import pytest

parametrize = pytest.mark.parametrize

from sales_taxes.main import parse_order
from sales_taxes.product import ProductCategory, ProductSource
from decimal import Decimal, ROUND_DOWN

class TestMain(object):

    def test_parse_order(self):
        lines = [
            "10 sticks of imported pythons at 59.99",
            "10 imported sticks of pythons at 59.99"
        ]

        result = (10, dict(
            name='sticks of pythons',
            product_source=ProductSource.IMPORTED,
            price=Decimal(59.99001).quantize(Decimal('.01'), rounding=ROUND_DOWN),
            product_category=ProductCategory.OTHER
        ))

        # identifies imported products properly
        for line in lines:
            assert parse_order(line) == result

        result = (1, dict(
            name='perfume bottle',
            product_source=ProductSource.LOCAL,
            price=Decimal(1),
            product_category=ProductCategory.OTHER
        ))
        line = "1 perfume bottle at 1"
        assert parse_order(line) == result
