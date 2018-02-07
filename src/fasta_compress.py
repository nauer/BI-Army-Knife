import string
from array import array
from itertools import product
import time
from collections import OrderedDict

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print("{} function took {:.3f} ms".format(f.__name__, (time2-time1) * 1000.0))
        return ret
    return wrap


def create_lib(alphabeth=[b"A", b"C", b"G", b"T", b"W", b"S", b"M", b"K", b"R", b"Y", b"B", b"D", b"H", b"V", b"N"],
               count=4):
    d = {}
    last_index = 0

    for i in range(count, 0, -1):
        d = {**d, **{b"".join(val): index + last_index for index, val in
                     enumerate(
                         product(alphabeth, repeat=i))}}

        print(last_index, len(d), i)
        last_index = len(d) - 1


    return d





@timing
def create_index(file_name):
    d = OrderedDict()

    h_start = -1

    with open(file_name, "rb") as f_in:
        for line in f_in:
            if line[0] == 62:
                if h_start > -1:
                    new_end = f_in.tell()
                    new_h_len = len(line)

                    end = new_end - new_h_len

                    # Write out
                    if line in d:
                        d[header].append((h_start, h_end, end))
                    else:
                        d[header] = [(h_start, h_end, end)]

                    h_start = end
                    h_end = new_end
                    header = line[1:].rstrip()
                else:
                    h_end = f_in.tell()
                    h_start = h_end - len(line)
                    header = line[1:].rstrip()


        # Update last end
        end = f_in.tell()

    # Write out
    if line in d:
        d[header].append((h_start, h_end, end))
    else:
        d[header] = [(h_start, h_end, end)]

    return d


def get_fasta(file_name, d, header):
    if not isinstance(header, bytes):
        header = header.encode()

    with open(file_name, "rb") as f_in:
        f_in.seek(d[header][0][0])

        return f_in.read(d[header][0][2] - d[header][0][0])


def compress_dna(file_name, d, output, count=4):
    db = create_lib()


    with open(file_name, "rb") as f_in, open(output, "wb") as f_out:
        for header in d:
            print("Encode {}".format(header.decode()))
            for fasta in d[header]:
                a = array("H")
                f_in.seek(fasta[0])
                f_out.write(f_in.readline())

                #print(fasta[1], fasta[2], fasta[2] - fasta[1])
                seq = f_in.read(fasta[2] - fasta[1]).translate(None, b'\t\n\r\v\f ')

                l, g = divmod(len(seq), count)

                for i in range(l):
                    #print(db[seq[i * 4: (i * 4) + 4]], seq[i * 4: (i * 4) + 4])
                    a.append(db[seq[i * count: (i * count) + count]])

                if g > 0:
                    a.append(db[seq[(i + 1) * count: ]])

                f_out.write(a.tobytes())

if __name__ == "__main__":
    #db = create_lib()

    d = create_index("/datastore/nauer/Assemblies/PICR_2.0/picr.scaffolds.fa")

    #get_fasta("/datastore/nauer/Assemblies/PICR_2.0/picr.scaffolds.fa", d, "picr_0 [chromosome=2]")#picr_1181 [chromosome=unplaced]")

    compress_dna("/datastore/nauer/Assemblies/PICR_2.0/picr.scaffolds.fa", d, "out.basta")

    # print(d[b'picr_0 [chromosome=2]']) #picr_1 [chromosome=5]

    # print(db)
    # print(b[1])



