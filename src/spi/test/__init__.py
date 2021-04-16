import unittest

from spi import *


class Test(unittest.TestCase):


    def test_shortname_limit(self):
        name = ShortName("SHORT")

    @unittest.expectedFailure
    def test_shortname_limit_exceed(self):
        name = ShortName("this should be too long")

    def test_shortname_gettext(self):
        name = ShortName("TEST")
        self.assertEqual(name.text, "TEST")

    def test_shortname_getdefaultlanguage(self):
        name = ShortName("TEST")
        self.assertEqual(name.language, DEFAULT_LANGUAGE)

    def test_shortname_getdifferentlanguage(self):
        name = ShortName("TEST", language="FR")
        self.assertNotEqual(name.language, "EN")
        self.assertEqual(name.language, "FR")



if __name__ == "__main__":
    unittest.main()
