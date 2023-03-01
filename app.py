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
import blockchain as bc

app = Flask(__name__)

# generate a globally unique address for this node
node_identifier = str(uuid4())

# instantiate the Blockchain
blockchain = bc.Blockchain()

# return the entire blockchain


@app.route('/blockchain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/mine', methods=['GET'])
def mine_block():
    # the miner must receive a reward for finding the proof the sender is "0" to signify that this node has mined a new coin.
    blockchain.add_transaction(sender="0", recipient=node_identifier, amount=1)

    # obtain the hash of last block in the blockchain
    last_block_hash = blockchain.hash_block(blockchain.last_block)

    # using PoW, get the nonce for the new block to be added to the blockchain
    index = len(blockchain.chain)
    nonce = blockchain.proof_of_work(
        index, last_block_hash, blockchain.current_transactions)

    # add the new block to the blockchain using the last block hash and the current nonce
    block = blockchain.append_block(nonce, last_block_hash)
    response = {
        'message': "New Block Mined",
        'index': block['index'],
        'hash_of_previous_block': block['hash_of_previous_block'],
        'nonce': block['nonce'],
        'transactions': block['transactions'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    # get the value passed in from the client
    values = request.get_json()

    # check that the required fields are in the POST'ed data
    required_fields = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required_fields):
        return ('Missing fields', 400)

    # create a new transaction
    index = blockchain.add_transaction(
        values['sender'],
        values['recipient'],
        values['amount']
    )

    response = {'message': f'Transaction will be added to Block {index}'}
    return (jsonify(response), 201)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(sys.argv[1]))
