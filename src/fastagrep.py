#! /usr/bin/env python3
# encoding: utf-8
'''
fastagrep -- search for a regular expression pattern in fasta headers from a multi fasta file and 
extract matching sequences to a new fasta file.

fastagrep is a description

It defines classes_and_methods

@author:     Norbert Auer
        
@copyright:  2014 University of Natural Resources and Life Sciences, Vienna. All rights reserved.
        
@license:    license

@contact:    norbert.auer@boku.ac.at
@deffield    updated: Updated
'''

import sys
import os
import re
import time

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from argparse import FileType
#from itertools import cycle
#from multiprocessing import Pool

__all__ = []
__version__ = 1.1
__date__ = '2014-09-19'
__updated__ = '2014-09-23'

DEBUG = 0
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
    pattern = list()
    
    # Get search pattern
    if args.pattern is not None:        
        pattern.append(re.compile(args.pattern.strip()))
    else:
        for p in args.pattern_list:
            pattern.append(re.compile(p.strip()))
    
    if args.output:
        f = args.output    
    else:
        f = sys.stdout
      
    if DEBUG:
        start = time.time()
        
    # Loop through fasta files
    for fastafile in args.file:
        for line in fastafile:
            # Check if line header
            if line.startswith('>'):
                trig = False 
                
                result = list()
                
                #Loops through all patterns
                for p in pattern:                                        
                    result.append(p.search(line))
                if len(list(filter(None, result))) > 0:                
                    trig = True
                    
            if trig:
                f.writelines(line)   
                
    if DEBUG:
        end = time.time()
        print(end-start)                                      

# Overhead is too big
# with Pool(processes=args.processors) as pool:     
# result=pool.map(grepSeq,zip(pattern,cycle((line,))))            
# def grepSeq(data):             
#    if data[0].search(data[1]) is not None:        
#        return(True)
#    else:
#        return(False)
        
        
        
        
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
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-e', '--pattern', help='Single regular expression pattern to search for',type=str)
        group.add_argument('-l', '--pattern-list',nargs='?', help='Path to file with multiple patterns. One pattern per line',type=FileType('r'))
        parser.add_argument('-V', '--version', action='version', version=program_version_message)            
        parser.add_argument('-o', '--output', help='Use output file instead of stdout',type=FileType('w'))        
        #parser.add_argument('-p', '--processors', default=None, help='How many processors should be used [Default: As many as possible]',type=int)
        parser.add_argument('file', nargs='+', type=FileType('r'), default='-', help="File from type fasta. Leave empty or use '-' to read from Stdin or pipe.")
        
        # Process arguments
        args = parser.parse_args()
        
        if DEBUG:
            print(args)
            
        start(args)
        
        #if verbose > 0:
        #    print("Verbose mode on")
                 
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt Easy to use parsing tools.###
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
        #sys.argv.append("-V")
        #sys.argv.append("-s")
        #sys.argv.append("5")
        #sys.argv.append("-l")
        #sys.argv.append("../test/pattern_list")
        sys.argv.append("-e")
        sys.argv.append("XM_003495338")
        #sys.argv.append("([^\t]*)\tgi\|(\d+).*?([^|]+)\|$")
        sys.argv.append("../test/test.fa")
                
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
