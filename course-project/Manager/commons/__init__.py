MANAGER_IP = '192.168.43.152'

MANAGER_PORT = 8840
SERVER_PORT = 5540
NANOSECONDS = 1
MICROSECONDS = 1000 * NANOSECONDS
MILLISECONDS = 1000 * MICROSECONDS
SECONDS = 1000 * MILLISECONDS

MINE_RATE = 4 * SECONDS

STARTING_BALANCE = 1000

MINING_REWARD = 50
MINING_REWARD_INPUT = {'address': '*--official-mining-reward--*'}

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}
