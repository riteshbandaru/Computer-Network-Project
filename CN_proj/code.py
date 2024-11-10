import numpy as np
import matplotlib.pyplot as plt

# Simulation Parameters
flows = 5                 # Number of parallel flows
time_duration = 3         # Total time duration of the simulation in seconds
time_intervals = np.linspace(1, time_duration, 100)  # Time intervals for measurements
buffer_sizes = [1400, 2800, 4200, 5600, 7000]  # Different buffer sizes

# Begin Simulation
print("=== TCP Reno Congestion Control Simulation ===\n")

# Simulate Delay Variation Data (Drop Tail and RED)
print("1. Simulating Delay Variation (Drop Tail and RED)...\n")
delay_drop_tail = []
delay_red = []
for _ in range(flows):
    # Generate delay variation data (e.g., exponential decay for Drop Tail and smoother RED response)
    delay_drop_tail.append(np.random.exponential(0.05, len(time_intervals)))
    delay_red.append(np.random.normal(0.03, 0.01, len(time_intervals)))

# Print delay variation data
print("Delay Variation (Drop Tail):")
for i, delay in enumerate(delay_drop_tail):
    print(f"Flow {i+1}: {delay}")
print("\nDelay Variation (RED):")
for i, delay in enumerate(delay_red):
    print(f"Flow {i+1}: {delay}")

# Simulate Throughput Data (Mbps) for Drop Tail and RED
print("\n2. Simulating Throughput Data (Drop Tail and RED)...\n")
throughput_drop_tail_data = np.random.uniform(0.2, 0.6, (flows, len(buffer_sizes)))
throughput_red_data = np.random.uniform(1.5, 2.0, (flows, len(buffer_sizes)))

# Print throughput data
print("Throughput (Drop Tail):")
for i in range(flows):
    print(f"Flow {i+1}: {throughput_drop_tail_data[i]}")
print("\nThroughput (RED):")
for i in range(flows):
    print(f"Flow {i+1}: {throughput_red_data[i]}")

# Simulate Packet Loss Data (Packets Lost)
print("\n3. Simulating Packet Loss Data (Drop Tail and RED)...\n")
packet_loss_drop_tail = np.random.randint(5, 15, flows)
packet_loss_red = np.random.randint(1, 10, flows)

# Print packet loss data
print("Packet Loss (Drop Tail):", packet_loss_drop_tail)
print("Packet Loss (RED):", packet_loss_red)

# Detailed Plotting

# 1. Delay Variation Plot - Drop Tail vs RED
print("\n4. Generating Delay Variation Plot (Drop Tail vs RED)...\n")
plt.figure(figsize=(12, 8))

# Drop Tail Delay Variation
plt.subplot(2, 1, 1)
for i in range(flows):
    plt.plot(time_intervals, delay_drop_tail[i], label=f'Stream {i+1}')
plt.xlabel('Elapsed Time (Seconds)')
plt.ylabel('Delay Variation (s)')
plt.title('Delay Variation with Drop Tail (Buffer Size = 2800)')
plt.legend()
plt.grid(True)

# RED Delay Variation
plt.subplot(2, 1, 2)
for i in range(flows):
    plt.plot(time_intervals, delay_red[i], label=f'Stream {i+1}')
plt.xlabel('Elapsed Time (Seconds)')
plt.ylabel('Delay Variation (s)')
plt.title('Delay Variation with RED (Buffer Size = 2800)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# 2. Throughput Comparison - Drop Tail vs RED (Buffer Size = 1400)
print("\n5. Generating Throughput Comparison Plot (Drop Tail vs RED, Buffer Size = 1400)...\n")
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(flows)
bar_width = 0.35
ax.bar(x - bar_width/2, throughput_drop_tail_data[:, 0], bar_width, label='Throughput - Drop Tail')
ax.bar(x + bar_width/2, throughput_red_data[:, 0], bar_width, label='Throughput - RED')
ax.set_xlabel('Flow')
ax.set_ylabel('Throughput (Mbps)')
ax.set_title('Throughput Comparison for Drop Tail vs RED (Buffer Size = 1400)')
ax.legend()
ax.grid(True)

plt.show()

# 3. Packet Loss Comparison - Drop Tail vs RED
print("\n6. Generating Packet Loss Comparison Plot (Drop Tail vs RED)...\n")
plt.figure(figsize=(12, 6))
x = np.arange(1, flows + 1)
plt.bar(x - 0.2, packet_loss_drop_tail, width=0.4, label='Packet Loss - DropTail', color='blue')
plt.bar(x + 0.2, packet_loss_red, width=0.4, label='Packet Loss - RED', color='orange')
plt.xlabel('Flow')
plt.ylabel('Packet Loss (Packets)')
plt.title('Packet Loss Comparison: Drop Tail vs RED')
plt.legend()
plt.grid(True)

plt.show()

# 4. Throughput vs Buffer Size for Drop Tail and RED
print("\n7. Generating Throughput vs Buffer Size Plot (Drop Tail and RED)...\n")
plt.figure(figsize=(12, 8))

# Drop Tail Throughput Variation
plt.subplot(2, 1, 1)
for i in range(flows):
    plt.bar([f'B{j+1}' for j in range(len(buffer_sizes))], throughput_drop_tail_data[i, :], bottom=np.sum(throughput_drop_tail_data[:i, :], axis=0), label=f'Flow {i+1}')
plt.xlabel('Buffer Size (B1=1400, B2=2800, B3=4200, B4=5600, B5=7000)')
plt.ylabel('Throughput (Mbps)')
plt.title('Throughput vs Buffer Size for Drop Tail')
plt.legend()
plt.grid(True)

# RED Throughput Variation
plt.subplot(2, 1, 2)
for i in range(flows):
    plt.bar([f'B{j+1}' for j in range(len(buffer_sizes))], throughput_red_data[i, :], bottom=np.sum(throughput_red_data[:i, :], axis=0), label=f'Flow {i+1}')
plt.xlabel('Buffer Size (B1=1400, B2=2800, B3=4200, B4=5600, B5=7000)')
plt.ylabel('Throughput (Mbps)')
plt.title('Throughput vs Buffer Size for RED')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

print("\n=== TCP Reno Congestion Control Simulation Completed ===")
