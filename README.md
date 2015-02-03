BI-Army-Knife
============

Small and easy to use bioinformatic tools.

+ grepline.py
+ fastagrep.py

## *grepline.py*

###Dependencies
Python >= 3.4
----

## *fastagrep.py*

Use a regular expression pattern to find header lines (default lines starting with: '>') 
of interest and extract the header plus the following sequence (following lines until 
the next header line) to the output.

Pattern could be a single regular expression or a list of regular expression. The pattern
which identify the header line is changeable to use the program also for non fasta file
types.

### Examples

Download a protein fasta file from NCBI and extract only RefSeq sequences starting with NP
and found a match of "uncharacterized protein" in the header definition.

~~~
  curl -L ftp://ftp.ncbi.nlm.nih.gov/refseq/M_musculus/mRNA_Prot/mouse.1.protein.faa.gz | gunzip > test.faa
  fastagrep.py -e "\|NP.*uncharacterized protein" test.faa
~~~

Uses a list of identifiers to extract sequences

~~~
  linegrep.py -p "gi\|(\d*)" -f 20 -t 100 -- test.faa > idlist
  fastagrep.py -l idlist -- test.faa 
~~~

Redirecting and piping also works.

~~~
  fastagrep.py -e "123" -- - < test.faa
~~~

###Dependencies
Python >= 3.4
Biopython >= 1.64

----

