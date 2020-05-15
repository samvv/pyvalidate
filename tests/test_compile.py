
from unittest import TestCase

try:
    import astor
except ImportError:
    pass

from pyvalidate.decorators import validator
from pyvalidate.compile import compile_validator

def has_next(iterable):
    try:
        next(iterable)
    except StopIteration:
        return False
    return True

class TestCompile(TestCase):

    def assert_validates(self, validator, value):
        self.assertEqual(validator.is_valid(value), not has_next(validator.get_errors(value)))

    def test_simple_equality(self):

        @validator
        def is_valid(value):
            return value == 1

        self.assert_validates(is_valid, 1)
        self.assert_validates(is_valid, 2)
        self.assert_validates(is_valid, False)
        self.assert_validates(is_valid, "Foo!")
        print(str(list(is_valid.get_errors("foo"))[0]))

    def test_early_return(self):

        @validator
        def is_valid(value):
            if value != 1:
                return False
            return True

        self.assert_validates(is_valid, 1)
        self.assert_validates(is_valid, 2)
        self.assert_validates(is_valid, False)
        self.assert_validates(is_valid, "Foo!")

    def test_boolean_or(self):

        @validator
        def is_valid(value):
            return value == 1 or value == 2

        self.assert_validates(is_valid, 1)
        self.assert_validates(is_valid, 2)
        self.assert_validates(is_valid, 3)
        self.assert_validates(is_valid, False)
        self.assert_validates(is_valid, "Foo!")

    def test_readme_example(self):

        @validator
        def valid_password(password):
            if len(password) < 8:
                return False
            return password != 'password'  \
               and password != 'easypeasy' \
               and password != 'p@ssw0rd'

        self.assert_validates(valid_password, 'somelongpassword123')
        self.assert_validates(valid_password, 'w3rdp@zzw0rdZw0rkT00')
        self.assert_validates(valid_password, 'password')
        self.assert_validates(valid_password, 'soshort')

    def test_in_not_in(self):

        @validator
        def is_valid(value):
            return value in ['test', 'foo', 'bar']

        msgs = list(is_valid.get_errors('bax'))
        self.assertEqual(str(msgs[0]), "value must be either of 'test', 'foo' or 'bar'")
        self.assert_validates(is_valid, 'test')
        self.assert_validates(is_valid, 'bax')

