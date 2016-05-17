# -*- coding: utf-8 -*-
from pytest import raises
# The parametrize function is generated, so this doesn't work:
#
#     from pytest.mark import parametrize
#
import pytest

parametrize = pytest.mark.parametrize

from tests.fixtures import *

class TestProduct(object):

    def test__eq(self):
        p1 = product_taxable()
        p2 = product_taxable()

        assert p1 == p2

        p1.name = "other name"
        assert p1 != p2

        p1 = product_taxable()
        p1.price = Decimal(88)
        assert p1 != p2

        p1 = product_taxable()
        p1.product_source = ProductSource.IMPORTED
        assert p1 != p2

        p1 = product_taxable()
        p1.product_category = ProductCategory.BOOKS
        assert p1 != p2

        p1.product_category = p2.product_category
        assert p1 == p2
