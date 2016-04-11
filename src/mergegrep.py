#! /usr/bin/env python3
# encoding: utf-8
"""
mergegrep -- merge tables by joining tables over keys by a grep search
in a second table

@author:     Norbert Auer

@copyright:  ACIB GmbH. All rights reserved.

@license:    license

@contact:    norbert.auer@boku.ac.at
@deffield    updated: Updated
"""

import sys
import os
import re

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from argparse import FileType

__all__ = []
__version__ = '0.1'
__date__ = '2016-04-11'
__updated__ = '2016-04-11'

DEBUG = 0
TESTRUN = 0
PROFILE = 0


class CLIError(Exception):
    """Generic exception to raise and log different fatal errors."""
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def start(args):
    if DEBUG:
        print(args)

    if args.output:
        f_out = args.output
    else:
        f_out = sys.stdout

    tb2 = args.table2.readlines()

    for line1 in args.table1:
        row1 = [item.strip(args.quote1) for item in line1.strip().split(args.delimiter1)]

        pattern = re.compile(row1[args.key1 - 1])

        for line2 in tb2:
            row2 = [item.strip(args.quote2) for item in line2.strip().split(args.delimiter2)]

            if pattern.search(row2[args.key2 - 1].strip(args.quote1)):
                if args.quote is not None:
                    row = [args.quote + item + args.quote for item in row1 + row2]
                else:
                    row = row1 + row2

                f_out.write(args.delimiter.join(row) + "\n")


def main(argv=None): # IGNORE:C0111
    """Command line options."""

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Norbert Auer on %s.
  Copyright 2016 Acib GmbH, Vienna. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)

        parser.add_argument('-V', '--version', action='version', version=program_version_message)

        parser.add_argument('-1', '--table1', type=FileType('r'), required="True",
                            help="Table 1.")
        parser.add_argument('-2', '--table2', type=FileType('r'), required="True",
                            help='Table2.')
        parser.add_argument('--key1', type=int, default=1,
                            help="The column Id from table 1 which should be used for the merge. Default is column 1.")
        parser.add_argument('--key2', type=int, default=1,
                            help="The column Id from table 2 which should be used for the merge. Default is column 1.")
        parser.add_argument('--quote1', type=str, default='"',
                            help="Quote character for table 1. Default is '\"'.")
        parser.add_argument('--quote2', type=str, default='"',
                            help="Quote character for table 1. Default is '\"'.")
        parser.add_argument('-q', '--quote', type=str, default=None,
                            help="Should quotes used for output table? Default is no quoting.")
        parser.add_argument('-o', '--output', help='Use output file instead of stdout.', type=FileType('w'))

        parser.add_argument('--delimiter1',  default='\t', type=str,
                            help='Column Delimiter. Default is tab (\t).')
        parser.add_argument('--delimiter2', default='\t', type=str,
                            help='Column Delimiter. Default is tab (\t).')
        parser.add_argument('-d', '--delimiter', default='\t', type=str,
                            help='Output column delimiter. Default is tab "\t".')

        # Process arguments
        args = parser.parse_args()

        start(args)

        return 0
    except KeyboardInterrupt:
        # handle keyboard interrupt Easy to use parsing tools.###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        # sys.argv.append("-h")
        # sys.argv.append("-v")

        sys.argv.append("-1")
        sys.argv.append("../test/table1.csv")
        sys.argv.append("-2")
        sys.argv.append("../test/table2.csv")
        sys.argv.append("--delimiter1")
        sys.argv.append(",")
        sys.argv.append("--delimiter2")
        sys.argv.append(",")
        sys.argv.append("--key1")
        sys.argv.append("2")
        sys.argv.append("--key2")
        sys.argv.append("2")
        sys.argv.append("-q")
        sys.argv.append('"')
        sys.argv.append("-d")
        sys.argv.append(";")

    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'linegrep_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())