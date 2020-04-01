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

def byteToStr(b, fill = 8):
    byte = str()
    while b != 0:
        i = b % 2
        byte = str(i) + byte
        b = b//2

    return byte.zfill(fill)

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
    decodeRing = dict()

    for code in codes:
        ring[code[0]] = code[1]
        decodeRing[code[1]] = code[0]

    cipher = str()

    for char in msg:
        cipher += ring[char]

    return cipher, decodeRing

def decode(msg, decoderRing):
    s = list(msg)
    queue = []
    decoded = array.array('B')
    for c in s:
        queue.append(c)
        val = ''.join(queue)
        if val in decoderRing:
            decoded.append(decoderRing[val])
            queue = []

    return decoded

def compress(msg):
    count = collections.Counter(msg)
    htree = [[weight, [char, '']] for char, weight in count.items()]
    codes = createRing(htree)
    ring = dict()
    binaryRing = dict()
    decodeRing = dict()

    for code in codes:
        ring[code[0]] = code[1]
        decodeRing[code[1]] = code[0]

    for code in codes:
        binary = encodeToBinary(code[1])
        binaryRing[code[0]] = binary

    # Initializes an array to hold the compressed message.
    compressed = array.array('B')
    count = 0
    buff = 0

    for char in msg:
        binary = ring[char]
        for bit in binary:
            if bit == "0":
                buff = (buff << 1)
            else:
                buff = (buff << 1) | 1

            count = count + 1
            if count > 7:
                compressed.append(buff)
                buff = 0
                count = 0

    if count < 7 and 0 < count:       
        compressed.append(buff)
    
    return compressed, decodeRing

    # Initializes an array to hold the compressed message.
    # compressed = array.array('B')
    # raise NotImplementedError

def decompress(msg, decoderRing):
    byteArray = array.array('B', msg)
    binary = str()
    for byte in range(len(byteArray)):
        if byte < len(byteArray) - 1:
            b = byteToStr(byteArray[byte])
            binary = binary + b
        else:
            b = byteToStr(byteArray[byte], 0)
            binary = binary + b

    s = list(binary)
    queue = []
    decompressed = array.array('B')

    for c in s:
        queue.append(c)
        val = ''.join(queue)
        if val in decoderRing:
            decompressed.append(decoderRing[val])
            queue = []

    return decompressed

    # Represent the message as an array
    # byteArray = array.array('B', msg)
    # raise NotImplementedError

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
            print(enc)
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
            print(msg)
        fp = open(outfile, 'wb')
        fp.write(msg)
        fp.close()
