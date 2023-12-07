import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = "C:\\Users\\Andi\\Desktop\\Bachelor\\etc\\a high quality rendering of a playmobil firefighter\\dreamfusion\\dreamfusion_playmobil_sds.csv"
data = pd.read_csv(file_path)

# Applying a moving average to the data
window_size = 50  # Window size for the moving average
data['Moving_Avg'] = data['Value'].rolling(window=window_size).mean()

# Calculating and printing mean values for every 500th interval
for i in range(0, 10000, 500):
    interval_data = data[(data['Step'] >= i) & (data['Step'] < i + 500)]
    mean_value = interval_data['Value'].mean()
    print(f"Mean value for interval {i} to {i + 499}: {mean_value}")

# Plotting the original values and moving average
plt.figure(figsize=(12, 6))
plt.plot(data['Step'], data['Value'], label='Original Values', color='orange')

plt.title('SDS Gradient, Moving Average, and Vertical Lines at Every 120th Step')
plt.xlabel('Step')
plt.ylabel('Value')
plt.yscale('log')  # Using logarithmic scale for better visualization
plt.legend()
plt.grid(True)
plt.show()
