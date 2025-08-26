# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2024.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Quantum Blockchain implementation using quantum entanglement and cryptographic primitives.
"""

from __future__ import annotations

import hashlib
import time
from typing import List, Optional, Tuple, Union
import numpy as np

from qiskit.circuit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.quantum_info import Statevector, random_statevector, partial_trace
from qiskit.quantum_info.operators import Pauli
from qiskit.exceptions import QiskitError


class QuantumBlock:
    """A quantum block in the quantum blockchain.
    
    Each block contains:
    - Classical data (transaction information)
    - Quantum state that links to the previous block through entanglement
    - Quantum hash for integrity verification
    - Timestamp
    """

    def __init__(
        self,
        data: str,
        previous_hash: str = "0",
        quantum_state: Optional[Statevector] = None,
        nonce: int = 0
    ):
        """Initialize a quantum block.
        
        Args:
            data: Classical data to store in the block
            previous_hash: Hash of the previous block
            quantum_state: Quantum state linking to previous block
            nonce: Nonce for proof of work
        """
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        
        # Initialize quantum state if not provided
        if quantum_state is None:
            # Create a random 2-qubit quantum state
            self.quantum_state = random_statevector(4)  # 2 qubits
        else:
            self.quantum_state = quantum_state
            
        # Calculate quantum hash
        self.quantum_hash = self._calculate_quantum_hash()
        self.hash = self._calculate_classical_hash()

    def _calculate_quantum_hash(self) -> str:
        """Calculate quantum hash using quantum state measurement probabilities."""
        # Get measurement probabilities from quantum state
        probs = self.quantum_state.probabilities()
        
        # Create a deterministic hash from probabilities
        prob_str = "".join([f"{p:.10f}" for p in probs])
        quantum_hash = hashlib.sha256(prob_str.encode()).hexdigest()
        
        return quantum_hash

    def _calculate_classical_hash(self) -> str:
        """Calculate classical hash of the block."""
        block_string = (
            str(self.timestamp) + 
            self.data + 
            self.previous_hash + 
            self.quantum_hash + 
            str(self.nonce)
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int = 4) -> None:
        """Mine the block by finding a hash with specified difficulty."""
        target = "0" * difficulty
        
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self._calculate_classical_hash()

    def create_entangled_state(self, previous_state: Statevector) -> Statevector:
        """Create entangled state with the previous block's quantum state.
        
        Args:
            previous_state: Quantum state from the previous block
            
        Returns:
            New entangled quantum state
        """
        # Create a 4-qubit entangled state between current and previous block
        qc = QuantumCircuit(4)
        
        # Initialize with previous state on qubits 0,1
        qc.initialize(previous_state.data, [0, 1])
        
        # Create current block state on qubits 2,3
        qc.initialize(self.quantum_state.data, [2, 3])
        
        # Create entanglement between blocks
        qc.cx(0, 2)  # Entangle between blocks
        qc.cx(1, 3)
        
        # Add some quantum gates for complexity
        qc.ry(np.pi/4, 0)
        qc.ry(np.pi/4, 2)
        
        # Get the final entangled state
        entangled_state = Statevector.from_instruction(qc)
        
        # Extract the new block's portion (qubits 2,3)
        from qiskit.quantum_info import DensityMatrix
        new_state_dm = DensityMatrix(entangled_state)
        traced_dm = partial_trace(new_state_dm, [0, 1])
        
        # Convert density matrix back to statevector (assuming pure state)
        eigenvals, eigenvecs = np.linalg.eigh(traced_dm.data)
        max_idx = np.argmax(eigenvals)
        new_statevector = eigenvecs[:, max_idx]
        
        # Ensure proper normalization
        new_statevector = new_statevector / np.linalg.norm(new_statevector)
        
        return Statevector(new_statevector)


class QuantumBlockchain:
    """A quantum blockchain implementation using quantum entanglement for block linkage."""

    def __init__(self, difficulty: int = 2):
        """Initialize the quantum blockchain.
        
        Args:
            difficulty: Mining difficulty (number of leading zeros required)
        """
        self.chain: List[QuantumBlock] = []
        self.difficulty = difficulty
        self.mining_reward = 10
        
        # Create genesis block
        self._create_genesis_block()

    def _create_genesis_block(self) -> None:
        """Create the first block in the blockchain."""
        genesis_block = QuantumBlock("Genesis Block", "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> QuantumBlock:
        """Get the latest block in the chain."""
        return self.chain[-1]

    def add_block(self, data: str) -> None:
        """Add a new block to the blockchain.
        
        Args:
            data: Data to store in the new block
        """
        previous_block = self.get_latest_block()
        
        # Create new block with quantum entanglement to previous block
        new_block = QuantumBlock(data, previous_block.hash)
        
        # Create entangled quantum state
        entangled_state = new_block.create_entangled_state(previous_block.quantum_state)
        new_block.quantum_state = entangled_state
        
        # Recalculate hashes after quantum state update
        new_block.quantum_hash = new_block._calculate_quantum_hash()
        new_block.hash = new_block._calculate_classical_hash()
        
        # Mine the block
        new_block.mine_block(self.difficulty)
        
        self.chain.append(new_block)

    def is_chain_valid(self) -> bool:
        """Validate the entire blockchain.
        
        Returns:
            True if the blockchain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block's hash is valid
            if current_block.hash != current_block._calculate_classical_hash():
                return False
                
            # Check if current block points to previous block
            if current_block.previous_hash != previous_block.hash:
                return False
                
            # Check quantum hash consistency
            if current_block.quantum_hash != current_block._calculate_quantum_hash():
                return False
                
            # Check if hash meets difficulty requirement
            if not current_block.hash.startswith("0" * self.difficulty):
                return False
                
        return True

    def get_quantum_entanglement_measure(self, block_index: int) -> float:
        """Measure quantum entanglement between consecutive blocks.
        
        Args:
            block_index: Index of the block to measure entanglement for
            
        Returns:
            Entanglement measure between the block and its predecessor
        """
        if block_index == 0 or block_index >= len(self.chain):
            return 0.0
            
        current_block = self.chain[block_index]
        previous_block = self.chain[block_index - 1]
        
        # Create combined state for entanglement calculation
        qc = QuantumCircuit(4)
        qc.initialize(previous_block.quantum_state.data, [0, 1])
        qc.initialize(current_block.quantum_state.data, [2, 3])
        
        from qiskit.quantum_info import DensityMatrix
        combined_state = Statevector.from_instruction(qc)
        
        # Calculate entanglement using von Neumann entropy
        reduced_state = partial_trace(DensityMatrix(combined_state), [2, 3])
        eigenvals = np.linalg.eigvals(reduced_state.data)
        eigenvals = np.real(eigenvals[eigenvals > 1e-10])  # Remove numerical zeros and take real part
        
        if len(eigenvals) == 0:
            return 0.0
            
        entropy = -np.sum(eigenvals * np.log2(eigenvals + 1e-10))
        
        # Ensure non-negative due to numerical precision
        return max(0.0, float(np.real(entropy)))

    def get_blockchain_info(self) -> dict:
        """Get information about the blockchain.
        
        Returns:
            Dictionary containing blockchain statistics
        """
        info = {
            "chain_length": len(self.chain),
            "difficulty": self.difficulty,
            "is_valid": self.is_chain_valid(),
            "total_quantum_entanglement": sum(
                self.get_quantum_entanglement_measure(i) 
                for i in range(1, len(self.chain))
            ),
        }
        
        if len(self.chain) > 1:
            info["average_entanglement"] = info["total_quantum_entanglement"] / (len(self.chain) - 1)
        else:
            info["average_entanglement"] = 0.0
            
        return info

    def quantum_verify_block(self, block_index: int) -> bool:
        """Verify a block using quantum measurements.
        
        Args:
            block_index: Index of block to verify
            
        Returns:
            True if block passes quantum verification
        """
        if block_index >= len(self.chain):
            return False
            
        block = self.chain[block_index]
        
        # Verify quantum state consistency
        try:
            # Measure quantum state in different bases
            x_measurement = block.quantum_state.expectation_value(Pauli("XX"))
            z_measurement = block.quantum_state.expectation_value(Pauli("ZZ"))
            
            # Check if measurements are within expected ranges
            if abs(x_measurement) > 1.0 or abs(z_measurement) > 1.0:
                return False
                
            # Verify quantum hash matches quantum state
            calculated_hash = block._calculate_quantum_hash()
            if calculated_hash != block.quantum_hash:
                return False
                
            return True
            
        except Exception:
            return False