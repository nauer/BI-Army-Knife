#! /usr/bin/env python3
# encoding: utf-8
"""
findreplace -- find and replace strings in text files

findreplace is a description

It defines classes_and_methods

@author:     Norbert Auer

@copyright:  Copyright 2016 Acib GmbH, Vienna. All rights reserved.

@license:    license

@contact:    norbert.auer@boku.ac.at
@deffield    updated: Updated
"""

import sys
import os
import re
import tempfile
import shutil

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from argparse import FileType

from collections import defaultdict

__all__ = []
__version__ = '0.1'
__date__ = '2016-07-01'
__updated__ = '2016-07-01'

DEBUG = 0

def start(args):
    if args.out:
        args.out = os.path.abspath(args.out)
    else:
        args.out = os.path.abspath(args.file.name)

    # Translate to bytes
    args.pattern = bytes(args.pattern, encoding="utf8")
    args.replace = bytes(args.replace, encoding="utf8")

    p = re.compile(args.pattern)

    name = ""

    with tempfile.NamedTemporaryFile(delete=False) as f:
        name = f.name
        for line in args.file:
            result = p.search(line)

            if result:
                line = line[0:result.start()] + args.replace + line[result.end():]

            f.write(line)

    # Move to destination
    try:
        shutil.move(name, args.out)
    except IOError as e:
        print("IOError, cannot move file to destination. Check if path is valid and you have the right permissions.",
              file=sys.stderr)


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
        parser.add_argument('-v', '--invert-match', action='store_true',
                            help='Invert the sense of matching, to select non-matching lines.')
        parser.add_argument('-t', '--fixed-strings', action='store_true',
                            help='Interpret PATTERN as a list of fixed strings, separated by newlines, any of which is to be matched.')
        parser.add_argument('pattern', type=str,
                            help='The find pattern.')
        parser.add_argument('replace', type=str, default="",
                            help='Replace the pattern by the replace string.')
        parser.add_argument('file', type=FileType('rb'),
                            help="Any kind of text file.")
        parser.add_argument('out', nargs="?", type=str,
                            help="Output file. If it is not defined the original file will be overwritten.")

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
        sys.argv.append("../test/test_dup.fa")

        sys.argv.append("X(M)_00(7)607503.1")
        sys.argv.append("!")
        sys.argv.append("../test/test_dup2.fa")

    sys.exit(main())
