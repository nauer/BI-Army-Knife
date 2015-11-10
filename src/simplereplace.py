#! /usr/bin/env python3
# encoding: utf-8
'''
simplereplace -- 

simplereplace is a description

It defines classes_and_methods

@author:     Norbert Auer
        
@copyright:  2015 University of Natural Resources and Life Sciences, Vienna. All rights reserved.
        
@license:    license

@contact:    norbert.auer@boku.ac.at
@deffield    updated: Updated
'''

import sys
import os
import logging
import re

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from argparse import FileType
from urllib.parse import ResultBase

__all__ = []
__version__ = 1.0
__date__ = '2015-07-15'
__updated__ = '2015-07-16'
__author__ = 'Norbert Auer'

DEBUG = 0

class CLIError(Exception):
    """Generic exception to raise and log different fatal errors."""
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg

def _subreturn(match):
    return("." * (match.end() - match.start()))
    
def start(args):
    # Set up logger
    if args.verbose > 0:
        logging.basicConfig(level=logging.INFO)

    if args.output is None:
        # Set output to Stdout
        f = sys.stdout
    else:
        # Set output to file
        f = args.output

    if args.header:
        # Remove Header and write it to output
        f.writelines(args.file.readline())

    try:
        for line in args.file:
            split_list = line.strip().split(args.delimiter)
            
            for pattern in args.pattern:
                tmp = pattern
                tmp = re.subn("(?<![\\\])[[][^]]+[]]",_subreturn, tmp)
                
                slash_pos = [m.start() for m in re.finditer("(?<!\\\)/",tmp[0])]
                
                if len(slash_pos) != 2:
                    sys.exit(-1)
                    
                pat = re.subn("\\\/","/",pattern[slash_pos[0]+1:slash_pos[1]])
                repl = re.subn("\\\/","/",pattern[slash_pos[1]+1:])
                       
                p = {'col':int(pattern[0:slash_pos[0]]) - 1, 
                     'pattern':pat[0], 
                     'repl':repl[0]}
                
                if len(split_list) - 1 >= p['col']:                    
                    split_list[p['col']] = re.subn(p['pattern'],
                                                   p['repl'], 
                                                   split_list[p['col']])[0]
                                                   
            f.write(args.delimiter.join(split_list) + "\n")

    except ValueError:
        logging.error("Value error occurred. Maybe file starts with a header. Use -H/--header option.")
        exit(2)
    except SystemExit as e:
        # this log will include traceback
        logging.exception("Pattern should have this format: 2/[A]../BBB\n")
        # this log will just include content in sys.exit
        logging.error(str(e))
        
    except:
        logging.error("Unexpected error:", sys.exc_info()[0])
        raise
    else:
        f.close()

def main():
    """Command line options."""
    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Norbert Auer on %s.
  Copyright 2015 ACIB GmbH, Graz. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, 
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-V', '--version', action='version', 
                            version=program_version_message)
        parser.add_argument('-v', '--verbose', dest='verbose', action='count',
                            help='Set verbosity level [default: %(default)s]', 
                            default=0)
        parser.add_argument('-o', '--output', 
                            help='Use output file instead of stdout', 
                            type=FileType('w'))
        parser.add_argument('file', type=FileType('r'), default='-',
                            help="""File path name. Leave empty or use '-' to 
                            read from Stdin or pipe.""")
        parser.add_argument('-d', '--delimiter', default='\t',
                            help='Set delimiter. [default: \t].', type=str)
        parser.add_argument('-H', '--header', help='Fist line is a header.', 
                            action='store_true')
        parser.add_argument('-p', '--pattern', nargs='+',  
                            help="""Column number plus search pattern plus 
                            replacement. Use this format: '3/[A,B]/C'. 
                            First column index start at 1. More than one pattern 
                            per column can be used and will be executed one
                            after another. If / is used in the pattern mask it 
                            with \ i.e \/."""
                            ,type=str, default=['.*'])
        
        # Process arguments
        args = parser.parse_args()

        if DEBUG:
            print(args)
            
        start(args)

        if args.verbose > 0:
            print("Verbose mode on")

        return 0
    except KeyboardInterrupt:
        # handle keyboard interrupt Easy to use parsing tools.
        return 0
    except Exception as e:
        if DEBUG:
            raise e
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        # sys.argv.append("-h")
        # sys.argv.append("-V")
        sys.argv.append("-d")
        sys.argv.append("-")
        sys.argv.append("-p")
        #sys.argv.append("2/[^A/-]*\//B[^CV]")
        sys.argv.append("2/.?B./CCC")
        sys.argv.append("2/[C]+/A")            
        sys.argv.append("-H")
    
        sys.argv.append("--")
        sys.argv.append("../test/simplereplace.test")
    sys.exit(main())