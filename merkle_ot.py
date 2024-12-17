
from merkle_tree import MerkleTree, hash_function
import secrets
import os
class MerkleBasedOT:
    def __init__(self, secrets):
        self.merkle_tree = MerkleTree(secrets)
        self.root = self.merkle_tree.get_root()

    def add_secret(self, new_secret):
        self.merkle_tree.add_secret(new_secret)
        self.root = self.merkle_tree.get_root()

    def remove_secret(self, index):
        self.merkle_tree.remove_secret(index)
        self.root = self.merkle_tree.get_root()

    def get_root(self):
        return self.root

    def sender_response(self, index):
        proof = self.merkle_tree.get_proof(index)
        leaf = self.merkle_tree.leaves[index]
        salt = self.merkle_tree.salts[index]
        return leaf, proof, salt

    def receiver_verify(self, root, leaf, proof, salt, secret, index):
        expected_leaf = hash_function(secret + salt)
        if leaf != expected_leaf:
            return False

        computed_root = leaf
        for sibling in proof:
            if index % 2 == 0:
                computed_root = hash_function(computed_root + sibling)
            else:
                computed_root = hash_function(sibling + computed_root)
            index //= 2
        return computed_root == root

# Testing the Integrated Protocol
if __name__ == "__main__":
    # Initial secrets
    secrets = [os.urandom(32) for _ in range(8)]

    # Initialize the OT system
    ot_system = MerkleBasedOT(secrets)
    print("Initial Merkle Root:", ot_system.get_root().hex())

    # Receiver requests a specific secret
    desired_index = 3
    print(f"\nReceiver requests secret at index {desired_index}.")

    # Sender provides the proof and leaf
    leaf, proof, salt = ot_system.sender_response(desired_index)

    # Receiver verifies the proof
    is_valid = ot_system.receiver_verify(ot_system.get_root(), leaf, proof, desired_index)
    print("Verification Successful:", is_valid)

    # Add a new secret dynamically
    new_secret = os.urandom(32)
    print("\nAdding a new secret...")
    ot_system.add_secret(new_secret)
    print("Updated Merkle Root:", ot_system.get_root().hex())

    # Receiver requests the newly added secret
    new_index = len(ot_system.merkle_tree.leaves) - 1
    print(f"\nReceiver requests newly added secret at index {new_index}.")
    leaf, proof, salt = ot_system.sender_response(new_index)
    is_valid = ot_system.receiver_verify(ot_system.get_root(), leaf, proof, new_index)
    print("Verification Successful:", is_valid)

    # Remove a secret
    print("\nRemoving a secret at index 2...")
    ot_system.remove_secret(2)
    print("Updated Merkle Root after removal:", ot_system.get_root().hex())