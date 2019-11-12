
import string

class PluralFormatter(string.Formatter):
    def format_field(self, value, format_spec):
        if format_spec.startswith('plural,'):
            words = format_spec.split(',')
            if value == 1:
                return words[1]
            else:
                return words[2]
        else:
            return super().format_field(value, format_spec)

class MsgPart:
    def __init__(self, text, **kwargs):
        self.text = text
        self.kwargs = kwargs
    def __str__(self):
        skwargs = dict((key, str(value)) for key, value in self.kwargs.items())
        return self.text.format(**skwargs)

