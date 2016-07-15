import time

class FileObjectError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

# Biopython read_fasta implementation
def SimpleFastaParser(file):
    """Generator function to iterate over Fasta records (as string tuples).
    For each record a tuple of two strings is returned, the FASTA title
    line (without the leading '>' character), and the sequence (with any
    whitespace removed). The title line is not divided up into an
    identifier (the first word) and comment or description.
    >>> with open("Fasta/dups.fasta") as handle:
    ...     for values in SimpleFastaParser(handle):
    ...         print(values)
    ...
    ('alpha', 'ACGTA')
    ('beta', 'CGTC')
    ('gamma', 'CCGCC')
    ('alpha (again - this is a duplicate entry to test the indexing code)', 'ACGTA')
    ('delta', 'CGCGC')
    """
    with open(file) as handle:
        # Skip any text before the first record (e.g. blank lines, comments)
        while True:
            line = handle.readline()
            if line == "":
                return  # Premature end of file, or just empty?
            if line[0] == ">":
                break

        while True:
            if line[0] != ">":
                raise ValueError(
                    "Records in Fasta files should start with '>' character")
            title = line[1:].rstrip()
            lines = []
            line = handle.readline()
            while True:
                if not line:
                    break
                if line[0] == ">":
                    break
                lines.append(line.rstrip())
                line = handle.readline()

            # Remove trailing whitespace, and any internal spaces
            # (and any embedded \r which are possible in mangled files
            # when not opened in universal read lines mode)
            yield title, "".join(lines)#.replace(" ", "").replace("\r", "")

            if not line:
                return  # StopIteration



def read_fasta(file_path):
    with open(file_path, "r") as fastafile:

        #if "b" not in fastafile.mode:
        #    raise FileObjectError("File is not opened in binary mode")

        #seq = b""
        seq = []#bytearray()
        header = ""
        trig = False

        for line in fastafile:
            line = line.strip()

            # Check if line header
            if line.startswith(">"):
                if trig:
                    yield header, seq
                    #seq = b""
                    seq = []#bytearray()

                trig = True
                header = line
            else:
                seq.append(line)

        yield header, "".join(seq).replace(" ", "").replace("\r", "")


start = time.time()
for fasta in read_fasta(file_path="/home/nauer/Projects/PrimerDesign/Sources/picr.fa"):
    pass
end = time.time()
print(end - start)

start = time.time()
for fasta in SimpleFastaParser("/home/nauer/Projects/PrimerDesign/Sources/picr.fa"):
    pass
end = time.time()
print(end - start)

