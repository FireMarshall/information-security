import json
import hashlib
import hashlib
import pickle
import socket
import threading
import time
from ecdsa import SigningKey
import json
def crypto_hash(*args):
    """
    Return a sha-256 hash of the given arguments.
    """
    stringified_args = sorted(map(lambda data: json.dumps(data), args))
    joined_data = ''.join(stringified_args)

    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()


HEX_TO_BINARY_CONVERSION_TABLE = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111'
}


def hex_to_binary(hex_string):
    binary_string = ''

    for character in hex_string:
        binary_string += HEX_TO_BINARY_CONVERSION_TABLE[character]

    return binary_string


def main():
    number = 451
    hex_number = hex(number)[2:]
    print(f'hex_number: {hex_number}')

    binary_number = hex_to_binary(hex_number)
    print(f'binary_number: {binary_number}')

    original_number = int(binary_number, 2)
    print(f'original_number: {original_number}')

    hex_to_binary_crypto_hash = hex_to_binary(crypto_hash('test-data'))
    print(f'hex_to_binary_crypto_hash: {hex_to_binary_crypto_hash}')

    print(f"crypto_hash('one', 2, [3]): {crypto_hash('one', 2, [3])}")
    print(f"crypto_hash(2, 'one', [3]): {crypto_hash(2, 'one', [3])}")


if __name__ == '__main__':
    main()
