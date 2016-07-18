#! /usr/bin/env python3
# encoding: utf-8
"""
findprimer3 -- search for unique primer pairs in fasta files. Wraps primer3 application

findprimer3 is a description

It defines classes_and_methods

@author:     Norbert Auer

@copyright:  Copyright 2016 Acib GmbH, Vienna. All rights reserved.

@license:    license

@contact:    norbert.auer@boku.ac.at
@deffield    updated: Updated
"""

import sys
import os
import time
import re
import tempfile
import shutil

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from argparse import FileType
from BioHelper import Primer3, Fasta, MultiFasta, Alphabeth
from Bio import SearchIO
import glob

from collections import defaultdict

__all__ = []
__version__ = '0.1'
__date__ = '2016-07-04'
__updated__ = '2016-07-04'

DEBUG = 1

# Primer orig Settings
primer3_settings = {
b'PRIMER_TASK' : b"pick_detection_primers",
b'PRIMER_PICK_LEFT_PRIMER' : b"1",
b'PRIMER_PICK_RIGHT_PRIMER' : b"1",
b'PRIMER_OPT_SIZE' : b"20",
b'PRIMER_MIN_SIZE' : b"18",
b'PRIMER_MAX_SIZE' : b"22",
b'PRIMER_MAX_NS_ACCEPTED' : b"1",
#b'PRIMER_PAIR_0_PRODUCT_SIZE' : b"500",
#b'PRIMER_PAIR_4_PRODUCT_SIZE' : b"10000",
b'PRIMER_EXPLAIN_FLAG' : b"1",
b'PRIMER_MAX_GC' : b"60",
b'PRIMER_MIN_GC' : b"40",
b'PRIMER_OPT_GC_PERCENT' : b"50",
b'PRIMER_OPT_TM' : b"60",
b'PRIMER_MAX_TM' : b"62",
b'PRIMER_MIN_TM' : b"55",
b'PRIMER_PAIR_MAX_DIFF_TM' : b"1",
b'PRIMER_NUM_RETURN' : b"5"}

# PRIMER 3 Settings
# primer3_settings = {
# b'PRIMER_TASK' : b"pick_detection_primers",
# b'PRIMER_PICK_LEFT_PRIMER' : b"1",
# b'PRIMER_PICK_RIGHT_PRIMER' : b"1",
# b'PRIMER_OPT_SIZE' : b"20",
# b'PRIMER_MIN_SIZE' : b"17",
# b'PRIMER_MAX_SIZE' : b"23",
# b'PRIMER_MAX_NS_ACCEPTED' : b"1",
# #b'PRIMER_PAIR_0_PRODUCT_SIZE' : b"500",
# #b'PRIMER_PAIR_4_PRODUCT_SIZE' : b"10000",
# b'PRIMER_EXPLAIN_FLAG' : b"1",
# b'PRIMER_MAX_GC' : b"65",
# b'PRIMER_MIN_GC' : b"35",
# b'PRIMER_OPT_GC_PERCENT' : b"50",
# b'PRIMER_OPT_TM' : b"60",
# b'PRIMER_MAX_TM' : b"64",
# b'PRIMER_MIN_TM' : b"53",
# b'PRIMER_PAIR_MAX_DIFF_TM' : b"2",
# b'PRIMER_NUM_RETURN' : b"5"}

