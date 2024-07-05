import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
file_path = 'results/compare_searches_8_puzzle.csv'
data = pd.read_csv(file_path)

# Extract unique algorithms
algorithms = data['object'].unique()

# Create subplots
fig, axs = plt.subplots(1, 2, figsize=(10, 12))

# Plot time
for algo in algorithms:
    algo_data = data[data['object'] == algo]
    axs[0].plot(algo_data['graph_problem'], algo_data['time'], label=algo)

axs[0].set_xlabel('Graph Problem (Number of Nodes)')
axs[0].set_ylabel('Time')
axs[0].set_title('Time vs Graph Problem Size')
axs[0].legend()

# Plot nodes expanded
for algo in algorithms:
    algo_data = data[data['object'] == algo]
    axs[1].plot(algo_data['graph_problem'], algo_data['nodes expanded'], label=algo)

axs[1].set_xlabel('Graph Problem (Number of Nodes)')
axs[1].set_ylabel('Nodes Expanded')
axs[1].set_title('Nodes Expanded vs Graph Problem Size')
axs[1].legend()

# Show plots
plt.tight_layout()
plt.show()
