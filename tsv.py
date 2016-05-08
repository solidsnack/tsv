# coding: utf-8
from __future__ import unicode_literals

import six


def un(source, row=list):
    """Parse a text stream to TSV

    If the source is a string, it is converted to a line-iterable stream. If
    it is a file handle or other object, we assume that we can iterate over
    the lines in it.

    The result is a generator, and what it contains depends on whether the
    second argument is set and what it is set to.

    If the second argument is set to list, the default, then each element of
    the result is a list of strings. If it is set to a class generated with
    namedtuple(), then each element is an instance of this class, or None if
    there were too many or too few fields.

    Although newline separated input is preferred, carriage-return-newline is
    accepted on every platform.

    Since there is no definite order to the fields of a dict, there is no
    consistent way to format dicts for output. To avoid the asymmetry of a
    type that can be read but not written, plain dictionary parsing is
    omitted.
    """
    if isinstance(source, six.string_types):
        source = six.StringIO(source)
    if row is list:
        return (parse_line(line) for line in source if line != '')
    else:
        if not (hasattr(row, '_fields') and hasattr(row, '_make')):
            raise ValueError('Custom row holder %r is not a namedtuple', row)
        return (parse_namedtuple(line, row) for line in source if line != '')


def parse_namedtuple(line, namedtuple):
    try:
        return namedtuple._make(parse_line(line))
    except TypeError:
        return None


def parse_line(line):
    line = line.split('\n')[0].split('\r')[0]
    return [parse_field(s) for s in line.split('\t')]


def parse_field(s):
    o = ''
    if s == '\\N':
        return None
    before, sep, after = s.partition('\\')
    while sep != '':
        o += before
        if after == '':
            raise FinalBackslashInFieldIsForbidden
        if after[0] in escapes:
            o += escapes[after[0]]
            before, sep, after = after[1:].partition('\\')
        else:
            before, sep, after = after.partition('\\')
    else:
        o += before
        return o


escapes = {'t': '\t', 'n': '\n', 'r': '\r', '\\': '\\'}


def to(items, output=None):
    """Present a collection of items as TSV

    The items in the collection can themselves be any iterable collection.
    (Single field structures should be represented as one tuples.)

    With no output parameter, a generator of strings is returned. If an output
    parameter is passed, it should be a file-like object. Output is always
    newline separated.
    """
    strings = (format_collection(item) for item in items)
    if output is None:
        return strings
    else:
        for s in strings:
            output.write(s + '\n')


def format_collection(col):
    return format_fields(*list(col))


def format_fields(*fields):
    if len(fields) != 0:
        return '\t'.join(format_field(field) for field in fields)


def format_field(thing):
    if thing is None:
        return '\\N'
    text = thing if isinstance(thing, six.string_types) else str(thing)
    return ('\\\\').join(escape_spacing_chars(s) for s in text.split('\\'))


def escape_spacing_chars(s):
    for a, b in [('\t', '\\t'), ('\n', '\\n'), ('\r', '\\r')]:
        s = s.replace(a, b)
    return s


class FinalBackslashInFieldIsForbidden(ValueError):
    pass
