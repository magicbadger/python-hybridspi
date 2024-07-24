from spi import *

import unittest

class BearerTest(unittest.TestCase):

    def test_fm_parse_valid(self):
        print('here')
        FmBearer.fromstring('fm:ce1.c985.09580')
        FmBearer.fromstring('fm:ce1.c985.*')

    @unittest.expectedFailure
    def test_fm_parse_invalid(self):
        FmBearer.fromstring('fm:cee1.c85.095802')
        FmBearer.fromstring('fm:ce1.*.09580')

