from subprocess import Popen, PIPE, STDOUT
import re
from enum import Enum

import os
import tempfile
import pprint

#from Bio.Blast.Applications import NcbiblastnCommandline

class Alphabeth():
    DNA = {'name' : "DNA", 'alphabeth' : b'ACGT', 'rev_translation' : b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNTNGNNNCNNNNNNNNNNNNANNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff', 'translation' : b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNANCNNNGNNNNNNNNNNNNTNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'}
    RNA = {'name' : "RNA", 'alphabeth' : b'ACGU', 'rev_translation' : b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNUNGNNNCNNNNNNNNNNNNNANNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff', 'translation' : b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNANCNNNGNNNNNNNNNNNNNUNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'}
    NONE= {'name' : "NONE", 'alphabeth' : b'', 'rev_translation' : b'', 'translation' : b''}

    def __init__(self, alphabeth=None):
        if alphabeth:
            if alphabeth == self.DNA:
                self.alphabeth = self.DNA
            elif alphabeth == self.RNA:
                self.alphabeth = self.RNA
            elif alphabeth == self.NONE:
                self.alphabeth = self.NONE
            else:
                raise Exception("Alphabeth unknown")
        else:
            self.alphabeth = self.NONE

    def __str__(self):
        return "{}: {}".format(self.alphabeth['name'], self.alphabeth['alphabeth'].decode())


