#! /usr/bin/python
#-*-coding: utf-8 -*-

"""
a simple for loop with conditionals
% is the modulus operator, giving the remainder of the
integer division of the left operand by the right operand.
If a number divides by two with no remainder it is even.
"""
for i in range (0,10,1):
    if i % 2 == 1:
        print (str (i) + ' is an odd number.')
    else:
         print (str (i) + ' is an even number.')
