#! /usr/bin/env python3
# encoding: utf-8
'''
linegrep -- grep lines from stdoutput or file and extract matching groups to csv

linegrep is a description

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

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from argparse import FileType

from operator import itemgetter

__all__ = []
__version__ = 1.0
__date__ = '2014-06-04'
__updated__ = '2015-01-31'

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
    if(DEBUG):
        print(args.pattern)
        
    #if(len(args.pattern) == 0 and len(args.split) == 0):
    #    sys.stderr.write("Minimum   for help use --help")
              
    pattern = []
    
    for p in args.pattern:
        pattern.append(re.compile(p))

    if args.output:
        f = args.output
    else:
        f = sys.stdout
            
    i = 1
    if args.fr:
        i = args.fr -1
        for i in range(args.fr - 1):
            args.file.readline()
            
    results = []

    for line in args.file:
        i = i + 1

        if args.to is not None and args.to < i:
            break

        groups = ()
        
        # Process pattern
        for p in pattern:
            rematch = p.search(line)
            
            if rematch:
                if len(rematch.groups()) == 0:
                    groups = ()
                    break
                
                groups = groups + rematch.groups()
            else:
                groups = ()
                break
        
        # Process split
        splitres = None
        if args.split:
            split1 = re.compile(args.split[0])
            split2 = re.compile(args.split[1])
            rematch = split1.search(line)
                        
            if rematch:
                if len(rematch.groups()) > 0:
                    splitres = split2.split("".join(list(rematch.groups())))

            if splitres is not None:
                for s in splitres:
                    results.append(groups + (s,))
            #else:
            #    results = []
                
        if args.unmatch:
            args.unmatch[0].write(line) 
                  
    if len(results) > 0:            
        # Group and Count
        if args.group:
            results = [l + (results.count(l),) for l in set(results)]
            
        # Sort
        if args.sort is not None:
            # First -s value is the main sorter therefore the last sort
            results.reverse()
            
            for s in args.sort:
                if abs(s) > len(results[0]):
                    print("WARNING: -s {0} is ignored. Result has only {1} columns.".format(s,len(results[0])), file=sys.stderr)
                elif abs(s) == 0:
                    print("WARNING: -s {0} is ignored. Columns start with index 1.".format(s,len(results[0])), file=sys.stderr)
                else:
                    results = sorted(results, key=itemgetter(abs(s)-1),reverse=s<0)

        # Write results
        for line in results:
            f.write(args.delimiter.join(map(str,line)) + '\n')

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
        #parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")        
        parser.add_argument('-V', '--version', action='version', version=program_version_message)    
        parser.add_argument('-p', '--pattern', nargs='+', help="Grep pattern.",type=str, default=['.*'])
        parser.add_argument('-r', '--split', nargs=2, help="Split pattern. First pattern for sequence to split. Second pattern for split.",type=str)
        parser.add_argument('file', nargs='?', type=FileType('r'), default='-', help="File to grep. Leave empty or use '-' to read from Stdin.")
        parser.add_argument('-d', '--delimiter', help='Set the delimiter for the output',type=str, default='\t')
        parser.add_argument('-f', '--from', dest='fr', help='Skip N-1 lines from begin of file. Use also the --to option to limit input',type=int)
        parser.add_argument('-t', '--to', help='Read only to this line. All other lines are skipped.',type=int)
        parser.add_argument('-o', '--output', help='Use output file instead of stdout',type=FileType('w'))
        parser.add_argument('-g', '--group', help='Instead of normal input identical lines are grouped together and an additional column is added with the group count.', action='store_true')
        parser.add_argument('-s', '--sort', nargs='+', help='Set columns for sorting. Use + or - to set descending or ascending order i.e -s -2 3 for sorting column 2 in descending order and than column 3 in ascending order.',type=int)
        parser.add_argument('-u', '--unmatch', nargs=1, type=FileType('w'), help="Write unmatched lines into file.")

        # Process arguments
        args = parser.parse_args()

        if DEBUG:
            print(args)

        start(args)

        #if verbose > 0:
        #    print("Verbose mode on")

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
        sys.argv.append("-d")
        sys.argv.append("\t")
        sys.argv.append("-g")
        #sys.argv.append("-f")
        #sys.argv.append("5")
        #sys.argv.append("-t")
        #sys.argv.append("6")
        sys.argv.append("-s")
        sys.argv.append("1")        
        sys.argv.append("-2")
        sys.argv.append("-0")
        sys.argv.append("2")
        sys.argv.append("0")
        sys.argv.append("-u")
        sys.argv.append("../test/unmatch.output") 
        sys.argv.append("-p")
        sys.argv.append("EMORG:(AF[^\s]*)")
        sys.argv.append("(\d+\.\d*)")
        #sys.argv.append("-p")
        #sys.argv.append("(ORG:)")
        sys.argv.append("-r")
        sys.argv.append("(.*)")
        sys.argv.append("\s+")
        sys.argv.append("--")
        sys.argv.append("../test/test.blast")

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
