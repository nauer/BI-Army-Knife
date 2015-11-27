__author__ = 'Norbert Auer'

import unittest

from fastagrep import Fasta
import fastagrep
import io

class TestFasta(unittest.TestCase):
    def test_add_header(self):
        """test add header"""
        fasta = Fasta()
        fasta.header = ">seq1"
        self.assertEqual(">seq1", fasta.header)

    def test_add_content(self):
        """test add line"""
        fasta = Fasta()
        fasta.add_content("ATG")
        fasta.add_content("CCGT")
        self.assertEqual("ATG\nCCGT", fasta.content)

    def test_is_duplicate(self):
        """test is duplicate True"""
        fasta1 = Fasta()
        fasta2 = Fasta()
        fasta1.header = ">seq1"
        fasta2.header = ">seq1"
        fasta1.is_duplicate()
        self.assertTrue(fasta2.is_duplicate())

    def test_is_duplicate(self):
        """test is duplicate False"""
        fasta1 = Fasta()
        fasta2 = Fasta()
        fasta1.header = ">seq1"
        fasta2.header = ">seq2"
        fasta1.is_duplicate()
        self.assertFalse(fasta2.is_duplicate())

    def test_is_equal(self):
        """test is fasta is equal"""
        fasta1 = Fasta()
        fasta2 = Fasta()
        fasta1.header = ">seq1"
        fasta1.add_content("ATG  ")
        fasta1.add_content("  CCT  ")
        fasta2.header = ">seq1  "
        fasta2.add_content("ATG")
        fasta2.add_content("CCT")
        self.assertTrue(fasta1 == fasta2)

    def test_is_not_equal1(self):
        """test is fasta is not equal"""
        fasta1 = Fasta()
        fasta2 = Fasta()
        fasta1.header = ">seq1"
        fasta1.add_content("ATG")
        fasta2.header = ">seq1"
        fasta2.add_content("CTG")
        self.assertFalse(fasta1 == fasta2)

    def test_is_not_equal2(self):
        """test is fasta is not equal"""
        fasta1 = Fasta()
        fasta2 = Fasta()
        fasta1.header = ">seq1"
        fasta1.add_content("ATG")
        fasta2.header = ">seq2"
        fasta2.add_content("ATG")
        self.assertFalse(fasta1 == fasta2)


# file=[<_io.TextIOWrapper name='../test/test_dup.fa' mode='r' encoding='UTF-8'>],
# fixed_strings=False,
# header_pattern='^>',

class ARGS():
    def __init__(self, file=[open("../test/unittest.fa", "r")], fixed_strings=False, header_pattern='^>',
                 invert_match=False, line_length=None, max_length=0, max_seq_length=0, max_sequences=1, max_size=10,
                 min_length=0, output=None, pattern='.*', pattern_list=None, prefix='output', rm_duplicates=False,
                 split='-', summary=False, summary_no_header=False):

        self.file = file
        self.fixed_strings = fixed_strings
        self.header_pattern = header_pattern
        self.invert_match = invert_match
        self.line_length = line_length
        self.max_length = max_length
        self.max_seq_length = max_seq_length
        self.max_sequences = max_sequences
        self.max_size = max_size
        self.min_length = min_length
        self.output = output
        self.pattern = pattern
        self.pattern_list = pattern_list
        self.prefix = prefix
        self.rm_duplicates = rm_duplicates
        self.split = split
        self.summary = summary
        self.summary_no_header = summary_no_header



class TestApp(unittest.TestCase):
    def test_fastagrep_no_para(self):
        with open("../test/unittest.fa", "r") as f:
            out = io.StringIO()
            args = ARGS(file=[f], output=out)
            fastagrep.start(args)

        with open("../test/unittest.fa", "r") as f:
            expected = f.read()

        self.assertEqual(out.getvalue(), expected)

    def test_fastagrep_e(self):
        with open("../test/unittest.fa", "r") as f:
            out = io.StringIO()
            args = ARGS(file=[f], output=out, pattern="seq2")
            fastagrep.start(args)

        expected = ">seq2\n12345678901234567890\n"

        self.assertEqual(out.getvalue(), expected)

if __name__ == '__main__':
    unittest.main()