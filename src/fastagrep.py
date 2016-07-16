#! /usr/bin/env python3
# encoding: utf-8
"""
fastagrep -- search for a regular expression pattern in fasta headers from a multi fasta file and
extract matching sequences to a new fasta file.

fastagrep is a description

It defines classes_and_methods

@author:     Norbert Auer

@copyright:  Copyright 2014 University of Natural Resources and Life Sciences, Vienna. All rights reserved.

@license:    license

@contact:    norbert.auer@boku.ac.at
@deffield    updated: Updated
"""

import sys
import os
import re
import time
import hashlib

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from argparse import FileType

from BioHelper import (Fasta, MultiFasta,Alphabeth)

__all__ = []
__version__ = '3.0'
__date__ = '2014-09-19'
__updated__ = '2016-07-16'

DEBUG = 0
TESTRUN = 0
PROFILE = 0


class CLIError(Exception):
    """Generic exception to raise and log different fatal errors."""
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: {}".format(msg)

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg

def start(args):
    pattern = list()
    file_count = 0
    seq_count = 0
    max_seq_length = 0
    duplicate_header = set()

    # Extract filename and file extension
    filename, file_extension = os.path.splitext(args.file[0].name)

    # Check if single sequence output mode
    if args.split is None:
        args.split = '.'
    elif args.split == '-':
        args.split = None

    # Should multi-fasta be splitted
    if args.split is not None:
        if not os.path.exists(args.split):
            raise CLIError("-O {} - Path does not exist".format(args.split))

    # Set default pattern if pattern was not defined
    if args.pattern is None and args.pattern_list is None:
        args.pattern = b"."

    # Get search pattern
    if args.pattern is not None:
        pattern.append(re.compile(args.pattern.strip()))
    else:
        for p in args.pattern_list:
            pattern.append(re.compile(p.strip().encode()))

    # Output to file or stdout or many files
    if args.output:
        f_out = args.output
    elif args.split is not None:
        f_out = None
    else:
        f_out = sys.stdout

    if DEBUG:
        start = time.time()

    # Output to single file no split
    if args.split is not None:
        f_out = open(os.path.join(args.split, "".join([args.prefix, str(file_count), file_extension])), 'w')

    # Loop through fasta files
    for fastafile in args.file:
        for fasta in MultiFasta.read_fasta(file_obj=fastafile, header_pattern=args.header_pattern.strip()):
            trig = True
            h = fasta.get_header()
            # Search for sequences with pattern in header
            for p in pattern:
                if args.fixed_strings:
                    if p.pattern in h:
                        trig = False
                        break
                else:
                    if p.search(h):
                        trig = False
                        break

            # Invert search result
            if args.invert_match:
                trig = not trig

            # If trig false then sequence is in
            if trig:
                continue

            # Remove duplicate sequences with same header
            if args.rm_duplicates:
                md5 = hashlib.md5()
                md5.update(fasta.get_header())

                digest = md5.hexdigest()
                if digest in duplicate_header:
                    continue
                else:
                    duplicate_header.add(digest)

            # Create new fasta by sub sequencing
            if args.start > 0 and args.length > 0:
                fasta = fasta[args.start:args.start + args.length]
            elif args.start > 0:
                fasta = fasta[args.start:]
            elif args.length > 0:
                fasta = fasta[:args.length]

            # Filtering too long sequences
            if args.max_length > 0 and fasta.get_seq_length() > args.max_length:
                continue

            # Filtering too short sequences
            if args.min_length > 0 and fasta.get_seq_length() < args.min_length:
                continue

            # Cutting too long sequences
            if args.max_size >= 0:
                fasta = fasta[0:args.max_size]

            # Create the reverse transcript
            if args.reverse_transcript == "DNA":
                fasta.set_alphabeth(Alphabeth.DNA)
                fasta = Fasta(fasta.get_header(), fasta.get_reverse_transcript_sequence())
            elif args.reverse_transcript == "RNA":
                fasta.set_alphabeth(Alphabeth.RNA)
                fasta = Fasta(fasta.get_header(), fasta.get_reverse_transcript_sequence())

            # Write to more files
            if args.split is not None:
                max_seq_length += fasta.get_seq_length()
                if seq_count >= args.max_sequences or max_seq_length >= args.max_seq_length:
                    f_out.close()
                    f_out = None
                    seq_count = 0
                    max_seq_length = 0
                    file_count += 1

                if f_out is None:
                    f_out = open(os.path.join(args.split, "".join([args.prefix, str(file_count), file_extension])), 'w')

                # Create summary instead normal fasta output
                if args.summary:
                    f_out.writelines("Header\tSeq.length\tAlphabet\n")
                    f_out.write(fasta.get_header().decode() + "\t" + fasta.get_summary())
                elif args.summary_no_header:
                    f_out.write(fasta.get_header().decode() + "\t" + fasta.get_summary())
                else:
                    for line in fasta.get_line_by_line(args.line_length):
                        f_out.write(line + "\n")

            # Write to one file
            else:
                if args.summary:
                    f_out.writelines("Header\tSeq.length\tAlphabet\n")
                    f_out.write(fasta.get_header().decode() + "\t" + fasta.get_summary())
                elif args.summary_no_header:
                    f_out.write(fasta.get_header().decode() + "\t" + fasta.get_summary())
                else:
                    for line in fasta.get_line_by_line(args.line_length):
                        f_out.write(line + "\n")

            seq_count += 1

    if DEBUG:
        print("\n" + "*" * 60 + "\n" + " " * 25 + "DEBUG MODE:\n")
        print("Current working directory: {}".format(os.getcwd()))
        print(args)
        end = time.time()
        print("Runtime: {} sec".format(end - start))
        print("\n" + "*" * 60 + "\n")

