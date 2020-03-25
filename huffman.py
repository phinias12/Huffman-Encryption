import os
import sys
import marshal
import array
import heapq

try:
    import cPickle as pickle
except:
    import pickle

def encode(msg):

    raise NotImplementedError

def decode(msg, decoderRing):

    raise NotImplementedError

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
            print(msg)
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