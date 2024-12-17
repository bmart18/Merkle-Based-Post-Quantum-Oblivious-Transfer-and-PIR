
import hashlib
import os
import secrets
import blake3
from concurrent.futures import ThreadPoolExecutor

# Quantum-safe hash function

# Merkle Tree class with lazy rebalancing
def hash_function(data):
    return blake3.blake3(data).digest()
class MerkleTree:
    def __init__(self, secrets):
        self.secrets = secrets
        self.salts = [os.urandom(16) for _ in secrets]  # Generate random salts
        self.leaves = [hash_function(secret + salt) for secret, salt in zip(secrets, self.salts)]
        self.tree = []
        self.build_tree()

    def build_tree(self):
        """Build the initial Merkle tree from all leaves."""

        level = self.leaves
        self.tree = [level]  # Store all levels of the tree
        while len(level) > 1:
            next_level = []
            for i in range(0, len(level), 2):
                left = level[i]
                right = level[i + 1] if i + 1 < len(level) else left
                next_level.append(hash_function(left + right))
            self.tree.append(next_level)
            level = next_level

    def get_root(self):
        return self.tree[-1][0] if self.tree else None

    def get_proof(self, index):
        """Generate Merkle proof for a specific leaf."""
        proof = []
        node_index = index
        for level in self.tree[:-1]:
            sibling_index = node_index ^ 1  # XOR to find sibling index
            if sibling_index < len(level):
                proof.append(level[sibling_index])
            node_index //= 2
        return proof

    def add_secret(self, new_secret):
        """Incrementally add a new secret to the Merkle tree."""
        salt = os.urandom(16)
        new_leaf = hash_function(new_secret + salt)

        # Update salts and leaves
        self.secrets.append(new_secret)
        self.salts.append(salt)
        self.leaves.append(new_leaf)

        # Incrementally update the tree
        self.incremental_update(new_leaf)

    def incremental_update(self, new_leaf):
        """Update the Merkle tree incrementally."""
        # Start at the new leaf
        current_hash = new_leaf
        current_index = len(self.leaves) - 1

        for level_index in range(len(self.tree)):
            level = self.tree[level_index]

            # If level is full, start a new level
            if current_index % 2 == 0 and current_index + 1 == len(level):
                if len(self.tree) <= level_index + 1:
                    self.tree.append([])  # Create a new level
                self.tree[level_index + 1].append(current_hash)
                break
            else:
                # Update the current level
                sibling_index = current_index ^ 1
                sibling_hash = level[sibling_index] if sibling_index < len(level) else current_hash
                parent_hash = hash_function(min(current_hash, sibling_hash) + max(current_hash, sibling_hash))

                # Add parent hash to the next level
                if len(self.tree) <= level_index + 1:
                    self.tree.append([])
                self.tree[level_index + 1].append(parent_hash)

                # Update for the next level
                current_hash = parent_hash
                current_index //= 2

    def remove_secret(self, index):
        """Mark a leaf for deletion and rebuild only affected paths."""
        # Mark the leaf as deleted (e.g., replace with a fixed value)
        self.secrets[index] = b""
        self.leaves[index] = hash_function(b"deleted" + self.salts[index])

        # Incrementally update paths affected by the change
        self.rebuild_affected_paths(index)

    def rebuild_affected_paths(self, index):
        """Recompute only the paths from the changed leaf to the root."""
        current_hash = self.leaves[index]
        current_index = index

        for level_index in range(len(self.tree) - 1):
            level = self.tree[level_index]
            sibling_index = current_index ^ 1
            sibling_hash = level[sibling_index] if sibling_index < len(level) else current_hash

            # Compute parent hash
            parent_hash = hash_function(min(current_hash, sibling_hash) + max(current_hash, sibling_hash))
            self.tree[level_index + 1][current_index // 2] = parent_hash

            # Update for the next level
            current_hash = parent_hash
            current_index //= 2

# Testing Dynamic Updates
if __name__ == "__main__":
    # Secrets
    secrets = [os.urandom(32) for _ in range(4)]

    # Build Merkle tree
    merkle_tree = MerkleTree(secrets)
    print("Initial Merkle Root:", merkle_tree.get_root().hex())

    # Add a new secret dynamically
    new_secret = os.urandom(32)
    merkle_tree.add_secret(new_secret)
    print("Updated Merkle Root (after addition):", merkle_tree.get_root().hex())

    # Remove a secret
    merkle_tree.remove_secret(1)
    print("Updated Merkle Root (after removal):", merkle_tree.get_root().hex())
