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
    def recurse(bitreader):
        if bitreader.readbit():
            left = recurse(bitreader)
            right = recurse(bitreader)
            return huffman.TreeBranch(left, right)
        else:
            if bitreader.readbit():
                return huffman.TreeLeaf(bitreader.readbits(8))

            else:
                return huffman.TreeLeaf(None)

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
    curr = tree
    def recurse(curr):
        try:
            print("CURR" + str(curr.value))
            return curr.value
        except:
            if bitreader.readbit():
                print("CURR>RIGHT")
                return recurse(curr.right)
            else:
                print("CURR>LEFT")
                return recurse(curr.left)

    return recurse(curr)

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

    input_stream = bitio.BitReader(compressed)
    print(input_stream.bcount)
    output_stream = bitio.BitWriter(uncompressed)
    tree = read_tree(input_stream)
    print(input_stream.bcount)

    while(True):
        next_byte = decode_byte(tree, input_stream)
        print(next_byte)
        if next_byte == None:
            break
        else:
            output_stream.writebits(next_byte, 8)



def write_tree(tree, bitwriter):
    '''Write the specified Huffman tree to the given bit writer.  The
    tree is written in the format described above for the read_tree
    function.

    DO NOT flush the bit writer after writing the tree.

    Args:
      tree: A Huffman tree.
      bitwriter: An instance of bitio.BitWriter to write the tree to.
    '''
    pass


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
    pass
