import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = "C:\\Users\\Andi\\Desktop\\Bachelor\\etc\\a high quality rendering of a playmobil firefighter\\dreamfusion\\dreamfusion_playmobil_sds.csv"
data = pd.read_csv(file_path)

# Filtering data for iteration steps between 6000 and 6480
filtered_data = data[(data['Step'] >= 6000) & (data['Step'] <= 6480)]

# Plotting the filtered data
plt.figure(figsize=(12, 6))
plt.plot(filtered_data['Step'], filtered_data['Value'], label='Value', color='blue')

# Labels for each segment
labels = ['F', 'L', 'B', 'R']

# Adding vertical lines and text labels
for i, step in enumerate(range(6000, 6480, 30)):
    plt.axvline(x=step, color='red', linestyle='--', alpha=0.5)
    label = labels[i % len(labels)]
    plt.text((step + 15), max(filtered_data['Value']), label, ha='center', va='bottom')

plt.title('SDS Gradient Between Iteration Steps 6000 and 6480 with Labels')
plt.xlabel('Step')
plt.ylabel('Value')
plt.grid(True)
plt.legend()
plt.show()
