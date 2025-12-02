import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Directory containing CSV files
data_dir = "simulation_results"

# Names of the simulation variables
sim_vars = ["Bn", "Un", "Cn", "Dn", "Dn_minus_Cn"]

# Dictionary to hold dataframes
data = {}

# Load CSV files
for var in sim_vars:
    file_path = os.path.join(data_dir, f"{var}.csv")
    if not os.path.exists(file_path):
        print(f"File {file_path} not found!")
        continue
    df = pd.read_csv(file_path)
    data[var] = df

# Plot individual repetitions and mean for each simulation
for var, df in data.items():
    n_values = df['n'].values
    repetitions = df.drop(columns='n').values  # shape = (len(n_values), k)
    mean_values = repetitions.mean(axis=1)

    plt.figure(figsize=(10,6))
    # Individual repetitions (semi-transparent)
    for k in range(repetitions.shape[1]):
        plt.plot(n_values, repetitions[:, k], color='blue', alpha=0.3)
    # Mean
    plt.plot(n_values, mean_values, color='red', linewidth=2, label='Mean')
    plt.xlabel("n")
    plt.ylabel(var)
    plt.title(f"{var} vs n (individual runs and mean)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(data_dir, f"{var}_plot.png"))
    plt.show()

# Now compute requested ratios / normalizations

def compute_and_plot_ratio(var_name, mean_values, n_values, ratios_dict):
    plt.figure(figsize=(10,6))
    for label, ratio in ratios_dict.items():
        plt.plot(n_values, ratio, label=label)
    plt.xlabel("n")
    plt.ylabel(f"{var_name} ratios")
    plt.title(f"{var_name} normalized ratios vs n")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(data_dir, f"{var_name}_ratios.png"))
    plt.show()

# (a) Bn ratios
Bn_mean = data["Bn"].drop(columns='n').mean(axis=1).values
compute_and_plot_ratio(
    "Bn",
    Bn_mean,
    n_values,
    {
        "Bn/n": Bn_mean / n_values,
        "Bn/sqrt(n)": Bn_mean / np.sqrt(n_values)
    }
)

# (b) Un ratios
Un_mean = data["Un"].drop(columns='n').mean(axis=1).values
compute_and_plot_ratio(
    "Un",
    Un_mean,
    n_values,
    {
        "Un/n": Un_mean / n_values
    }
)

# (c) Cn ratios
Cn_mean = data["Cn"].drop(columns='n').mean(axis=1).values
compute_and_plot_ratio(
    "Cn",
    Cn_mean,
    n_values,
    {
        "Cn/n": Cn_mean / n_values,
        "Cn/(n*ln n)": Cn_mean / (n_values * np.log(n_values)),
        "Cn/n^2": Cn_mean / (n_values**2)
    }
)

# (d) Dn ratios
Dn_mean = data["Dn"].drop(columns='n').mean(axis=1).values
compute_and_plot_ratio(
    "Dn",
    Dn_mean,
    n_values,
    {
        "Dn/n": Dn_mean / n_values,
        "Dn/(n*ln n)": Dn_mean / (n_values * np.log(n_values)),
        "Dn/n^2": Dn_mean / (n_values**2)
    }
)

# (e) Dn-Cn ratios
DnCn_mean = data["Dn_minus_Cn"].drop(columns='n').mean(axis=1).values
compute_and_plot_ratio(
    "Dn_minus_Cn",
    DnCn_mean,
    n_values,
    {
        "(Dn-Cn)/n": DnCn_mean / n_values,
        "(Dn-Cn)/(n*ln n)": DnCn_mean / (n_values * np.log(n_values)),
        "(Dn-Cn)/(n*ln ln n)": DnCn_mean / (n_values * np.log(np.log(n_values)))
    }
)

print("All plots generated in:", data_dir)

