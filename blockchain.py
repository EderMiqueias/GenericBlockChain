from datetime import datetime as dt
import hashlib
import json

class Blockchain:
    def __init__(self) -> None:
        self.chain = list()
        self.create_block(proof=1, previous_hash = '0')
    
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(dt.now()),
            'previous_hash': previous_hash,
            'proof': proof
        }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def get_hash_operation(self, new_proof, previous_proof):
        return hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        while True:
            hash_operation = self.get_hash_operation(new_proof, previous_proof)
            if hash_operation[:4] == '0000':
                return new_proof
            new_proof += 1

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self):
        previous_block = self.chain[0]
        for block in self.chain:
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = self.get_hash_operation(proof, previous_proof)
            if hash_operation[:4] == '0000':
                return False
            
            previous_block = block
        return True
