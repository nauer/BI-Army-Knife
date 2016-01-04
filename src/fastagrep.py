#! /usr/bin/env python3
# encoding: utf-8
"""
fastagrep -- search for a regular expression pattern in fasta headers from a multi fasta file and
extract matching sequences to a new fasta file.

fastagrep is a description

It defines classes_and_methods

@author:     Norbert Auer

@copyright:  Norbert Auer, Vienna. All rights reserved.

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

from collections import defaultdict

__all__ = []
__version__ = '2.3'
__date__ = '2014-09-19'
__updated__ = '2015-11-26'

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


class Fasta():
    gduplicate_header = set()

    def __init__(self):
        self.reset()

    def reset(self):
        self.content = []
        self.header = None
        self.alphabet = defaultdict(int)
        self.md5 = hashlib.md5()

    def add_header(self, header):
        self.header = header

    def get_header(self):
        return self.header

    def is_duplicate(self):
        self.md5.update(self.header.encode('utf8'))

        if self.md5.hexdigest() in Fasta.gduplicate_header:
            return True
        else:
            Fasta.gduplicate_header.add(self.md5.hexdigest())
            return False

    def add_line(self, line):
        self.content.append(line)

    def get_content(self):
        return "\n".join(self.content)

    def get_seq(self):
        return "".join(self.content)

    def get_length(self):
        return len(self.get_seq())

    def get_summary(self):
        l = list(self.get_seq())

        for c in l:
            self.alphabet[c] += 1

        return str(self.get_length()) + "\t" + "|".join([item[0] + ":" + str(item[1]) for item in self.alphabet.items()]) + "\n"

    def get_fasta(self, wide=None):
        if wide is None or wide <= 0:
            return "\n".join([self.header, self.get_content()]) + "\n"
        else:
            l = [self.get_seq()[i:i + wide] for i in range(0, self.get_length(), wide)]
            l.insert(0,self.get_header())
            return "\n".join(l) + "\n"


def start(args):
    if DEBUG:
        print(args)

    pattern = list()
    file_count = 0
    trig = False
    seq_count = 0
    max_seq_length = 0

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
        args.pattern = "."

    # Get search pattern
    if args.pattern is not None:
        pattern.append(re.compile(args.pattern.strip()))
    else:
        for p in args.pattern_list:
            pattern.append(re.compile(p.strip()))

    if args.output:
        f = args.output
    elif args.split is not None:
        f = None
    else:
        f = sys.stdout

    if DEBUG:
        start = time.time()

    header_re = re.compile(args.header_pattern.strip())

    # Write Header for option summary
    if args.summary and f is not None:
        f.writelines("Header\tSeq.length\tAlphabet\n")

    fasta = Fasta()
    seq_count = 0

    # Loop through fasta files
    for fastafile in args.file:
        for line in fastafile:
            line = line.strip()
            # Check if line header
            if header_re.search(line) is not None:
                if trig: # full fasta sequence is valid
                    # Check if duplicate
                    if args.rm_duplicates and fasta.header is not None:
                        trig = not fasta.is_duplicate()

                    # Filter for max_length
                    if args.max_length > 0:
                        if fasta.get_length() > args.max_length:
                            trig = False

                    # Filter for min_length
                    if args.min_length > 0:
                        if fasta.get_length() < args.min_length:
                            trig = False

                    # Write output if trig is True
                    if trig:
                        # Cut content to max size
                        if args.max_size >= 0:
                            seq_len = 0
                            new_content = []

                            for row in fasta.get_content():
                                seq_len += len(row)

                                if seq_len > args.max_size:
                                    new_content.append(row[0:len(row) - (seq_len - args.max_size)])
                                else:
                                    new_content.append(row)

                            fasta.content = new_content

                        # Split multi-fasta into smaller fasta files
                        if args.split is not None:
                            # Add sequence length to max_seq_length
                            max_seq_length += fasta.get_length()

                            if (max_seq_length > args.max_seq_length and args.max_seq_length > 0) or seq_count >= args.max_sequences:
                                if seq_count >= 0:
                                    seq_count = 0
                                else:
                                    pass # TODO warning 1.sequence is already longer than max_seq_length

                            if seq_count == 0:
                                if f is not None:
                                    f.close()

                                if seq_count >= args.max_sequences or max_seq_length > args.max_seq_length:
                                    max_seq_length = fasta.get_length()

                                f = open(os.path.join(args.split, "".join([args.prefix, str(file_count),
                                                                           file_extension])), 'w')

                                file_count += 1
                                # seq_count = 0

                                # Write Header for option summary
                                if args.summary:
                                    f.writelines("Header\tSeq.length\tAlphabet\n")

                            seq_count += 1

                        # Write data
                        if args.summary is False and args.summary_no_header is False:
                            f.write(fasta.get_fasta(args.line_length))
                        else:
                            f.write(fasta.get_header() + "\t" + fasta.get_summary())

                # Reset trig
                trig = False

                # Loops through all patterns
                is_in = False

                for p in pattern:
                    if args.fixed_strings:
                        if p.pattern == line:
                            is_in = True
                            break
                    else:
                        if p.search(line) is not None:
                            is_in = True
                            break

                if is_in != args.invert_match:
                    # New header is valid
                    trig = True
                    # Reset fasta object
                    fasta.reset()
                    fasta.add_header(line)
            else:
                if trig:
                    fasta.add_line(line)

    # Write last fasta sequence
    if trig:
        # Check if duplicate
        if args.rm_duplicates and fasta.header is not None:
            trig = not fasta.is_duplicate()

        # Filter for max_length
        if args.max_length > 0:
            if fasta.get_length() > args.max_length:
                trig = False

        # Filter for min_length
        if args.min_length > 0:
            if fasta.get_length() < args.min_length:
                trig = False

        # Write output if trig is True
        if trig:
            # Cut content to max size
            if args.max_size >= 0:
                seq_len = 0
                new_content = []

                for row in fasta.get_content():
                    seq_len += len(row)

                    if seq_len > args.max_size:
                        new_content.append(row[0:len(row) - (seq_len - args.max_size)])
                    else:
                        new_content.append(row)

                fasta.content = new_content

            # Split multi-fasta into smaller fasta files
            if args.split is not None:
                # Add sequence length to max_seq_length
                max_seq_length += fasta.get_length()

                if (max_seq_length > args.max_seq_length and args.max_seq_length > 0):
                    if seq_count >= 0:
                        seq_count = 0
                    else:
                        pass # TODO warning 1.sequence is already longer than max_seq_length

                if seq_count == 0:
                    if f is not None:
                        f.close()

                    if seq_count >= args.max_sequences or max_seq_length > args.max_seq_length:
                        max_seq_length = fasta.get_length()

                    f = open(os.path.join(args.split, "".join([args.prefix, str(file_count),
                                                               file_extension])), 'w')

                    file_count += 1
                    seq_count = 0

                    # Write Header for option summary
                    if args.summary:
                        f.writelines("Header\tSeq.length\tAlphabet\n")

                seq_count += 1

            # Write data
            if args.summary is False and args.summary_no_header is False:
                f.write(fasta.get_fasta(args.line_length))
            else:
                f.write(fasta.get_header() + "\t" + fasta.get_summary())

    if DEBUG:
        print("Current working directory:".format(os.getcwd()))
        print(args)
        end = time.time()
        print(end - start)
        #print("TATA:" + fasta.header)
        #print(fasta.get_content())
        #print(fasta.get_summary())

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
                           help='Path to file with multiple patterns. One pattern per line', type=FileType('r'))
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument('-v', '--invert-match', action='store_true',
                            help='Invert the sense of matching, to select non-matching lines.')
        parser.add_argument('-t', '--fixed-strings', action='store_true',
                            help='Interpret PATTERN as a list of fixed strings, separated by newlines, any of which is to be matched.')
        parser.add_argument('file', nargs='+', type=FileType('r'), default='-',
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
        parser.add_argument('-L', '--line-length',  default=None, type=int,
                            help='Max character length of output line. Default is same output as input.')
        parser.add_argument('-f', '--min-length',  default=0, type=int, help='Filter sequences smaller --min_length.')
        parser.add_argument('-F', '--max-length',  default=0, type=int, help='Filter sequences bigger --max_length.')
        group2.add_argument('-m', '--max-seq-length',  default=0, type=int, help='Create a new file when summary of sequences exceed --max-seq-length. Only used with option -O.')

        # Process arguments
        args = parser.parse_args()

        start(args)

        #if verbose > 0:
        #    print("Verbose mode on")

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
        #sys.argv.append("-v")

        # sys.argv.append("-t")
        # sys.argv.append("-x")
        # sys.argv.append("79")
        sys.argv.append("-O")
        #sys.argv.append("test.fna")
        # sys.argv.append("../test/pattern_list")
        #sys.argv.append("-l")
        #sys.argv.append("../test/list")
        # sys.argv.append("--")
        # sys.argv.append("tata")
        sys.argv.append("-z")
        sys.argv.append("3")
        sys.argv.append("-m")
        sys.argv.append("24")
        # sys.argv.append("-F")
        # sys.argv.append("250")
        # sys.argv.append("-L")
        # sys.argv.append("52")
        #sys.argv.append("-e")
        #sys.argv.append(".*")
        #sys.argv.append("([^\t]*)\tgi\|(\d+).*?([^|]+)\|$")
        #sys.argv.append("/home/nauer/Projects/Proteomics/Scripts/snakemake/proto/test/output1.fna")
        #sys.argv.append("/home/nauer/Projects/Proteomics/Scripts/snakemake/proto/test/output2.fna")
        #sys.argv.append("/home/nauer/Projects/Proteomics/Scripts/snakemake/proto/test/output3.fna")
        #sys.argv.append("/home/nauer/Projects/Proteomics/Scripts/snakemake/proto/test/output6.fna")
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
