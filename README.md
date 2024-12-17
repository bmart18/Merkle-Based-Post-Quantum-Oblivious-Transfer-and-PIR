
# Merkle-Based Post-Quantum Oblivious Transfer and PIR

This project provides a **quantum-safe cryptographic framework** using **Merkle Trees** for Oblivious Transfer (OT) and Private Information Retrieval (PIR). It includes optimized implementations for comparison between **Merkle-Based PIR** and a **Naive PIR** solution. The results highlight scalability, security, and efficiency under realistic conditions.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Structure](#structure)
3. [Features](#features)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Testing](#testing)
7. [Performance](#performance)
8. [License](#license)

---

## Project Overview

This repository compares two approaches:
1. **Merkle-Based PIR**: A quantum-safe PIR mechanism leveraging Merkle Trees.
2. **Naive PIR**: A baseline solution using AES-based encryption without tree optimizations.

Additionally, the repository contains:
- **Merkle-Based OT (Oblivious Transfer)** implementation.
- Performance benchmarks on different dataset sizes.

---

## Structure

The repository consists of the following components:

```
.
├── merkle_tree.py       # Merkle Tree implementation with dynamic updates
├── merkle_pir.py        # Merkle-Based PIR
├── naive_pir.py         # Naive PIR implementation
├── merkle_ot.py         # Merkle-Based Oblivious Transfer (OT)
├── test_pir.py          # Benchmarking script for PIR comparison
├── title_page.txt       # Project title and abstract
└── README.md            # Documentation
```

---

## Features

### 1. **Merkle Tree**
- Efficient dynamic updates (add/remove secrets).
- Uses **BLAKE3** for quantum-safe hashing.
- Generates proofs for integrity verification.

### 2. **Merkle-Based PIR**
- Optimized for large datasets.
- Quantum-resistant cryptographic framework.
- Proof generation and verification for secure retrieval.

### 3. **Naive PIR**
- AES encryption with record-based verification.
- Baseline comparison for performance benchmarking.

### 4. **Merkle-Based OT**
- Extends Merkle Tree for Oblivious Transfer (OT) with sender/receiver interaction.
- Verifiable proofs of integrity for secure OT.

---

## Installation

### Requirements:
- Python 3.8+
- Required Libraries:
    - `blake3`
    - `cryptography`
    - `os`
    - `secrets`

### Steps:
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repository.git
   cd your-repository
   ```
2. Install dependencies:
   ```bash
   pip install blake3 cryptography
   ```

---

## Usage

### **Merkle-Based PIR**

Example of querying a record securely:
```python
from merkle_pir import MerklePIR
import os

# Generate records
records = [os.urandom(32) for _ in range(10)]
query_index = 2

# Initialize and query
pir = MerklePIR(records)
record, proof = pir.query(query_index)

# Verify record integrity
is_valid = pir.verify(pir.root, record, proof, query_index)
print("Record Valid:", is_valid)
```

### **Naive PIR**

Example of querying a record:
```python
from naive_pir import NaivePIR

# Generate records
records = [b"record" + bytes([i]) for i in range(10)]
query_index = 3

# Query and decrypt
pir = NaivePIR(records)
encrypted_record, key = pir.query(query_index)
decrypted_record = pir.decrypt(encrypted_record, key)

# Verify
is_valid = pir.verify(records[query_index], decrypted_record)
print("Record Valid:", is_valid)
```

---

## Testing

To run benchmarks and test performance:
```bash
python test_pir.py
```

Results include:
- Query and verification times for both **Merkle-Based PIR** and **Naive PIR**.
- Scalability with datasets of size 10K, 100K, and 1M records.

---

## Performance

The project highlights:
1. Scalability of Merkle-Based PIR for large datasets.
2. Comparison of efficiency with Naive PIR.
3. **Quantum-safe** guarantees using **BLAKE3** hashing.

Sample Output (Test Run):
```
Testing with 10000 records...
Merkle-Based PIR Query Time: 0.002143 seconds
Merkle-Based PIR Verification Successful: True
Naive PIR Query Time: 0.001345 seconds
Naive PIR Verification Successful: True
```

---

## License

This project is licensed under the MIT License. 
