from crypt import methods
from flask import Flask, jsonify
from blockchain import Blockchain


app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Parabéns, você minerou um bloco!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_chain_valid = blockchain.is_chain_valid()
    message = 'A Blockchain é válida!' if is_chain_valid else 'A Blockchain não é válida!'
    response = {
        'message': message
    }
    return jsonify(response), 200


app.run(host='0.0.0.0', port=5000, debug=True)
