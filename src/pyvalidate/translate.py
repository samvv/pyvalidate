
import string
import inflect

from .vm import Evaluator

def enum(elements):
    assert(len(elements) > 0)
    if len(elements) == 1:
        return elements[0]
    else:
        return ', '.join(elements[:-1]) + ' or ' + elements[-1]

class EnumFormatter(string.Formatter):
    def format_field(self, value, format_spec):
        print(format_spec)
        if format_spec == 'enum':
            return enum(value)
        else:
            return super().format_field(value, format_spec)

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
        print(self.text)
        skwargs = dict((key, str(value)) for key, value in self.kwargs.items())
        return self.text.format(**skwargs)

class Translator:

    def format_message(self, text, **kwargs):
        scan_mode = 0 # default
        expr_buffer = ''
        for ch in text:
            if scan_mode == 0:
                if ch == '{':
                    scan_mode = 1
                else:
                    out += ch
            elif scan_mode == 1:
                if ch == '}':
                    out += self.evaluator.eval_expr(expr_buffer, locals=kwargs)
                    scan_mode = 0
                else:
                    expr_buffer += ch

import inflect

class EnglishTranslator(Translator):

    @callable
    def enum(self, elements):
        assert(len(elements) > 0)
        if len(elements) == 1:
            return elements[0]
        else:
            return ', '.join(elements[:-1]) + ' or ' + elements[-1]

    @callable
    def plural(self, noun):
        return inflect.plural_noun(noun)

    @callable
    def singular(self, noun):
        return inflect.singular_noun(noun)
