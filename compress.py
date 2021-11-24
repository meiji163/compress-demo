#!/usr/bin/env python3
from typing import List
from argparse import ArgumentParser
parser = ArgumentParser(description = "prefix code compression")
parser.add_argument("-x", dest="expand", action="store_true")
parser.add_argument("file", type=str)
args = parser.parse_args()

# a binary prefix code i made up
# ( i.e. no codeword is a prefix of any other )
ENDL = "!\n"
CODE = {
         "MLH": "10",
         "but": "11",
         "because": "0010",
         "spectacular": "0011",
         "cool": "0100",
         "wonderful": "0101",
         "compression": "0010",
         "Pod 4.2.0": "011",
          ENDL: "0001",
    }

def encode(sents: List[List[str]]) -> bytes: 
    codes = []
    for sent in sents:
        for t in sent:
            if t == "Pod":
                codes.append(CODE["Pod 4.2.0"])
            elif t == "4.2.0":
                continue
            elif t == "is":
                continue
            else:
                codes.append(CODE[t])
        codes.append(CODE[ENDL])
    out = "".join(codes)

    # convert the binary string to actual bytes  
    enc_bytes = int(out, 2).to_bytes( (len(out)+7)//8, byteorder='big')
    return enc_bytes 

def decode(data: bytes) -> List[str]:
    code = bin( int.from_bytes(data, byteorder='big') )
    code = code.lstrip("0b")
    words = {code: w for w, code in CODE.items() }
    decoded = []

    # read the prefix, it should be uniquely decoable!
    while len(code) > 0:
        valid = False 
        for prefix in words:
            if code.startswith(prefix):
                decoded.append(words[prefix])
                code = code[len(prefix):]

                # these words always followed by "is"
                if words[prefix] in ("MLH", "Pod 4.2.0", "compression"):
                    decoded.append("is")
                valid = True
                break
        if not valid:
            raise RuntimeError("can't decode!")
    return decoded

if __name__ == "__main__":
    # decompress the file
    if args.expand:
        with open(args.file, 'rb') as f:
            data = f.read()
        out_file = args.file.rstrip(".ec") + ".dc"
        decoded = decode(data)
        with open(out_file,'w') as f:
            for i in range(len(decoded)):
                f.write(decoded[i])
                
                # fill in the spaces
                if decoded[i]!=ENDL and i+1<len(decoded) and decoded[i+1]!=ENDL:
                    f.write(" ")

    # compress the file 
    else:
        with open(args.file, 'r') as f:
            lines = f.readlines()
        sents = [l.strip("!\n").split(" ") for l in lines] 
        encoded = encode(sents)
        with open(args.file + ".ec",'wb') as f:
            f.write(encoded)
