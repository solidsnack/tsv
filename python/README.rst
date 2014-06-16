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

.. code-block:: python
    
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

