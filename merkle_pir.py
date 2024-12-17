
from merkle_tree import MerkleTree
import hashlib
import blake3
# Quantum-safe hash function
def hash_function(data):
    return blake3.blake3(data).digest()
class MerklePIR:
    def __init__(self, records):
        self.tree = MerkleTree(records)
        self.root = self.tree.get_root()

    def query(self, index):
        """Client query: request a record and its proof."""
        proof = self.tree.get_proof(index)
        record = self.tree.secrets[index]
        return record, proof

    def verify(self, root, record, proof, index):
        """Verify the integrity of the retrieved record."""
        leaf = hash_function(record + self.tree.salts[index])
        computed_root = leaf
        for sibling in proof:
            if index % 2 == 0:
                computed_root = hash_function(computed_root + sibling)
            else:
                computed_root = hash_function(sibling + computed_root)
            index //= 2
        #print(computed_root, root)
        return computed_root == root
