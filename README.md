# 🛡️ Zero-Knowledge Proof (ZKP) Dark Pool Simulator

A privacy-preserving financial matching engine simulating a Dark Pool exchange utilizing cryptographic commitments and simulated **zk-SNARK** overhead profiling.

This project bridges advanced financial cryptography with market microstructure, demonstrating how institutional order flow can be matched without exposing intent to the public ledger or the central exchange operator.

---

## 🧠 The Market Microstructure Problem

### 1. The Vulnerability of Dark Pools
Institutional investors use "Dark Pools" to trade massive blocks of stock (e.g., 500,000 shares of Apple) without tipping off the public market and causing the price to crash before their order fills. However, current Dark Pools require the trader to trust the central exchange operator with their order data. Corrupt operators have historically front-run their own clients using this privileged information.

### 2. The Cryptographic Solution
By utilizing **Zero-Knowledge Proofs**, a trader can prove to the exchange: *"I have the funds, and my order crosses with another order in the pool,"* **without ever revealing the actual price or volume to the exchange server.**
* The exchange acts strictly as a blind cryptographic verifier.
* Order flow toxicity and front-running become mathematically impossible.

---

## ⚙️ Engine Architecture & Simulation

This Python-based engine simulates the end-to-end flow of a ZKP-secured exchange:
1. **Cryptographic Commitments:** Traders submit orders hidden behind cryptographic hashes (simulating Pedersen Commitments using salted SHA-256).
2. **Proof Generation:** The engine simulates the heavy computational overhead required to generate a zk-SNARK proof on the client side.
3. **$O(1)$ Verification:** The exchange verifies the proof in constant time, allowing it to approve the order for the matching engine without ever decrypting the payload.

### 🏎️ Latency & Overhead Benchmarking
Because computational latency is the enemy of High-Frequency Trading, this engine includes a quantitative profiler. It directly compares the $O(n)$ scaling latency of a standard "Lit" exchange (Cleartext Matching) against the heavily scaled latency of generating ZK-Proofs, visualizing the tradeoff between absolute privacy and tick-to-trade speed.

---

## 📊 Interactive Dashboard Output

The engine utilizes `PyQt5` to render a 2-panel quantitative dashboard analyzing the microstructure overhead:
1. **Cumulative Latency (Log Scale):** ZK-Proof Generation vs. Cleartext Matching.
2. **Verification Overhead:** Demonstrating the flat, $O(1)$ verification time allowing the central exchange to process securely without bottlenecking.





https://github.com/user-attachments/assets/95b3736c-e0a5-49c5-b9ae-cdbcf7c40e2b





---

## 💻 Quick Start

```bash
# Clone the repository
git clone [https://github.com/Snoob965/zkp_darkpool_simulator.git](https://github.com/Snoob965/zkp_darkpool_simulator.git)
cd zkp_darkpool_simulator

# Install dependencies
pip install numpy matplotlib PyQt5

# Run the engine and launch the ZKP profiler dashboard
python darkpool_engine.py
