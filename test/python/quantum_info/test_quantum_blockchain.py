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

"""Test quantum blockchain functionality."""

import unittest
import numpy as np

from qiskit.quantum_info import QuantumBlockchain, QuantumBlock, Statevector
from test import QiskitTestCase


class TestQuantumBlock(QiskitTestCase):
    """Tests for QuantumBlock class."""

    def test_quantum_block_creation(self):
        """Test basic quantum block creation."""
        block = QuantumBlock("Test data")
        
        self.assertIsInstance(block.quantum_state, Statevector)
        self.assertEqual(block.data, "Test data")
        self.assertEqual(block.previous_hash, "0")
        self.assertIsNotNone(block.quantum_hash)
        self.assertIsNotNone(block.hash)
        self.assertGreater(block.timestamp, 0)

    def test_quantum_hash_consistency(self):
        """Test that quantum hash is consistent with quantum state."""
        block = QuantumBlock("Test data")
        original_hash = block.quantum_hash
        
        # Recalculate hash
        recalculated_hash = block._calculate_quantum_hash()
        
        self.assertEqual(original_hash, recalculated_hash)

    def test_block_mining(self):
        """Test block mining functionality."""
        block = QuantumBlock("Test mining")
        
        # Mine with difficulty 2
        block.mine_block(difficulty=2)
        
        # Check that hash starts with required zeros
        self.assertTrue(block.hash.startswith("00"))
        self.assertGreater(block.nonce, 0)

    def test_entangled_state_creation(self):
        """Test creation of entangled states between blocks."""
        # Create two blocks
        block1 = QuantumBlock("Block 1")
        block2 = QuantumBlock("Block 2")
        
        # Create entangled state
        entangled_state = block2.create_entangled_state(block1.quantum_state)
        
        self.assertIsInstance(entangled_state, Statevector)
        self.assertEqual(len(entangled_state), 4)  # 2-qubit state


class TestQuantumBlockchain(QiskitTestCase):
    """Tests for QuantumBlockchain class."""

    def test_blockchain_creation(self):
        """Test basic blockchain creation."""
        blockchain = QuantumBlockchain(difficulty=1)
        
        # Should have genesis block
        self.assertEqual(len(blockchain.chain), 1)
        self.assertEqual(blockchain.chain[0].data, "Genesis Block")
        self.assertEqual(blockchain.difficulty, 1)

    def test_add_block(self):
        """Test adding blocks to the blockchain."""
        blockchain = QuantumBlockchain(difficulty=1)
        
        # Add a block
        blockchain.add_block("First block")
        
        self.assertEqual(len(blockchain.chain), 2)
        self.assertEqual(blockchain.chain[1].data, "First block")
        
        # Check that previous hash is set correctly
        self.assertEqual(
            blockchain.chain[1].previous_hash,
            blockchain.chain[0].hash
        )

    def test_blockchain_validation(self):
        """Test blockchain validation."""
        blockchain = QuantumBlockchain(difficulty=1)
        
        # Add some blocks
        blockchain.add_block("Block 1")
        blockchain.add_block("Block 2")
        
        # Should be valid
        self.assertTrue(blockchain.is_chain_valid())
        
        # Tamper with a block
        blockchain.chain[1].data = "Tampered data"
        
        # Should now be invalid
        self.assertFalse(blockchain.is_chain_valid())

    def test_quantum_entanglement_measure(self):
        """Test quantum entanglement measurement between blocks."""
        blockchain = QuantumBlockchain(difficulty=1)
        blockchain.add_block("Block 1")
        blockchain.add_block("Block 2")
        
        # Measure entanglement
        entanglement = blockchain.get_quantum_entanglement_measure(1)
        
        # Should be a positive value for entangled blocks
        self.assertGreaterEqual(entanglement, 0.0)
        self.assertLessEqual(entanglement, 2.0)  # Max entropy for 2 qubits

    def test_blockchain_info(self):
        """Test blockchain information retrieval."""
        blockchain = QuantumBlockchain(difficulty=2)
        blockchain.add_block("Block 1")
        blockchain.add_block("Block 2")
        
        info = blockchain.get_blockchain_info()
        
        self.assertEqual(info["chain_length"], 3)  # Genesis + 2 blocks
        self.assertEqual(info["difficulty"], 2)
        self.assertTrue(info["is_valid"])
        self.assertGreaterEqual(info["total_quantum_entanglement"], 0.0)
        self.assertGreaterEqual(info["average_entanglement"], 0.0)

    def test_quantum_block_verification(self):
        """Test quantum verification of blocks."""
        blockchain = QuantumBlockchain(difficulty=1)
        blockchain.add_block("Test block")
        
        # Verify the block
        self.assertTrue(blockchain.quantum_verify_block(0))  # Genesis
        self.assertTrue(blockchain.quantum_verify_block(1))  # Added block
        
        # Invalid index should return False
        self.assertFalse(blockchain.quantum_verify_block(10))

    def test_multiple_blocks_consistency(self):
        """Test consistency when adding multiple blocks."""
        blockchain = QuantumBlockchain(difficulty=1)
        
        # Add multiple blocks
        for i in range(5):
            blockchain.add_block(f"Block {i}")
        
        # Check all blocks are properly linked
        self.assertEqual(len(blockchain.chain), 6)  # Genesis + 5 blocks
        self.assertTrue(blockchain.is_chain_valid())
        
        # Check quantum verification for all blocks
        for i in range(len(blockchain.chain)):
            self.assertTrue(blockchain.quantum_verify_block(i))

    def test_quantum_state_properties(self):
        """Test properties of quantum states in blocks."""
        blockchain = QuantumBlockchain(difficulty=1)
        blockchain.add_block("Quantum test")
        
        block = blockchain.chain[1]
        
        # Check quantum state is normalized
        self.assertAlmostEqual(
            np.sum(block.quantum_state.probabilities()), 1.0, places=10
        )
        
        # Check quantum state is valid
        self.assertTrue(block.quantum_state.is_valid())

    def test_genesis_block_properties(self):
        """Test properties of the genesis block."""
        blockchain = QuantumBlockchain(difficulty=2)
        genesis = blockchain.chain[0]
        
        self.assertEqual(genesis.data, "Genesis Block")
        self.assertEqual(genesis.previous_hash, "0")
        self.assertTrue(genesis.hash.startswith("00"))  # Meets difficulty
        self.assertIsInstance(genesis.quantum_state, Statevector)

    def test_empty_data_block(self):
        """Test adding block with empty data."""
        blockchain = QuantumBlockchain(difficulty=1)
        blockchain.add_block("")
        
        self.assertEqual(len(blockchain.chain), 2)
        self.assertEqual(blockchain.chain[1].data, "")
        self.assertTrue(blockchain.is_chain_valid())

    def test_large_data_block(self):
        """Test adding block with large data."""
        blockchain = QuantumBlockchain(difficulty=1)
        large_data = "A" * 1000  # 1000 character string
        
        blockchain.add_block(large_data)
        
        self.assertEqual(len(blockchain.chain), 2)
        self.assertEqual(blockchain.chain[1].data, large_data)
        self.assertTrue(blockchain.is_chain_valid())


if __name__ == "__main__":
    unittest.main()