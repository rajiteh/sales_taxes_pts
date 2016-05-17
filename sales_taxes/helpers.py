# -*- coding: utf-8 -*-


# Courtesy of http://stackoverflow.com/a/1695250
def enum(name, *sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type(name, (), enums)
