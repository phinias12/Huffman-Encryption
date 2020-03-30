import os
import sys
import marshal
import array
import heapq
import collections

try:
    import cPickle as pickle
except:
    import pickle

def createRing(htree):
    heapq.heapify(htree)
    while len(htree) > 1:
        left = heapq.heappop(htree)
        right = heapq.heappop(htree)
        for sumNode in left[1:]:
            sumNode[1] = '0' + sumNode[1]
        
        for sumNode in right[1:]:
            sumNode[1] = '1' + sumNode[1]

        heapq.heappush(htree, [left[0] + right[0]] + left[1:] + right[1:])
    codes = sorted(heapq.heappop(htree)[1:], key=lambda p: (len(p[-1]), p))

    return codes

def encodeToBinary(ascii):
    binary = list(ascii)
    buff = 0

    for c in binary:
        if c == "1":
            buff = (buff << 1) | 0x01

        if c == "0":
            buff = (buff << 1) | 0x00

    return buff

def encode(msg):
    count = collections.Counter(msg)
    htree = [[weight, [char, '']] for char, weight in count.items()]
    codes = createRing(htree)
    ring = dict()

    for code in codes:
        ring[code[0]] = code[1]

    cipher = str()

    for char in msg:
        cipher += ring[char]

    return cipher, codes

def decode(msg, decoderRing):
    ring = dict()
    for code in decoderRing:
        ring[code[0]] = code[1]

    s = list(msg)
    queue = []
    decoded = str()
    while len(s) != 0:
        c = s.pop(0)
        queue.append(c)
        val = ''.join(queue)
        if val in ring.values():
            key = list(ring.keys())[list(ring.values()).index(val)]
            decoded += str(chr(key))
            queue = []

    return decoded.encode()

def compress(msg):
    # Initializes an array to hold the compressed message.
    compressed = array.array('B')
    raise NotImplementedError

def decompress(msg, decoderRing):

    # Represent the message as an array
    byteArray = array.array('B',msg)
    raise NotImplementedError

def usage():
    sys.stderr.write("Usage: {} [-c|-d|-v|-w] infile outfile\n".format(sys.argv[0]))
    exit(1)

if __name__=='__main__':
    if len(sys.argv) != 4:
        usage()
    opt = sys.argv[1]
    compressing = False
    decompressing = False
    encoding = False
    decoding = False
    if opt == "-c":
        compressing = True
    elif opt == "-d":
        decompressing = True
    elif opt == "-v":
        encoding = True
    elif opt == "-w":
        decoding = True
    else:
        usage()

    infile = sys.argv[2]
    outfile = sys.argv[3]
    assert os.path.exists(infile)

    if compressing or encoding:
        fp = open(infile, 'rb')
        msg = fp.read()
        fp.close()
        if compressing:
            compr, decoder = compress(msg)
            fcompressed = open(outfile, 'wb')
            marshal.dump((pickle.dumps(decoder), compr), fcompressed)
            fcompressed.close()
        else:
            enc, decoder = encode(msg)
            fcompressed = open(outfile, 'wb')
            marshal.dump((pickle.dumps(decoder), enc), fcompressed)
            fcompressed.close()
    else:
        fp = open(infile, 'rb')
        pickleRick, compr = marshal.load(fp)
        decoder = pickle.loads(pickleRick)
        fp.close()
        if decompressing:
            msg = decompress(compr, decoder)
        else:
            msg = decode(compr, decoder)
        fp = open(outfile, 'wb')
        fp.write(msg)
        fp.close()