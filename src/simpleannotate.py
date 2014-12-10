#! /usr/bin/env python3
# encoding: utf-8
'''
simpleannotate -- annotates a given sequence with features presented in a list
and visualise it in a svg file.  

simpleannotate is a description

It defines classes_and_methods

@author:     Norbert Auer
        
@copyright:  2014 University of Natural Resources and Life Sciences, Vienna. All rights reserved.
        
@license:    license

@contact:    norbert.auer@boku.ac.at
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from argparse import FileType

from reportlab.lib import colors
from reportlab.lib.units import cm
from Bio.Graphics import GenomeDiagram
from Bio import SeqIO
from Bio.SeqFeature import SeqFeature, FeatureLocation


__all__ = []
__version__ = 0.1
__date__ = '2014-10-06'
__updated__ = '2014-10-06'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def start(args):
    seqrecord = None
    
    try:
        for seq_record in SeqIO.parse(args.input[0], "fasta"):
            seqrecord = seq_record
            break            
    except:        
        args.input[0].close()
        raise    
    
    f1 = SeqFeature(FeatureLocation(15, 10), type="gene")
   

    f2 = SeqFeature(FeatureLocation(50, 110, strand=-1), type="CDS")


    f3 = SeqFeature(FeatureLocation(119, 158, strand=-1), type="CDS")


    features = [f1,f2,f3]
    
    gd_diagram = GenomeDiagram.Diagram("Test")
    gd_track_for_features = gd_diagram.new_track(1, name="Annotated Features")
    gd_feature_set = gd_track_for_features.new_set()

    for feature in features:
        #if feature.type != "gene":
            #Exclude this feature
        #    continue
        if len(gd_feature_set) % 2 == 0:
            color = colors.blue
        else:
            color = colors.lightblue
        gd_feature_set.add_feature(feature, color=color, label=True, sigil="ARROW",
                           arrowshaft_height=0.5, arrowhead_length=0.25)

    gd_diagram.draw(format="linear", orientation="landscape", pagesize='A4',
                fragments=4, start=0, end=len(seqrecord))
    
    gd_diagram.write("plasmid_linear.svg", "SVG")
    print(os.getcwd())
def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

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
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument('-o', '--output', help='Use output file instead of stdout',type=FileType('w'))
        parser.add_argument('input', nargs=1, type=FileType('rU'), default='-', help="Sequence to annotate in fasta format. Only the first sequence is used if more than one sequence is present in the fasta file. Ignore all other sequences. Leave empty or use '-' to read from Stdin.")
        parser.add_argument('features', nargs=1, help="List of features.",type=FileType('r'))
        
        
        # Process arguments
        args = parser.parse_args()

        if DEBUG:
            print(args)

        start(args)

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
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
        #sys.argv.append("-h")
        sys.argv.append("../test/test.fa")
        sys.argv.append("../test/test.features")

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
