# -*- coding: utf-8 -*-
from decimal import Decimal, ROUND_DOWN
import math
from helpers import currencyfy


class RoundingPolicyFactory(object):
    @staticmethod
    def create_policy(policy_type):
        policies = {
            'StandardRoundingPolicy': StandardRoundingPolicy
        }
        return policies[policy_type]()


class BaseRoundingPolicy(object):
    def apply(self, value):
        raise NotImplementedError('Method must be overridden.')


class StandardRoundingPolicy(BaseRoundingPolicy):
    ROUND_OFF = Decimal('1') / Decimal('0.05')

    def apply(self, value):
        _r = Decimal(math.ceil(value * self.ROUND_OFF)) / self.ROUND_OFF
        return currencyfy(_r)

