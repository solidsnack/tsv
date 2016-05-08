#!/usr/bin/env python

from collections import namedtuple
import sys

import tsv


def main():
    results = [(pop.location(), pop.density())
               for pop in tsv.un(sys.stdin, Pop) if pop]
    tsv.to(results, sys.stdout)


class Pop(namedtuple('Pop', ['state', 'city', 'population', 'area'])):
    def location(self):
        return '%s (%s)' % (self.city, self.state)

    def density(self):
        if self.population and self.area:
            return float(self.population) / float(self.area)


if __name__ == '__main__':
    main()
