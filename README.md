BI-Army-Knife
============

Small and easy to use bioinformatic tools.

+ grepline.py
+ fastagrep.py

## *linegrep.py*
Uses one or more regular regression patterns to extract different fields from line.
TODO

### Dependencies
Python >= 3.4
----

## *fastagrep.py*

Use a regular expression pattern to find header lines (default lines starting with: '>')
of interest and extract the header plus the following sequence (following lines until
the next header line) to the output.

Pattern could be a single regular expression or a list of regular expression. The pattern
which identify the header line is changeable to use the program also for non fasta file
types.

There is also a summary option available providing general information about the sequence
i.e sequence length or alphabet composition. Also sequences with duplicate headers could
be filtered out.

### Examples

Download a protein fasta file from NCBI and extract only RefSeq sequences starting with NP
and found a match of "uncharacterized protein" in the header definition.

~~~
  curl -L ftp://ftp.ncbi.nlm.nih.gov/refseq/M_musculus/mRNA_Prot/mouse.1.protein.faa.gz | gunzip > test.faa
  fastagrep.py -e "\|NP.*uncharacterized protein" test.faa
~~~

~~~
  output:
>gi|294997241|ref|NP_001171123.1| uncharacterized protein LOC545886 precursor [Mus musculus]
MLVVLLTAALLALSSAQSADEDGQSTSDVQEQAPVNQTQVSGSDPSSAEVNTVNVQEPESASAGNESSANSGSEQEQQQQ
AKESQEAQGQRPSDSAVKEQESQTGEERRKEVQGQHNFHPEKPGVVHMKVKRNNPNSHKRFNHNLPNKRKFESPDKGNQR
RRSMA
>gi|339639643|ref|NP_001229872.1| uncharacterized protein LOC100190996 [Mus musculus]
MRDSTGCCERRLVKLRTPNMDLLTYDDVHVNFTQEEWALLDASQKSLYKGVMVETYRNLTAIGYSWEEHTIEDHFQTSRS
LGRHERRSSAEQHSEFIPCGKAFAYQSRSQRHVRIHNGEKHYECNQCGKDFGTRSVLQRLKRTHSGENPYECNHCGKAFA
ESSTLQIHKRKHTGEKPYECNHCVKAFAKMSELQIHKRIHTGEKPYECKQCGKAFTQSSHLGIHKQTHTGEKPYECKQCG
KAFARSSTLQTHKQTHTGEKPYECKQCDKAFVRRGELQIHKGTHTGEKPYECKQCGKAFAQSGTLQIHKRTHTGEKPY
...
~~~

Uses a list of identifiers to extract sequences

~~~
  linegrep.py -p "gi\|(\d*)" -f 20 -t 100 -- test.faa > idlist
  fastagrep.py -l idlist -- test.faa
~~~

~~~
  idlist:
62198717
62198718
62198719
62198720
62198721
...

  output:
>gi|62198717|ref|YP_220553.1| cytochrome c oxidase subunit II (mitochondrion) [Mus musculus domesticus]
MAYPFQLGLQDATSPIMEELMNFHDHTLMIVFLISSLVLYIISLMLTTKLTHTSTMDAQEVETIWTILPAVILIMIALPS
LRILYMMDEINNPVLTVKTMGHQWYWSYEYTDYEDLCFDSYMIPTNDLKPGELRLLEVDNRVVLPMELPIRMLISSEDVL
HSWAVPSLGLKTDAIPGRLNQATVTSNRPGLFYGQCSEICGSNHSFMPIVLEMVPLKYFENWSASMI
>gi|62198718|ref|YP_220554.1| ATP synthase F0 subunit 8 (mitochondrion) [Mus musculus domesticus]
MPQLDTSTWFITIISSMITLFILFQLKVSSQTFPLAPSPKSLTTMKVKTPWELKWTKIYLPHSLPQQ
...

~~~

Also getting a summary over sequence length and alphabeth frequency is quity easy.

~~~
  fastagrep.py -s -- test.faa
~~~

~~~
  output:
Header  Seq.length      Alphabet
>gi|62198714|ref|YP_220550.1| NADH dehydrogenase subunit 1 (mitochondrion) [Mus musculus domesticus]    318     I:26|V:11|Y:14|Q:6|T:22|P:22|S:24|K:6|E:12|M:21|W:9|F:20|C:1|H:4|L:58|D:3|N:13|A:25|R:8|G:13
>gi|62198715|ref|YP_220551.1| NADH dehydrogenase subunit 2 (mitochondrion) [Mus musculus domesticus]    345     I:38|G:14|Y:9|Q:12|T:35|P:20|K:13|E:4|V:5|W:8|M:36|C:1|H:4|L:62|N:22|A:23|R:3|S:22|F:14
...

~~~

Redirecting and piping also works.

~~~
  fastagrep.py -e "123" -- - < test.faa
~~~

Single sequence output is new in version 1.8. Now you can simply create single fasta sequence files out from
multi-fasta file searches.

~~~
  # Produce singlefasta0.faa, singlefasta1.faa, singlefasta2,.faa, ... in tmp folder
  fastagrep.py -e "123" --prefix "singlefasta" -O tmp -- - < test.faa

  # Convert multi-fasta file to single-fasta files in the current working directory
  fastagrep.py --prefix "singlefasta" -O -- - < test.faa
~~~

# New features in version 3.0
+ Sub sequencing now supported
+ Create reverse transcript from RNA or DNA sequences

~~~
  # Create the reverse transcript of all fasta sequences
  fastagrep.py -T DNA -- DNA.fa

  # Returns the sub sequence from index 10 to 110 of all sequences
  fastagrep.py -a 10 -b 100 -- DNA.fa
~~~


### Dependencies
Python >= 3.4

----
