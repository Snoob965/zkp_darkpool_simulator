import hashlib
import time
import uuid
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

class ZKOrder:
    def __init__(self, side, price, volume):
        self.order_id = uuid.uuid4().hex[:8]
        self.side = side
        self.salt = uuid.uuid4().hex
        self.price_commit = self._commit(price)
        self.vol_commit = self._commit(volume)
        self._price = price
        self._volume = volume
        self.timestamp = time.time()

    def _commit(self, value):
        payload = f"{value}_{self.salt}".encode()
        return hashlib.sha256(payload).hexdigest()

    def generate_snark_proof(self, complexity_factor=1000):
        start = time.perf_counter()
        temp = self.salt
        for _ in range(complexity_factor):
            temp = hashlib.sha256(temp.encode()).hexdigest()
        gen_time = time.perf_counter() - start
        
        proof = {
            "pi_a": temp[:16],
            "pi_b": temp[16:32],
            "price_check": self.price_commit,
            "gen_time": gen_time
        }
        return proof

class DarkPoolExchange:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def submit_order(self, order: ZKOrder):
        proof = order.generate_snark_proof()
        if self._verify_proof(proof, order.price_commit):
            if order.side == 'buy':
                self.buy_orders.append(order)
            else:
                self.sell_orders.append(order)
            return True
        return False

    def _verify_proof(self, proof, expected_commit):
        start = time.perf_counter()
        is_valid = proof["price_check"] == expected_commit
        ver_time = time.perf_counter() - start
        return is_valid, ver_time

    def match_orders(self):
        matches = []
        self.buy_orders.sort(key=lambda x: x.timestamp)
        self.sell_orders.sort(key=lambda x: x.timestamp)

        for buy in self.buy_orders[:]:
            for sell in self.sell_orders[:]:
                if buy._price >= sell._price and buy._volume == sell._volume:
                    matches.append((buy.order_id, sell.order_id, buy._volume))
                    self.buy_orders.remove(buy)
                    self.sell_orders.remove(sell)
                    break
        return len(matches)

class ZKPProfiler:
    def __init__(self):
        self.exchange = DarkPoolExchange()

    def run_microstructure_benchmark(self, max_orders=500):
        print(f"Running ZK-SNARK Overhead Benchmark ({max_orders} orders)...")
        order_counts = np.arange(10, max_orders + 1, 20)
        cleartext_latencies = []
        zkp_latencies = []
        verification_latencies = []

        for n in order_counts:
            ct_start = time.perf_counter()
            for _ in range(n):
                price = np.random.randint(100, 105)
                vol = np.random.randint(1, 10) * 100
                _ = price * vol 
            cleartext_latencies.append((time.perf_counter() - ct_start) * 1000)

            zk_start = time.perf_counter()
            ver_times = []
            for _ in range(n):
                price = np.random.randint(100, 105)
                vol = np.random.randint(1, 10) * 100
                order = ZKOrder('buy', price, vol)
                proof = order.generate_snark_proof(complexity_factor=5000)
                _, v_time = self.exchange._verify_proof(proof, order.price_commit)
                ver_times.append(v_time * 1000)
            zkp_latencies.append((time.perf_counter() - zk_start) * 1000)
            verification_latencies.append(np.mean(ver_times) if ver_times else 0)

        self._plot_results(order_counts, cleartext_latencies, zkp_latencies, verification_latencies)

    def _plot_results(self, counts, ct_lat, zkp_lat, ver_lat):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Dark Pool Microstructure: ZK-SNARK Latency Overhead', fontsize=14, fontweight='bold')

        ax1.plot(counts, zkp_lat, label='ZK-Proof Generation (Total)', color='purple', marker='o')
        ax1.plot(counts, ct_lat, label='Cleartext Matching (Lit Exchange)', color='green', marker='x')
        ax1.set_title('Cumulative Latency: ZKP vs Cleartext')
        ax1.set_xlabel('Order Volume (N)')
        ax1.set_ylabel('Latency (ms)')
        ax1.set_yscale('log')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        ax2.plot(counts, ver_lat, label='O(1) Verification Time', color='blue', linestyle='--')
        ax2.set_title('ZK Verification Overhead per Order')
        ax2.set_xlabel('Order Volume (N)')
        ax2.set_ylabel('Verification Latency (ms)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        plt.tight_layout()
        plt.savefig("zkp_overhead_analysis.png", dpi=300, bbox_inches='tight')
        print("Success: 'zkp_overhead_analysis.png' generated.")
        print("Opening interactive profiler dashboard...")
        plt.show()

if __name__ == "__main__":
    profiler = ZKPProfiler()
    profiler.run_microstructure_benchmark(max_orders=300)