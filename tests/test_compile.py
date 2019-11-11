
from unittest import TestCase

from pyvalidate.compile import compile_validator

class TestCompile(TestCase):

    def test_simple_equality(self):

        def is_valid(value):
            return value == 1

        v1 = compile_validator(is_valid, locals(), globals())
        self.assertTrue(v1.is_valid(1))
        self.assertFalse(v1.is_valid(2))
        self.assertFalse(v1.is_valid(False))
        self.assertFalse(v1.is_valid("Foo!"))

    def test_early_return(self):

        def is_valid(value):
            if value != 1:
                return False
            return True

        v1 = compile_validator(is_valid, locals(), globals())
        self.assertTrue(v1.is_valid(1))
        self.assertFalse(v1.is_valid(2))
        self.assertFalse(v1.is_valid(False))
        self.assertFalse(v1.is_valid("Foo!"))

    def test_boolean_or(self):

        def is_valid(value):
            return value == 1 or value == 2

        v1 = compile_validator(is_valid, locals(), globals())
        self.assertTrue(v1.is_valid(1))
        self.assertTrue(v1.is_valid(2))
        self.assertFalse(v1.is_valid(3))
        print(list(v1.validate(3)))
        self.assertFalse(v1.is_valid(False))
        self.assertFalse(v1.is_valid("Foo!"))
