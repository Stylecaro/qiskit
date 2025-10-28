import React, { useState } from "react";

function App() {
  const [tokenId, setTokenId] = useState("");
  const [metadata, setMetadata] = useState("{}");
  const [result, setResult] = useState("");
  const [blockchain, setBlockchain] = useState(null);
  const [aiResult, setAiResult] = useState("");

  const createNFT = async () => {
    try {
      const response = await fetch("http://localhost:8000/nft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          token_id: tokenId,
          metadata: JSON.parse(metadata)
        })
      });
      const data = await response.json();
      setResult(data.message);
      getBlockchain(); // Actualizar blockchain
    } catch (err) {
      setResult("Error: " + err.message);
    }
  };

  const getBlockchain = async () => {
    const response = await fetch("http://localhost:8000/blockchain");
    const data = await response.json();
    setBlockchain(data);
  };

  const getQuantumAI = async () => {
    const response = await fetch("http://localhost:8000/quantum-ai");
    const data = await response.json();
    setAiResult(data.message);
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>Quantum Web3</h1>
      <input
        value={tokenId}
        onChange={e => setTokenId(e.target.value)}
        placeholder="Token ID"
        style={{ marginRight: 10 }}
      />
      <input
        value={metadata}
        onChange={e => setMetadata(e.target.value)}
        placeholder='Metadata (JSON: {"name": "Alice"})'
        style={{ marginRight: 10 }}
      />
      <button onClick={createNFT}>Crear NFT Cuántico</button>
      <div style={{ marginTop: 20 }}>{result}</div>
      <button onClick={getBlockchain} style={{ marginTop: 20 }}>
        Ver Blockchain Cuántica
      </button>
      <pre>{blockchain && JSON.stringify(blockchain, null, 2)}</pre>
      <button onClick={getQuantumAI} style={{ marginTop: 20 }}>
        Consultar AI Cuántica
      </button>
      <div style={{ marginTop: 20 }}>{aiResult}</div>
    </div>
  );
}

export default App;