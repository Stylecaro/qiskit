# This code is part of Qiskit.
#
# (C) Copyright IBM 2025.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=missing-function-docstring

"""Test QuantumNFT instruction for quantum circuits."""

from qiskit.circuit import QuantumCircuit, CircuitInstruction
from qiskit.circuit.quantum_nft import QuantumNFT
from qiskit.circuit.exceptions import CircuitError
from test import QiskitTestCase  # pylint: disable=wrong-import-order


class TestQuantumNFTClass(QiskitTestCase):
    """Test QuantumNFT instruction for quantum circuits."""

    def test_quantum_nft_creation(self):
        """Test basic QuantumNFT creation."""
        qnft = QuantumNFT(2, "token_001")
        self.assertEqual(qnft.num_qubits, 2)
        self.assertEqual(qnft.token_id, "token_001")
        self.assertEqual(qnft.metadata, {})
        self.assertEqual(qnft.name, "qnft")

    def test_quantum_nft_with_metadata(self):
        """Test QuantumNFT creation with metadata."""
        metadata = {"name": "MyNFT", "value": 100, "creator": "alice"}
        qnft = QuantumNFT(3, "token_002", metadata)
        self.assertEqual(qnft.token_id, "token_002")
        self.assertEqual(qnft.metadata, metadata)
        # Ensure metadata is copied, not referenced
        metadata["extra"] = "test"
        self.assertNotIn("extra", qnft.metadata)

    def test_quantum_nft_with_label(self):
        """Test QuantumNFT creation with label."""
        qnft = QuantumNFT(1, "token_003", label="my_nft")
        self.assertEqual(qnft.label, "my_nft")

    def test_quantum_nft_inverse(self):
        """Test QuantumNFT inverse method."""
        metadata = {"test": "data"}
        qnft = QuantumNFT(2, "token_004", metadata, "label")
        inverse_qnft = qnft.inverse()
        self.assertEqual(inverse_qnft.num_qubits, qnft.num_qubits)
        self.assertEqual(inverse_qnft.token_id, qnft.token_id)
        self.assertEqual(inverse_qnft.metadata, qnft.metadata)
        self.assertEqual(inverse_qnft.label, qnft.label)

    def test_quantum_nft_repr(self):
        """Test QuantumNFT string representation."""
        qnft = QuantumNFT(2, "token_005")
        expected = "QuantumNFT(num_qubits=2, token_id='token_005')"
        self.assertEqual(repr(qnft), expected)


class TestQuantumCircuitNFT(QiskitTestCase):
    """Test QuantumNFT integration with QuantumCircuit."""

    def test_quantum_nft_circuit_method(self):
        """Test adding QuantumNFT to circuit with quantum_nft method."""
        qc = QuantumCircuit(3)
        qc.h(0)
        qc.quantum_nft(0, 1, token_id="nft_001", metadata={"type": "quantum"})
        
        # Check that the instruction was added
        self.assertEqual(len(qc.data), 2)
        nft_instruction = qc.data[1]
        self.assertIsInstance(nft_instruction, CircuitInstruction)
        self.assertIsInstance(nft_instruction.operation, QuantumNFT)
        self.assertEqual(nft_instruction.operation.token_id, "nft_001")
        self.assertEqual(nft_instruction.operation.metadata, {"type": "quantum"})

    def test_quantum_nft_all_qubits(self):
        """Test QuantumNFT applied to all qubits when no args given."""
        qc = QuantumCircuit(2)
        qc.quantum_nft(token_id="nft_002")
        
        nft_instruction = qc.data[0]
        self.assertEqual(nft_instruction.operation.num_qubits, 2)
        self.assertEqual(len(nft_instruction.qubits), 2)

    def test_quantum_nft_specific_qubits(self):
        """Test QuantumNFT applied to specific qubits."""
        qc = QuantumCircuit(3)
        qc.quantum_nft(0, 2, token_id="nft_003")
        
        nft_instruction = qc.data[0]
        self.assertEqual(nft_instruction.operation.num_qubits, 2)
        self.assertEqual(len(nft_instruction.qubits), 2)
        self.assertEqual(nft_instruction.qubits[0], qc.qubits[0])
        self.assertEqual(nft_instruction.qubits[1], qc.qubits[2])

    def test_quantum_nft_with_label_in_circuit(self):
        """Test QuantumNFT with label in circuit."""
        qc = QuantumCircuit(1)
        qc.quantum_nft(0, token_id="nft_004", label="test_label")
        
        nft_instruction = qc.data[0]
        self.assertEqual(nft_instruction.operation.label, "test_label")

    def test_multiple_quantum_nfts(self):
        """Test adding multiple QuantumNFTs to a circuit."""
        qc = QuantumCircuit(3)
        qc.quantum_nft(0, token_id="nft_1")
        qc.quantum_nft(1, 2, token_id="nft_2", metadata={"multi": True})
        
        self.assertEqual(len(qc.data), 2)
        self.assertEqual(qc.data[0].operation.token_id, "nft_1")
        self.assertEqual(qc.data[1].operation.token_id, "nft_2")
        self.assertEqual(qc.data[1].operation.metadata, {"multi": True})