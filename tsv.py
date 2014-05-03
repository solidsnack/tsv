#!/usr/bin/env python

import StringIO
import sys


def main():
    for state, city, population, area in parse(sys.stdin):
        location, density = None, None
        location = '%s (%s)' % (city, state)
        if population and area:
            density = '%0.4f' % (float(population) / float(area))
        print format_fields(location, density)

def parse(source):
    """Parse a text stream

    If the source is a string, it is converted to a line-iterable stream.

    If it is a file handle or other object, we assume that we can iterate over
    the lines in it.

    A generator of parsed field lists is returned.
    """
    if isinstance(source, basestring):
        source = StringIO.StringIO(source)
    return ( parse_line(line) for line in source )

def parse_line(line):
    line = line.split('\n')[0].split('\r')[0]
    return [ parse_field(s) for s in line.split('\t') ]

def parse_field(s):
    if s == '\\N':
        return None
    if s[-1:] == '\\':
        raise FinalBackslashInFieldIsForbidden
    for a, b in [ ('\\t', '\t'), ('\\n', '\n'), ('\\r', '\r'), ('\\', '') ]:
        s = s.replace(a, b)
    return s

def format_fields(*fields):
    return '\t'.join( format_field(field) for field in fields )

def format_field(thing):
    if thing is None:
        return '\\N'
    text = thing if isinstance(thing, basestring) else str(thing)
    return ('\\\\').join( escape_spacing_chars(s) for s in text.split('\\') )

def escape_spacing_chars(s):
    for a, b in [ ('\t', '\\t'), ('\n', '\\n'), ('\r', '\\r') ]:
        s = s.replace(a, b)
    return s

class FinalBackslashInFieldIsForbidden(ValueError):
    pass


if __name__ == '__main__':
    main()

