# -*- coding: utf-8 -*-
import decimal
import math


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
    CENTS = decimal.Decimal('0.01')
    ROUND_OFF = 1 / 0.05

    def apply(self, value):
        return decimal.Decimal(
            math.ceil(float(value) * self.ROUND_OFF) / self.ROUND_OFF)\
            .quantize(self.CENTS, decimal.ROUND_HALF_DOWN)
