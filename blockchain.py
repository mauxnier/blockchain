import sys
import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
# -------------------------------
import requests
from urllib.parse import urlparse
# -------------------------------
app = Flask(__name__)


class Blockchain(object):
    difficulty_target = "0000"

    def hash_block(self, block):
        block_encoded = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_encoded).hexdigest()

    def __init__(self):
        # stores all the blocks in the entire blockchain
        self.chain = []
        # temporarily stores the transactions for the current block
        self.current_transactions = []
        # create the genesis block with a specific fixed hash of previous block genesis block starts with index 0
        genesis_hash = self.hash_block("genesis_block")
        self.append_block(hash_of_previous_block=genesis_hash,
                          nonce=self.proof_of_work(0, genesis_hash, []))

    def proof_of_work(self, index, hash_of_previous_block, transactions):
        # try with nonce = 0
        nonce = 0
        # try hashing the nonce together with the hash of the previous block until it is valid
        while self.valid_proof(index, hash_of_previous_block, transactions, nonce) is False:
            nonce += 1
            return nonce

    def valid_proof(self, index, hash_of_previous_block, transactions, nonce):
        # create a string containing the hash of the previous block and the block content, including the nonce
        content = f'{index}{hash_of_previous_block}{transactions}{nonce}'.encode()
        # hash using sha256
        content_hash = hashlib.sha256(content).hexdigest()
        # check if the hash meets the difficulty target
        return content_hash[:len(self.difficulty_target)] == self.difficulty_target

    # creates a new block and adds it to the blockchain
    def append_block(self, nonce, hash_of_previous_block):
        block = {
            'index': len(self.chain),
            'timestamp': time(),
            'transactions': self.current_transactions,
            'nonce': nonce,
            'hash_of_previous_block': hash_of_previous_block
        } 
        # reset the current list of transactions
        self.current_transactions = []
        # add the new block to the blockchain
        self.chain.append(block)
        return block


    def add_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'amount': amount,
            'recipient': recipient,
            'sender': sender
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        # returns the last block in the blockchain
        return self.chain[-1]
