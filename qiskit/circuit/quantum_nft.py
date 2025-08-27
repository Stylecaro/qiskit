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

"""Quantum NFT instruction.

Can be applied to a :class:`~qiskit.circuit.QuantumCircuit`
with the :meth:`~qiskit.circuit.QuantumCircuit.quantum_nft` method.
"""

from __future__ import annotations

from qiskit.circuit.instruction import Instruction


class QuantumNFT(Instruction):
    """A quantum NFT (Non-Fungible Token) instruction that represents
    a unique quantum state or quantum data with associated metadata.
    
    This instruction can be used to mark qubits as containing quantum NFT data
    with unique identifiers and metadata.
    """

    _directive = True

    def __init__(self, num_qubits: int, token_id: str, metadata: dict = None, label: str | None = None):
        """
        Args:
            num_qubits: the number of qubits for the quantum NFT.
            token_id: unique identifier for this quantum NFT.
            metadata: optional metadata dictionary for the NFT.
            label: the optional label of this quantum NFT.
        """
        self._token_id = token_id
        self._metadata = (metadata or {}).copy()  # Make a copy to avoid reference issues
        self._label = label
        super().__init__("qnft", num_qubits, 0, [], label=label)

    @property
    def token_id(self) -> str:
        """Return the unique token ID of this quantum NFT."""
        return self._token_id

    @property
    def metadata(self) -> dict:
        """Return the metadata dictionary of this quantum NFT."""
        return self._metadata.copy()

    def inverse(self, annotated: bool = False):
        """Special case. Return self."""
        return QuantumNFT(self.num_qubits, self._token_id, self._metadata, self._label)

    def __repr__(self):
        return f"QuantumNFT(num_qubits={self.num_qubits}, token_id='{self._token_id}')"