def main(argv=None):
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
  Copyright 2014 University of Natural Resources and Life Sciences, Vienna. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        group = parser.add_mutually_exclusive_group()
        group2 = parser.add_mutually_exclusive_group()
        group3 = parser.add_mutually_exclusive_group()
        group.add_argument('-e', '--pattern', help='Single regular expression pattern to search for', type=str)
        group.add_argument('-l', '--pattern-list', nargs='?',
                           help='Path to file with multiple patterns. One pattern per line', type=FileType('rb'))
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument('-v', '--invert-match', action='store_true',
                            help='Invert the sense of matching, to select non-matching lines.')
        parser.add_argument('-t', '--fixed-strings', action='store_true',
                            help='Interpret PATTERN as a list of fixed strings, separated by newlines, any of which is to be matched.')
        parser.add_argument('file', nargs='+', type=FileType('rb'), default='-',
                            help="File from type fasta. Leave empty or use '-' to read from Stdin or pipe.")
        parser.add_argument('-p', '--header-pattern',  default='^>', type=str,
                            help='Use this pattern to identify header line.')
        parser.add_argument('-d', '--rm-duplicates', action='store_true',
                            help='Remove sequences with duplicate header lines. Hold only first founded sequence.')
        group2.add_argument('-s', '--summary', action='store_true',
                            help='Returns instead of the normal output only the header and a summary of the sequence.')
        group2.add_argument('-n', '--summary-no-header', action='store_true',
                            help='Same like summary without starting header line.')
        group3.add_argument('-o', '--output', help='Use output file instead of stdout', type=FileType('w'))
        group3.add_argument('-O', '--split', type=str, default='-', nargs="?",
                            help='Split multi-fasta files in smaller files. Size is 1 by default and is set by -z. Use -r to set name prefix. Default output folder is the current working directory. Add a folder to change directory.')
        parser.add_argument('-r', '--prefix',  default='output', type=str,
                            help='Set name prefix for single sequence output mode. Output file name is set as <prefix>{number}.{input-extention}. Only used with option -O.')
        parser.add_argument('-z', '--max-sequences',  default=1, type=int,
                            help='Set max sequences per file. Size is 1 by default. Only used with option -O.')
        parser.add_argument('-x', '--max-size',  default=-1, type=int,
                            help='Sequences exceeding --max-length were cut.')
        parser.add_argument('-a', '--start', default=-1, type=int, help='Start index of sequence.')
        parser.add_argument('-b', '--length', default=-1, type=int, help='Length of sequence. If --start is not set returns sub sequence from start index 0.')
        parser.add_argument('-T', '--reverse-transcript', type=str,
                            help='Return the reverse transcript. Sequence must be DNA or RNA. {DNA|RNA}')
        parser.add_argument('-L', '--line-length',  default=60, type=int,
                            help='Max character length of output line. Default is same output as input.')
        parser.add_argument('-f', '--min-length',  default=0, type=int, help='Filter sequences smaller --min_length.')
        parser.add_argument('-F', '--max-length',  default=0, type=int, help='Filter sequences bigger --max_length.')
        group2.add_argument('-m', '--max-seq-length',  default=0, type=int,
                            help='Create a new file when summary of sequences exceed --max-seq-length. Only used with option -O.')

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
        sys.argv.append("-m")
        sys.argv.append("290")
        sys.argv.append("-z")
        sys.argv.append("5")
        sys.argv.append("-r")
        sys.argv.append("outt")
        sys.argv.append("-a")
        sys.argv.append("20")
        sys.argv.append("-b")
        sys.argv.append("20")
        sys.argv.append("-L")
        sys.argv.append("60")
        sys.argv.append("-T")
        sys.argv.append("DNA")
        sys.argv.append("--")
        sys.argv.append("../test/test_dup.fa")

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
