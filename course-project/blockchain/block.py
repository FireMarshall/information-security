import time

from ..config import MINE_RATE
from ..util.crypto_hash import crypto_hash
from ..util.hex_to_binary import hex_to_binary

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}


class Block:

    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __str__(self):
        return f'''Block(
            'timestamp: {self.timestamp}, '
            'last_hash: {self.last_hash}, '
            'hash: {self.hash}, '
            'data: {self.data}, '
            'difficulty: {self.difficulty}, '
            'nonce: {self.nonce})'
        )'''

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(block_json):
        return Block(**block_json)

    @staticmethod
    def genesis():
        return Block(**GENESIS_DATA)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1
