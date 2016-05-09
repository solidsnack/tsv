# coding: utf-8
from __future__ import unicode_literals

import six
import pytest
import collections

import tsv


def test_un():
    source = '\n'.join([
        r'1	a',
        r'2	\t',
        r'3	\n',
        r'4	\\',
        r'5	\N',
        r'6	\j',
        r'',
    ])
    assert list(tsv.un(source)) == [
        ['1', 'a'],
        ['2', '\t'],
        ['3', '\n'],
        ['4', '\\'],
        ['5', None],
        ['6', 'j'],
    ]


def test_un_namedtuple_row_holder():
    Row = collections.namedtuple('Row', 'x,y')
    assert list(tsv.un('1\ta\n', Row)) == [Row(x='1', y='a')]


def test_un_namedtuple_error():
    Row = collections.namedtuple('Row', 'x,y')
    with pytest.raises(ValueError):
        list(tsv.un('1\n', Row))
    with pytest.raises(ValueError):
        list(tsv.un('1\ta\tb\n', Row))


def test_un_with_inconsistent_number_of_fields():
    source = [
        '1',
        '2\t3',
    ]

    # Number of fields of all rows should be equal to number of fields in the
    # first row.
    with pytest.raises(ValueError) as excinfo:
        list(tsv.un(source))
    assert str(excinfo.value) == 'Expected 1 fields in line 2, saw 2'

    # If error_bad_lines is turned off, bad lines are simply skipped.
    with pytest.warns(UserWarning) as warns:
        assert list(tsv.un(source, error_bad_lines=False)) == [['1']]
        assert len(warns) == 1
        assert str(warns[0].message) == 'Expected 1 fields in line 2, saw 2'


def test_final_backslash_error():
    with pytest.raises(tsv.FinalBackslashInFieldIsForbidden):
        list(tsv.un('1\t\\\n'))


def test_to():
    table = [
        (1, 'a'),
        (2, '\t'),
        (3, '\n'),
        (4, '\\'),
        (5, '\\\\'),
        (6, None),
    ]
    output = six.StringIO()
    tsv.to(table, output)
    assert output.getvalue() == '\n'.join([
        r'1	a',
        r'2	\t',
        r'3	\n',
        r'4	\\',
        r'5	\\\\',
        r'6	\N',
        r'',
    ])


def test_to_string():
    assert list(tsv.to([(1, 2)])) == ['1\t2']