def start(args):
    p3 = Primer3()
    not_unique_primers = MultiFasta()
    unique_primers = MultiFasta()
    fastas = MultiFasta()
    fastas.load_fasta(file_obj=args.file)

    result = None

    # for fasta in fastas:
    #     print("Get left primers: " + fasta.get_header().decode())
    #     p3.get_primer_stat(fasta, args.primer_length)
    #     print("Get rigth primers: " + fasta.get_header().decode())
    #     p3.get_primer_stat(fasta, args.primer_length, type='right')

    # primer_list = p3.get_primer_list()
    #
    # for key in primer_list:
    #     unique_primer = primer_list[key]
    #
    #     h = b"|".join([b":".join(zip_item + (unique_primer['type'],)) for zip_item in zip(unique_primer['id'],
    #                                                             [str(i).encode() for i in unique_primer['start']])])
    #
    #     if p3.get_primer_list()[key]['count'] == 1:
    #         unique_primers.add_fasta(Fasta(b"UNIQUE_PRIMER " + h, key))
    #     else:
    #         not_unique_primers.add_fasta(Fasta(b"PRIMER_MISPRIMING_LIBRARY " + h, key))
    # not_unique_primers.add_fasta(Fasta(b"PRIMER_MISPRIMING_LIBRARY " + h, key))
    # unique_primers.save_fasta(args.unique_primers)

    # start = time.time()
    # print("Get not unique Primers")
    # # Create PRIMER_MISPRIMING_LIBRARY
    # i = 0
    # for key, not_unique_primer in [(key, p3.get_primer_list()[key]) for key in p3.get_primer_list() if p3.get_primer_list()[key]['count'] != 1]:
    #     h = b"|".join([b":".join(zip_item + (not_unique_primer['type'],))
    #                    for zip_item in zip(not_unique_primer['id'],
    #                                        [str(i).encode() for i in not_unique_primer['start']])])
    #
    #     not_unique_primers.add_fasta(Fasta(b"PRIMER_MISPRIMING_LIBRARY " + h, key))
    #
    # end = time.time()
    # print(end - start)
    #
    #
    # not_unique_primers.save_fasta(args.mispriming_library)
    #
    # start = time.time()
    # print("Get unique Primers")
    #
    # for key, unique_primer in [(key, p3.get_primer_list()[key]) for key in p3.get_primer_list() if
    #                            p3.get_primer_list()[key]['count'] == 1]:
    #     h = b"|".join([b":".join(zip_item + (unique_primer['type'],))
    #                    for zip_item in zip(unique_primer['id'],
    #                                        [str(i).encode() for i in unique_primer['start']])])
    #
    #     unique_primers.add_fasta(Fasta(b"UNIQUE_PRIMER " + h, key))
    #
    # end = time.time()
    # print(end - start)

    #pat = re.compile(b"(AGCATGATGATTGGCGAGCT)|(CCACGTTGCCCATATCCTGT)|(TTCCCTTGACAGACCTCTCTAA)|(TGTACCTACAAGGGTGAGCT)")

    #for fasta in fastas:
    #    print(pat.findall(fasta.get_sequence()))
    #    print(pat.findall(fasta.get_reverse_transcript_sequence()))

    #exit()
    #myfastas = MultiFasta()
    #myfastas.add_fasta(fastas[9])
    #myfastas.add_fasta(fastas[7])
    #myfastas.save_fasta("issued7.fa")
    #exit()
    #
    #myfastas.remove_all()
    #myfastas.add_fasta(fastas[9][33527:])
    # myfastas.add_fasta(Fasta(fastas[12].get_header() + b" Reversed", fastas[12].get_reverse_transcript_sequence()))
    #myfastas.save_fasta("issue_831.9.fa")
    #exit()
    #
    # myfastas.remove_all()
    # myfastas.add_fasta(fastas[4][342385:366876])
    # myfastas.add_fasta(Fasta(fastas[13].get_header() + b" Reversed", fastas[13].get_reverse_transcript_sequence()))
    # myfastas.save_fasta("issued3.fa")
    #
    # myfastas.remove_all()
    # myfastas.add_fasta(fastas[5][667158:678030])
    # myfastas.add_fasta(fastas[14])
    # #myfastas.add_fasta(Fasta(fastas[15].get_header() + b" Reversed", fastas[15].get_reverse_transcript_sequence()))
    # myfastas.add_fasta(fastas[2][:14126])
    # myfastas.save_fasta("issued4.fa")
    #
    # myfastas.remove_all()
    # myfastas.add_fasta(fastas[14])
    # myfastas.add_fasta(Fasta(fastas[15].get_header() + b" Reversed", fastas[15].get_reverse_transcript_sequence()))
    # # myfastas.add_fasta(fastas[2][:14126])
    # myfastas.save_fasta("issued6.fa")
    #
    # myfastas.remove_all()
    # myfastas.add_fasta(fastas[4][1090477:1115525])
    # myfastas.add_fasta(fastas[16])
    # myfastas.save_fasta("issued5.fa")

    data = read_blat(args.pls)

    primer3_settings[b'PRIMER_MISPRIMING_LIBRARY'] = bytes(args.mispriming_library.encode())

    #print(data.keys())
    primer3_settings[b'PRIMER_PRODUCT_SIZE_RANGE'] = args.product_size.encode()

    for fasta in fastas:
        try:
            primer3_settings[b'SEQUENCE_EXCLUDED_REGION'] = data[fasta.get_header().split()[0].decode()].encode()
            print(data[fasta.get_header().split()[0].decode()].encode())
        except:
            print("No exclude regions in {}".format(fasta.get_header().split()[0].decode()))
            primer3_settings[b'SEQUENCE_EXCLUDED_REGION'] = b""

        primer3_settings[b'SEQUENCE_ID'] = fasta.get_header()
        primer3_settings[b'SEQUENCE_TEMPLATE'] = fasta.get_sequence()

        print("Run fasta " + fasta.get_header().decode())
        print(len(fasta.get_sequence()))
        p3.run(fasta, primer3_settings)

    args.out.write(p3.get_result())

