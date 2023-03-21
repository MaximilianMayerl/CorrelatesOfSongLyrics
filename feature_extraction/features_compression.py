""""
Computes compression ratio obtained by zlib, effectively using the LZ77 compression algorithm.
"""

import sys
import zlib


def get_compression_ratio(text):
    original_size = sys.getsizeof(text.encode('utf-8'))
    compressed_size = sys.getsizeof(zlib.compress(text.encode('utf-8')))
    
    return original_size / compressed_size
