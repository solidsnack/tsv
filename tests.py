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
    # XXX: https://github.com/solidsnack/tsv/issues/3
    Row = collections.namedtuple('Row', 'x,y')
    assert list(tsv.un('1\n', Row)) == [None]
    assert list(tsv.un('1\ta\tb\n', Row)) == [None]


def test_un_with_inconsistent_number_of_fields():
    source = [
        '1',
        '1\t2',
    ]
    assert list(tsv.un(source)) == [['1'], ['1', '2']]


def test_un_custom_row_holder_error():
    with pytest.raises(ValueError):
        tsv.un('1\ta\n', object)


def test_final_backslash_error():
    with pytest.raises(tsv.FinalBackslashInFieldIsForbidden):
        list(tsv.un('1\t\\\n'))


def test_to():
    table = [
        (1, 'a'),
        (2, '\t'),
        (3, '\n'),
        (3, '\\'),
        (4, None),
    ]
    output = six.StringIO()
    tsv.to(table, output)
    assert output.getvalue() == '\n'.join([
        r'1	a',
        r'2	\t',
        r'3	\n',
        r'3	\\',
        r'4	\N',
        r'',
    ])


def test_to_string():
    assert list(tsv.to([(1, 2)])) == ['1\t2']