def read_blat(path):
    data = {}

    for name in glob.glob(path):
        try:
            blat_result = SearchIO.read(name, 'blat-psl')
        except:
            continue

        filter_func = lambda hit: hit.query_span >= 200 and (hit.hit_span <= hit.query_span * 1.2 and hit.query_span <= hit.hit_span * 1.2)

        for hit in blat_result:
            hit = hit.filter(filter_func)
            if hit:
                #print(hit)
                hsp_hit = []
                for hsp in hit:
                    if hsp.query_id != hsp.hit_id:
                    #if hsp.is_fragmented:
                        hsp_hit.append(hsp.query_start)
                        hsp_hit.append(hsp.query_end)

                        print(hsp.query_id, hsp.hit_id, hsp.query_start, hsp.query_end, hsp.hit_start, hsp.hit_end)

                if len(hsp_hit) > 0:
                    ranges = ["{},{} ".format(hsp_hit[i], hsp_hit[i + 1] - hsp_hit[i]) for i in range(0, len(hsp_hit), 2)]
                    if hsp.query_id in data:
                        data[hsp.query_id] += "".join(ranges)
                        #data[hsp.query_id] += "{},{} ".format(min(hsp_hit), max(hsp_hit) - min(hsp_hit))
                    else:
                        data[hsp.query_id] = "".join(ranges)
                        #data[hsp.query_id] = "{},{} ".format(min(hsp_hit), max(hsp_hit) - min(hsp_hit))

                    print(ranges)

    return data


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
        parser.add_argument('file', type=FileType('rb'), default='-', help="Fasta file.")
        parser.add_argument('primer_length', type=int, help='Length of the primer.')
        parser.add_argument('product_size', type=str, help='Product size range [500-2000]. Includes also the primer length')
        parser.add_argument('pls', type=str, help='Path for pls files')
        parser.add_argument('-m','--mispriming-library', type=str, default='PRIMER_MISPRIMING_LIBRARY.fa',
                            help="Path to primer3 mispriming library.")
        parser.add_argument('-u', '--unique-primers', type=str, default='UNIQUE_PRIMERS.fa',
                            help="Path to unique primer output.")

        parser.add_argument('out', type=FileType('wb'), default='-',
                            help="Output file. If it is not defined output will bes send to the terminal.")

        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument('-v', '--invert-match', action='store_true',
                            help='Invert the sense of matching, to select non-matching lines.')

        parser.add_argument('--max-GC', default=60, type=int, help='Max GC content.')
        parser.add_argument('--min-GC', default=40, type=int, help='Min GC content.')

        # Process arguments
        args = parser.parse_args()

        start(args)

        return 0
    except KeyboardInterrupt:
        # handle keyboard interrupt Easy to use parsing tools.###
        return 0
    except Exception as e:
        if DEBUG:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("/home/nauer/Projects/PrimerDesign/Sources/pirc_C9.fa")

        sys.argv.append("20")
        sys.argv.append("500-10000")
        sys.argv.append("/home/nauer/Projects/PrimerDesign/Results/*psl")
        sys.argv.append("-m")
        sys.argv.append("/home/nauer/Projects/PrimerDesign/Sources/PRIMER_MISPRIMING_LIBRARY.fa")
        sys.argv.append("-u")
        sys.argv.append("/home/nauer/Projects/PrimerDesign/Sources/UNIQUE_PRIMERS.fa")
        sys.argv.append("/home/nauer/Projects/PrimerDesign/Results/primers.csv")

    sys.exit(main())