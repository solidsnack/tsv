.. image:: https://travis-ci.org/solidsnack/tsv.svg?branch=master
    :target: https://travis-ci.org/solidsnack/tsv

`Linear TSV`__ is a line-oriented, portable tabular data format. Tabular data
-- rows of tuples, each of the same length -- is commonly stored as CSV and is
the lingua franca of spreadsheets, databases and analysis tools.

__ http://dataprotocols.org/linear-tsv/

CSV is almost but not quite line-oriented, because newlines are quoted, not
escaped. In the TSV format presented here, escape codes are used for newlines
and tabs in field data, allowing naive filtering with line-oriented shell
tools like ``sort``, ``fgrep`` and ``cut`` to work as expected. In all of its
details, the format derives from the ``TEXT`` serialization mode of Postgres
and MySQL.

----------
Python API
----------

.. code:: python

    from collections import namedtuple
    import sys

    import tsv


    # Simplest access mode: parse a text stream (strings are okay, too) to a
    # generator of lists of strings.
    lists = tsv.un(sys.stdin)


    # Parse each row as a particular class derived with namedtuple()
    class Stats(namedtuple('Stats', ['state', 'city', 'population', 'area'])):
        pass

    tuples = tsv.un(sys.stdin, Stats)


    # Format a collection of rows, getting back a generator of strings, one
    # each row. Any parseable type is okay.
    strings = tsv.to(lists)
    strings = tsv.to(tuples)

    # Write the rows to a handle:
    strings = tsv.to(tuples, sys.stdout)


    # CSV compatible API (reader/writer)
    with open('eggs.tsv', 'w') as tsvfile:
        spamwriter = tsv.writer(tsvfile)
        spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
        spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

    with open('eggs.tsv') as tsvfile:
        spamreader = tsv.reader(tsvfile)
        for row in spamreader:
            print(', '.join(row))


    # CSV compatible API (DictReader/DictWriter)
    with open('names.tsv', 'w') as tsvfile:
        fieldnames = ['first_name', 'last_name']
        writer = tsv.DictWriter(tsvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
        writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
        writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

    with open('names.tsv') as tsvfile:
        reader = tsv.DictReader(tsvfile)
        for row in reader:
            print(row['first_name'], row['last_name'])

------------------
Format Description
------------------

In this format, all records are separated by ASCII newlines (``0x0a``) and
fields within a record are separated with ASCII tab (``0x09``). It is permitted
but discouraged to separate records with ``\r\n``.

To include newlines, tabs, carriage returns and backslashes in field data, the
following escape sequences must be used:

* ``\n`` for newline,

* ``\t`` for tab,

* ``\r`` for carriage return,

* ``\\`` for backslash.

To indicate missing data for a field, the character sequence ``\N`` (bytes
``0x5c`` and ``0x4e``) is used. Note that the ``N`` is capitalized. This
character sequence is exactly that used by SQL databases to indicate SQL
``NULL`` in their tab-separated output mode.

~~~~~~~~~~~~~~~~~~~~~~~~~
A Word About Header Lines
~~~~~~~~~~~~~~~~~~~~~~~~~

There are no header lines specified by this format. One objection to them is
that they break the naive concantenation of files. Another is that they are
anithetical to stream processing. Yet another is that one generally wants more
than column names -- one wants at least column types. Better to do nothing
than too little.

----------
Motivation
----------

In advocating a shift to a line-oriented, tab-separated serialization format,
we are endorsing an existing format: the default serialization format of both
Postgres and MySQL. We propose to standardize a subset of the format common to
both database systems.

A truly line-oriented format for tabular data, where newline, carriage return
and the separator are always represented by escape sequences, offers many
practical advantages, among them:

* The parsers are simple and fast.

* First pass filtering and sorting for line-oriented formats is easy to
  implement in high-level languages, like Python and Java.

* Analysis and transformation of line-oriented data with command line tools is
  simple, dependable and often surprisingly efficient.

* By requiring escape sequences when newlines and tabs are in field text, the
  format allows parsers to naively and efficiently split data on raw byte
  values: ``0x09`` for fields and ``0x0a`` for records.

CSV is almost right and it's worth talking about the disadvantages of CSV that
motivate the author to promote another tabular data format:

* In some locales, ``,`` is the decimal separator; whereas the ASCII tab never
  collides with the decimal separator. More generally, the tab is not a
  centuries old glyph that one encounters in natural language.

* CSV is not truly line-oriented -- newlines are quoted, not escaped. A single
  record can span multiple physical lines. In consequence, line-oriented
  processing almost works until it doesn't, and then simple tricks -- sorting
  on the first column to optimize insertion order or batching records in to
  groups of a few thousand to get better insert performance -- require
  relatively complicated code to get right.

* CSV's quoting style requires one to mingle field data parsing and record
  splitting. Taking every third record still requires one to parse the prior
  two, since a newline inside quotes is not a record separator.

* CSV is ambiguous in many small areas -- the presence or absence of a header
  line, the choice of quote character (single or double?) and even the choice
  of separator character are all axes of variability.

----------------------------
Sample Parsers & Serializers
----------------------------

A few sample parsers are included in the distribution.

Bash
  ``tsv.bash < cities10.tsv``

Python
  ``example.py < cities10.tsv``

-------
Grammar
-------

This grammar is presented in the W3C EBNF format.

.. code:: bnf

    TSV        ::= Row (NL Row)*

    /* This form may be read but not written by conforming implementations. */
    TSVInput   ::= Row (CR? NL Row)*

    Row        ::= Field (Tab Field)*
    Field      ::= (Escape|NoOpEscape|PlainChar)*

    Char       ::= [http://www.w3.org/TR/xml#NT-Char]
    PlainChar  ::= Char - (NL|Tab|CR|'\')
    NL         ::= #x0A
    CR         ::= #x0D
    Tab        ::= #x09

    Escape     ::= '\n' | '\r' | '\t' | '\\'
    NoOpEscape ::= '\' (Char - ('n'|'r'|'t'|'\'))

A diagram of the grammar can be generated online with the
`Bottlecaps Railroad Diagram generator`__.

__ http://bottlecaps.de/rr/ui

