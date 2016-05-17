# -*- coding: utf-8 -*-
from pytest import raises
# The parametrize function is generated, so this doesn't work:
#
#     from pytest.mark import parametrize
#
import pytest

parametrize = pytest.mark.parametrize

from tests.fixtures import *
from sales_taxes.rounding_policy import RoundingPolicyFactory, StandardRoundingPolicy
from decimal import Decimal, ROUND_DOWN
class TestRoundingPolicy(object):

    def test_factory(self):
        srp = RoundingPolicyFactory.create_policy('StandardRoundingPolicy')
        assert srp.__class__ == StandardRoundingPolicy().__class__

    def test_standard_rounding_policy(self):
        srp = StandardRoundingPolicy()

        vals = {
            Decimal('0.0'): Decimal('0.0'),
            Decimal('0.01'): Decimal('0.05'),
            Decimal('0.06'): Decimal('0.10'),
            Decimal('10.06'): Decimal('10.10'),
            Decimal('1.99'): Decimal('2.0'),
            Decimal('13.13'): Decimal('13.15')
        }

        for _k, _v in vals.items():
            k = _k.quantize(Decimal('.01'), rounding=ROUND_DOWN)
            v = _v.quantize(Decimal('.01'), rounding=ROUND_DOWN)
            assert srp.apply(k) == v
