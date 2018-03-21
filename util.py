# Ahmed El Gohary, 1508009

import bitio
import huffman

def read_tree(bitreader):

    '''Read a description of a Huffman tree from the given bit reader,
    and construct and return the tree. When this function returns, the
    bit reader should be ready to read the next bit immediately
    following the tree description.

    Huffman trees are stored in the following format:
      * TreeLeaf is represented by the two bits 01, followed by 8 bits
          for the symbol at that leaf.
      * TreeLeaf that is None (the special "end of message" character)
          is represented by the two bits 00.
      * TreeBranch is represented by the single bit 1, followed by a
          description of the left subtree and then the right subtree.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.

    Returns:
      A Huffman tree constructed according to the given description.
    '''
    # recursive function to read the bitreader
    def recurse(bitreader):
        if bitreader.readbit(): # if we get a 1, that means we have a branch
            left = recurse(bitreader)   # find left tree
            right = recurse(bitreader)  # find right tree
            return huffman.TreeBranch(left, right)  # return tree branch
        else:   # we got a 0
            if bitreader.readbit(): # we got a 01
                return huffman.TreeLeaf(bitreader.readbits(8))  # read byte

            else:
                return huffman.TreeLeaf(None)   # return empty tree leaf

    return recurse(bitreader)


def decode_byte(tree, bitreader):
    """
    Reads bits from the bit reader and traverses the tree from
    the root to a leaf. Once a leaf is reached, bits are no longer read
    and the value of that leave is returned.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.
      tree: A Huffman tree.

    Returns:
      Next byte of the compressed bit stream.
    """
    # recursive function to decode bytes
    def recurse(curr):
        if isinstance(curr, huffman.TreeLeaf):  # return value if leaf
            return curr.value
        else:
            # go right or left depending on code
            if bitreader.readbit():
                return recurse(curr.right)
            else:
                return recurse(curr.left)

    return recurse(tree)

def decompress(compressed, uncompressed):
    '''First, read a Huffman tree from the 'compressed' stream using your
    read_tree function. Then use that tree to decode the rest of the
    stream and write the resulting symbols to the 'uncompressed'
    stream.

    Args:
      compressed: A file stream from which compressed input is read.
      uncompressed: A writable file stream to which the uncompressed
          output is written.

    '''
    # initialise bit streams and tree
    input_stream = bitio.BitReader(compressed)
    tree = read_tree(input_stream)
    output_stream = bitio.BitWriter(uncompressed)

    while(True):
        next_byte = decode_byte(tree, input_stream) # decode each byte
        if next_byte == None:   # break if end of file
            break
        else:
            output_stream.writebits(next_byte, 8)   # write the decoded byte



def write_tree(tree, bitwriter):
    '''Write the specified Huffman tree to the given bit writer.  The
    tree is written in the format described above for the read_tree
    function.

    DO NOT flush the bit writer after writing the tree.

    Args:
      tree: A Huffman tree.
      bitwriter: An instance of bitio.BitWriter to write the tree to.
    '''
    def recurse(curr):
        if isinstance(curr, huffman.TreeBranch):    # write 1 if branch
            bitwriter.writebit(0b1)
            recurse(curr.left)  # check left branch first
            recurse(curr.right) # check right branch after
        else:
            if curr.value is not None:
                bitwriter.writebits(0b01, 2)    # output 01 then the byte
                bitwriter.writebits(curr.value, 8)
            else:
                bitwriter.writebits(0b00, 2)    # output 00
        return

    recurse(tree)


def compress(tree, uncompressed, compressed):
    '''First write the given tree to the stream 'compressed' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Flush the bitwriter after writing the entire compressed file.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
    '''
    # initialise tables and input and output bitstreams
    table = huffman.make_encoding_table(tree)
    input_stream = bitio.BitReader(uncompressed)

    output_stream = bitio.BitWriter(compressed)
    write_tree(tree, output_stream)

    # set up a counter to find partially filled bytes
    counter = 0

    while (True):
        try:
            # tries to read 8 bytes, if end of file found, go to except
            byte = input_stream.readbits(8)
            path = table[byte]  # find the path
            counter += len(path)
            for i in path:
                # output the bits
                output_stream.writebit(i)
        except:
            # for partially filled bytes, pad with 0's to make a byte
            byte = output_stream.writebits(0, counter % 8)
            # flush
            output_stream.flush()
            return
