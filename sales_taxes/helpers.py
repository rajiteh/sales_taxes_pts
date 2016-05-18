# -*- coding: utf-8 -*-
import decimal


# Courtesy of http://stackoverflow.com/a/1695250
def enum(name, *sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type(name, (), enums)


CENTS = decimal.Decimal('0.01')


def currencyfy(dec):
    return dec.quantize(CENTS, decimal.ROUND_DOWN)
