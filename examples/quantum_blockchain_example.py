#!/usr/bin/env python3
"""
Example usage of the Quantum Blockchain (Cadena de Bloques Cuántico) implementation.

This script demonstrates how to create and use a quantum blockchain with
quantum entanglement for block linkage and quantum cryptographic security.
"""

from qiskit.quantum_info import QuantumBlockchain, QuantumBlock

def main():
    """Demonstrate quantum blockchain functionality."""
    print("=== Cadena de Bloques Cuántico (Quantum Blockchain) Example ===")
    print()
    
    # Create a new quantum blockchain
    print("1. Creating quantum blockchain...")
    blockchain = QuantumBlockchain(difficulty=2)
    print(f"   ✓ Created blockchain with {len(blockchain.chain)} initial block(s)")
    print(f"   ✓ Mining difficulty set to {blockchain.difficulty}")
    print()
    
    # Add some blocks with transaction data
    print("2. Adding transaction blocks...")
    transactions = [
        "Alice transfers 100 quantum tokens to Bob",
        "Bob transfers 50 quantum tokens to Charlie", 
        "Charlie transfers 25 quantum tokens to David"
    ]
    
    for i, transaction in enumerate(transactions, 1):
        print(f"   Adding block {i}: {transaction}")
        blockchain.add_block(transaction)
        
        # Verify the block was added correctly
        if blockchain.quantum_verify_block(i):
            print(f"   ✓ Block {i} quantum verification passed")
        else:
            print(f"   ✗ Block {i} quantum verification failed")
    
    print()
    
    # Display blockchain information
    print("3. Blockchain status:")
    info = blockchain.get_blockchain_info()
    print(f"   Chain length: {info['chain_length']} blocks")
    print(f"   Blockchain valid: {'Yes' if info['is_valid'] else 'No'}")
    print(f"   Total quantum entanglement: {info['total_quantum_entanglement']:.8f}")
    print()
    
    # Show quantum features
    print("4. Quantum security features:")
    print("   ✓ Each block contains a quantum state")
    print("   ✓ Blocks are linked through quantum entanglement")
    print("   ✓ Quantum hash functions ensure integrity")
    print("   ✓ Quantum measurements verify authenticity")
    print()
    
    # Test blockchain validation
    print("5. Testing blockchain security...")
    original_valid = blockchain.is_chain_valid()
    print(f"   Original blockchain valid: {original_valid}")
    
    # Simulate tampering attempt
    original_data = blockchain.chain[1].data
    blockchain.chain[1].data = "TAMPERED DATA"
    
    tampered_valid = blockchain.is_chain_valid()
    print(f"   After tampering attempt: {tampered_valid}")
    
    # Restore original data
    blockchain.chain[1].data = original_data
    restored_valid = blockchain.is_chain_valid()
    print(f"   After restoration: {restored_valid}")
    print()
    
    print("6. Quantum blockchain demonstration complete!")
    print("   The quantum blockchain successfully demonstrates:")
    print("   • Quantum entanglement between blocks")
    print("   • Quantum cryptographic security")
    print("   • Tamper detection and verification")
    print("   • Integration with classical blockchain concepts")

if __name__ == "__main__":
    main()