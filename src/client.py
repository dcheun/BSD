#!/usr/bin/env python

"""Sample client.

Sample client that uses the qc module to run the DATAnalyzer.

@author:     Danny Cheun
@copyright:  2014 Danny Cheun and Blackstone Discovery.
             Proprietary software.
@contact:    dcheun@gmail.com

"""

import sys

from bsd.qc import DATAnalyzer

# Export on *
__all__ = []


def main():
    dat_file = sys.argv[1]
    analyzer = DATAnalyzer()
    analyzer.analyze(dat_file)
    analyzer.print_report()

if __name__ == '__main__':
    main()

