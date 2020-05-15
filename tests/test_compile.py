
from pyvalidate import validator, compile_validator

def has_next(iterable):
    try:
        next(iterable)
    except StopIteration:
        return False
    return True

def has_same_output(validator, value):
    return validator.is_valid(value) == (not has_next(validator.get_errors(value)))

def test_simple_equality():

    @validator
    def is_valid(value):
        return value == 1

    has_same_output(is_valid, 1)
    has_same_output(is_valid, 2)
    has_same_output(is_valid, False)
    has_same_output(is_valid, "Foo!")
    print(str(list(is_valid.get_errors("foo"))[0]))

def test_early_return():

    @validator
    def is_valid(value):
        if value != 1:
            return False
        return True

    has_same_output(is_valid, 1)
    has_same_output(is_valid, 2)
    has_same_output(is_valid, False)
    has_same_output(is_valid, "Foo!")

def test_boolean_or():

    @validator
    def is_valid(value):
        return value == 1 or value == 2

    has_same_output(is_valid, 1)
    has_same_output(is_valid, 2)
    has_same_output(is_valid, 3)
    has_same_output(is_valid, False)
    has_same_output(is_valid, "Foo!")

def test_readme_example():

    @validator
    def valid_password(password):
        if len(password) < 8:
            return False
        return password != 'password'  \
           and password != 'easypeasy' \
           and password != 'p@ssw0rd'

    has_same_output(valid_password, 'somelongpassword123')
    has_same_output(valid_password, 'w3rdp@zzw0rdZw0rkT00')
    has_same_output(valid_password, 'password')
    has_same_output(valid_password, 'soshort')

def test_in_not_in():

    @validator
    def is_valid(value):
        return value in ['test', 'foo', 'bar']

    msgs = list(is_valid.get_errors('bax'))
    assert(str(msgs[0]) == "value must be either of 'test', 'foo' or 'bar'")
    has_same_output(is_valid, 'test')
    has_same_output(is_valid, 'bax')