class FileObjectError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Fasta():
    """Class for holding a fasta sequence

    """

    def __init__(self, header, sequence, alphabeth=Alphabeth(Alphabeth.DNA), line_width=60, header_pattern=b'^>'):
        # Translate to bytes
        try:
            self._header_pattern = header_pattern.encode().strip()
        except AttributeError:
            self._header_pattern = bytes(header_pattern.strip())

        try:
            self._header = header.encode().rstrip()
        except AttributeError:
            self._header = bytes(header).rstrip()

        # Remove all non-word characters (everything except numbers and letters)
        rm_pattern = re.compile(b"\s")

        try:
            self._seq = bytearray(rm_pattern.sub(b"", sequence.encode()))
        except AttributeError:
            self._seq = bytearray(rm_pattern.sub(b"", sequence))

        self._alphabeth = alphabeth
        self.line_width = line_width

    def __repr__(self):
        return self._header.decode() + "\n" + self._seq.decode()

    def __iter__(self):
        """
        Returns fasta line by line. First line is header. Line length is defined by self.line_width
        :yield: str
        """
        # Returns header as first line
        yield self.get_header().decode()

        if self.line_width > 0:
            for i in range(self.get_seq_length() // self.line_width):
                start_pos = i * self.line_width
                # Returns line by line - linewidth is self.line_width
                yield self._seq[start_pos:start_pos + self.line_width].decode()

            # Last line if not full length
            if self.get_seq_length() % self.line_width != 0:
                yield self._seq[self.get_seq_length() // self.line_width * self.line_width:].decode()
        else:
            # No line width returns all in one line
            yield self._seq.decode()

    def __getitem__(self, index):
        if isinstance(index, slice):
            if index.step:
                raise TypeError("Index step is not supported")

            return Fasta(self._header.decode() + " subseq[{fr}:{to}]".format(fr=index.start, to=index.stop), self._seq[index])
        else:
            return Fasta(self._header.decode() + " subseq[{fr}:{to}]".format(fr=index, to=index+1), self._seq[index:index + 1])

    def get_line_by_line(self, line_width=60):
        """
        Returns fasta line by line. First line is header. Line length is defined by line_width argument
        :yield: str
        """
        # Returns header as first line
        yield self.get_header().decode()

        if line_width > 0:
            for i in range(self.get_seq_length() // line_width):
                start_pos = i * line_width
                # Returns line by line - linewidth is self.line_width
                yield self._seq[start_pos:start_pos + line_width].decode()

            # Last line if not full length
            if self.get_seq_length() % line_width != 0:
                yield self._seq[self.get_seq_length() // line_width * line_width:].decode()
        else:
            # No line width returns all in one line
            yield self._seq.decode()

    def get_summary(self):
        chars = dict()

        for c in self.get_sequence():
            if c in chars:
                chars[c] += 1
            else:
                chars[c] = 1

        return "{}\t{}\n".format(str(self.get_seq_length()), "|".join([chr(item[0]) + ":" + str(item[1]) for item in chars.items()]))

    def set_line_width(self, line_width):
        self.line_width = line_width

    def get_GC_content(self):
        return (self._seq.count(b"G") + self._seq.count(b"C")) / self.get_seq_length() * 100

    def mask_sequence(self, start, stop, char=None):
        if char:
            try:
                self._seq[start:stop] = char
            except:
                self._seq[start:stop] = char.encode()
        else:
            self._seq[start:stop] = self._seq[start:stop].lower()

    def to_upper(self):
        self._seq[:] = self._seq.upper()

    def to_lower(self):
        self._seq[:] = self._seq.lower()

    def get_reverse_transcript_sequence(self):
        if len(self._alphabeth.alphabeth['rev_translation']) == 0:
            return self._seq[::-1]
        else:
            return self._seq.translate(self._alphabeth.alphabeth['rev_translation'])[::-1]

    def get_sequence(self):
        if len(self._alphabeth.alphabeth['translation']) == 0:
            return self._seq
        else:
            return self._seq.translate(self._alphabeth.alphabeth['translation'])

    def get_header(self):
        return self._header

    def get_seq_length(self):
        return len(self._seq)

    def get_alphabeth(self):
        return self.alphabeth

    def set_alphabeth(self, alphabeth):
        if alphabeth == Alphabeth.DNA:
            self.alphabeth = Alphabeth.DNA
        elif alphabeth == Alphabeth.RNA:
            self.alphabeth = Alphabeth.RNA
        elif alphabeth == Alphabeth.NONE:
            self.alphabeth = Alphabeth.NONE
        else:
            raise Exception("Alphabeth unknown")


class MultiFasta():
    """Class for holding a multiple Fasta objects

    """

    def __init__(self):
        self.fastas = []

    def __str__(self):
        multi_fasta = []
        for fasta in self.fastas:
            multi_fasta.append(fasta.__str__())

        return "\n".join(multi_fasta)

    def __len__(self):
        return len(self.fastas)

    def __iter__(self):
        for fasta in self.fastas:
            yield fasta

    def __getitem__(self, index):
        return self.fastas[index]

    def remove_all(self):
        self.fastas = []

    def load_fasta(self, *, file_path):
        with open(file_path, "rb") as fastafile:
            self.load_fasta(file_obj=fastafile)

    def load_fasta(self, *, file_obj):
        [self.fastas.append(fasta) for fasta in MultiFasta.read_fasta(file_obj=file_obj)]

    def add_fasta(self, fasta):
        if isinstance(fasta, Fasta):
            self.fastas.append(fasta)

    def save_fasta(self, path):
        with open(path,"wb") as handler:
            for fasta in self.fastas:
                handler.write(b">" + fasta.get_header() + b"\n")
                handler.write(fasta.get_sequence() + b"\n")

    @staticmethod
    def read_fasta(*, file_path, header_pattern=b"^>"):
        with open(file_path, "rb") as fastafile:
            Fasta.read_fasta(file_obj=fastafile, header_pattern=header_pattern)

    @staticmethod
    def read_fasta(*, file_obj, header_pattern=b"^>"):
        try:
            header_pattern = header_pattern.encode()
        except AttributeError:
            header_pattern = bytes(header_pattern)

        pattern = re.compile(header_pattern)

        if "b" not in file_obj.mode:
            raise FileObjectError("not in binary mode")

        header = b""

        # Get first fasta header in file
        for line in file_obj:
            if pattern.search(line):
                header = line
                break

        seq = bytearray()

        for line in file_obj:
            #line = line.rstrip()

            # Check if line header
            if pattern.search(line):
                yield Fasta(header, seq)

                header = line
                seq = bytearray()
            else:
                seq += line

        yield Fasta(header, seq)


class Primer3():
    # Prepare Header
    primer3_header = [b'PRIMER_LEFT_SEQUENCE', b'PRIMER_RIGHT_SEQUENCE', b'PRIMER_LEFT', b'PRIMER_RIGHT',
                      b'PRIMER_LEFT_TM', b'PRIMER_RIGHT_TM', b'PRIMER_LEFT_GC_PERCENT', b'PRIMER_RIGHT_GC_PERCENT',
                      b'PRIMER_PAIR_PRODUCT_SIZE', b'PRIMER_LEFT_PENALTY', b'PRIMER_RIGHT_PENALTY',
                      b'PRIMER_PAIR_PENALTY', b'PRIMER_LEFT_END_STABILITY', b'PRIMER_RIGHT_END_STABILITY',
                      b'PRIMER_LEFT_HAIRPIN_TH', b'PRIMER_RIGHT_HAIRPIN_TH', b'PRIMER_LEFT_SELF_ANY_TH',
                      b'PRIMER_RIGHT_SELF_ANY_TH', b'PRIMER_LEFT_SELF_END_TH', b'PRIMER_RIGHT_SELF_END_TH',
                      b'PRIMER_PAIR_COMPL_ANY_TH', b'PRIMER_PAIR_COMPL_END_TH']

    def __init__(self, alphabeth=Alphabeth.DNA, **kargs):
        #self.alphabeth = alphabeth
        #self.pattern = re.compile(b"[^" + self.alphabeth['alphabeth'] + b"]")
        self.settings = kargs
        self.primer_list = dict()
        self.result_set = dict()

    def get_settings(self):
        return self.settings

    def get_primer_list(self):
        return self.primer_list

    def get_primer_stat(self, fasta, window_size, type='left'):
        """
        Get a list of unique and not unique primers
        :param fasta: Fasta
        :param window_size: int - primer length
        :param type: str - ['left' | 'right']
        :return: dict - all primers with count, type, id and start position
        """
        seq_len = fasta.seq_length

        subseq_count = seq_len - window_size + 1

        i = 0
        if type == 'left':
            seq = bytes(fasta.get_sequence())

            while i < subseq_count:
                primer = seq[i:i + window_size] # bytes(fasta.get_sequence()[i:i + window_size])

                try:
                    i += primer.index(b'N') + 1
                    continue
                except ValueError:
                    pass

                if primer not in self.primer_list:
                    self.primer_list[primer] = dict()
                    self.primer_list[primer]['count'] = 0
                    self.primer_list[primer]['start'] = []
                    self.primer_list[primer]['id'] = []
                    self.primer_list[primer]['type'] = b'left'

                self.primer_list[primer]['count'] += 1
                self.primer_list[primer]['start'].append(i)
                self.primer_list[primer]['id'].append(fasta.get_header())

                i += 1
        elif type == 'right':

            rev_seq = bytes(fasta.get_reverse_transcript_sequence())

            while i < subseq_count:
                primer = rev_seq[i:i + window_size]

                try:
                    i += primer.index(b'N') + 1
                    continue
                except ValueError:
                    pass

                if primer not in self.primer_list:
                    self.primer_list[primer] = dict()
                    self.primer_list[primer]['count'] = 0
                    self.primer_list[primer]['start'] = []
                    self.primer_list[primer]['id'] = []
                    self.primer_list[primer]['type'] = b'right'

                self.primer_list[primer]['count'] += 1
                self.primer_list[primer]['start'].append(i)
                self.primer_list[primer]['id'].append(fasta.get_header())

                i += 1
        return self.primer_list

    def run(self, fasta, settings):
        # Create primer3 process
        p = Popen(['primer3_core'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

        outs, errs = p.communicate(input=b"\n".join(self.get_settings(settings)) + b"\n=")

        # Output parsing regex
        pat1 = re.compile(b"(PRIMER_PAIR)_(\d+)(_([^=]*))?=(.*)")
        pat2 = re.compile(b"(PRIMER_LEFT)_(\d+)(_([^=]*))?=(.*)")
        pat3 = re.compile(b"(PRIMER_RIGHT)_(\d+)(_([^=]*))?=(.*)")

        result = self.result_set[fasta.get_header()] = {}

        # Parse primer3 output
        for line in outs.split(b"\n"):
            res1 = pat1.search(line)
            res2 = pat2.search(line)
            res3 = pat3.search(line)

            if res1:
                nr = int(res1.group(2))

                if nr not in result:
                    result[nr] = dict()

                if res1.group(3):
                    result[nr][res1.group(1) + res1.group(3)] = res1.group(5)
                else:
                    result[nr][res1.group(1)] = res1.group(5)
            elif res2:

                nr = int(res2.group(2))

                if nr not in result:
                    result[nr] = dict()

                if res2.group(3):
                    result[nr][res2.group(1) + res2.group(3)] = res2.group(5)
                else:
                    result[nr][res2.group(1)] = res2.group(5)
            elif res3:
                nr = int(res3.group(2))

                if nr not in result:
                    result[nr] = dict()

                if res3.group(3):
                    result[nr][res3.group(1) + res3.group(3)] = res3.group(5)
                else:
                    result[nr][res3.group(1)] = res3.group(5)

    def get_result(self):
        # Header
        result = b"SEQ_ID\t" + b"\t".join(self.primer3_header)

        for fasta_header in self.result_set:
            t = self.result_set[fasta_header]

            for primer in sorted(t):
                line = [fasta_header]

                for h in self.primer3_header:
                    if h in t[primer]:
                        line.append((t[primer][h]))

                result += b"\n" + b"\t".join(line)

        return result

    def get_settings(self, settings):
        args = []

        for key in settings:
            if settings[key] != b"":
                args.append(key + b"=" + settings[key])

        return args
