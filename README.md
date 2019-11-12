Python Validation Library
=========================

This is the definitive validation library for Python 3 and above. Featuring
automatic generation of error messages, a collection of built-in validators and
support for the Python 3 `typing` module, your search for the perfect
validation library has finally come to an end!

```py
@validator
def is_valid_password(password):
    if len(password) < 8:
        return False
    return password != 'password' \
        and password != 'easypeasy' \
        and password != 'p@ssw0rd'

# works as you'd expect
is_valid_password('areallygoodlongpasswordhaha') # True

# prints "password must be longer than 8 characters"
print(next(valid_password.get_errors('bob'))

# prints "password may not equal 'easypeasy'"
print(next(valid_password.get_errors('easypeasy'))
```

## Rationale

A lot of work goes into creating huge schema specifications that capture as
much of the business logic as possible. For example, [JSON Schema][1] even has
conditionals, which you'd normally only expect in regular programming languages:

```json
{
  "type": "object",
  "properties": {
    "street_address": {
      "type": "string"
    },
    "country": {
      "enum": ["United States of America", "Canada"]
    }
  },
  "if": {
    "properties": { "country": { "const": "United States of America" } }
  },
  "then": {
    "properties": { "postal_code": { "pattern": "[0-9]{5}(-[0-9]{4})?" } }
  },
  "else": {
    "properties": { "postal_code": { "pattern": "[A-Z][0-9][A-Z] [0-9][A-Z][0-9]" } }
  }
}
```

It looks OK, but it is quite cumbersome. **pyvalidate** tries to do the reverse, by
allowing you to write regular Python code. The Python code is transformed to a
sort of schema under the hood.

In theory, this allows you to write any Python code you can come up with and
have it magically work. In practice, **pyvalidate** sometimes needs a little nudge
in the right direction, but it is worth it!

[1]: https://json-schema.org/specification.html

## Features

The following features are planned:

 - [x] A `@validator` decorator that can automatically transform simple Python
   functions to a validator with user-friendly error messages.
 - [ ] `@validate` decorator that will give better error messages to your
   existing Python functions.
 - [ ] Native support for translations with fine-grained control over how the 
   messages are built.
 - [ ] A growing collection of built-in validators to help you build your
   programs faster.
 - [ ] Support for Python 3's [`typing`][2] module, allowing you to write types 
   and have them automatically validated.

[2]: https://docs.python.org/3/library/typing.html

## More Examples

### Using `SimpleRecord`

The following demonstrates the use of `SimpleRecord`, which uses **pyvalidate**
under the hood:

```py
from pyvalidate import SimpleRecord

class Address(SimpleRecord):
  street: str
  house_number: int
  city: str
  country: str

class Person(SimpleRecord):
    serial: int
    firstname: str
    lastname: str
    phone: Optional[str]
    address: Address
    age: int
```

You can just act as if each record is a [`SimpleNamespace`][2]:

[2]: https://docs.python.org/3/library/types.html#types.SimpleNamespace

```py
jefs_address = Address(street='Boudewijnstraat', house_number=25, \
                       city='Elsene', country='Belgium')
```

... or use positional arguments to keep it short:

```
smith = Person('Jef', 'Uyterhoeve', '+32475948314', jefs_address, 34)
```

Be careful, though, because things like this won't work:

```py
jan = Person('Jan', 'Vercouteren', None, None, 34) # TypeError: 'address' is required
```

What if you want to know upfront if constructing a record will give an error.
Easy, just use the static method `is_valid()` or `get_errors()`!

```py
Person.is_valid('Jan', 'Vercouteren', None, None, 34) # False
```

## License

© 2012 Vahid Mardani

© 2019 Sam Vervaeck

The license of this software has yet to be determined.

