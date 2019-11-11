
from unittest import TestCase

from pyvalidate.compile import compile_validator

class TestCompile(TestCase):

    def test_simple_equality(self):

        def is_valid_1(value):
            return value == 1

        v1 = compile_validator(is_valid_1, locals(), globals())
        self.assertTrue(v1.is_valid(1))
        self.assertFalse(v1.is_valid(2))
        self.assertFalse(v1.is_valid(False))
        self.assertFalse(v1.is_valid("Foo!"))

        def is_valid_2(value):
            if value == 1:
                return True
            return False

        v2 = compile_validator(is_valid_2, locals(), globals())
        self.assertTrue(v2.is_valid(1))

