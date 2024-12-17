import time
import os
from merkle_pir import MerklePIR
from naive_pir import NaivePIR
import gc

# Generate random records
def generate_records(num_records, record_size=32):
    return [os.urandom(record_size) for _ in range(num_records)]


# Test both methods
def test_pir_methods():
    dataset_sizes = [10000, 100000, 1000000]  # Varying dataset sizes
    query_index = 500  # Fixed query index for consistency

    for size in dataset_sizes:
        print(f"\nTesting with {size} records...")

        # Generate dataset
        records = generate_records(size)

        # Test Merkle-Based PIR
        print("Testing Merkle-Based PIR...")
        merkle_pir = MerklePIR(records)
        start_time = time.perf_counter()
        record, proof = merkle_pir.query(query_index)
        query_time = time.perf_counter() - start_time
        print(f"Merkle-Based PIR Query Time: {query_time:.6f} seconds")

        start_time = time.perf_counter()
        is_valid = merkle_pir.verify(merkle_pir.root, record, proof, query_index)
        verify_time = time.perf_counter() - start_time
        print(f"Merkle-Based PIR Verify Time: {verify_time:.6f} seconds")
        print("Merkle-Based PIR Verification Successful:", is_valid)

        # Test Naive PIR
        print("Testing Naive PIR...")
        naive_pir = NaivePIR(records)
        start_time = time.perf_counter()
        encrypted_record, key = naive_pir.query(query_index)
        query_time = time.perf_counter() - start_time
        print(f"Naive PIR Query Time: {query_time:.6f} seconds")

        start_time = time.perf_counter()
        decrypted_record = naive_pir.decrypt(encrypted_record, key)
        is_valid = naive_pir.verify(records[query_index], decrypted_record)
        verify_time = time.perf_counter() - start_time
        print(f"Naive PIR Verify Time: {verify_time:.6f} seconds")
        print("Naive PIR Verification Successful:", is_valid)

        print("Garbage collection")
        gc.collect()

# Run the tests
if __name__ == "__main__":
    test_pir_methods()
