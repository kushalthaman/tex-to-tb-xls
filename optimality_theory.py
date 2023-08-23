# Plot of text frequencies of syllables with simple v/s complex margins

# Onsets and codas in syllables with simple margins (plotted with log frequency)



# Linear, binomial and poisson regression 

# Likelihood ratio testing

# Correlation with zipfian distribution
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the Excel file
df = pd.read_excel('FinnishTemplateTable1.xlsx', engine='openpyxl')

# Sort by Type Frequency in descending order
df = df.sort_values(by='Type Frequency', ascending=False)

# Create ranks
df['Rank'] = range(1, len(df) + 1)

# Log transform
log_ranks = np.log(df['Rank'])
log_frequencies = np.log(df['Type Frequency'])

# Linear regression
slope, intercept = np.polyfit(log_ranks, log_frequencies, 1)

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(log_ranks, log_frequencies, color='blue', label="Data")
plt.plot(log_ranks, slope * log_ranks + intercept, color='red', label=f"Fit: y = {slope:.2f}x + {intercept:.2f}")
plt.title('Zipff Law Check')
plt.xlabel('Log Rank')
plt.ylabel('Log Frequency')
plt.legend()
plt.grid(True)
plt.show()

print(f"Slope of the fit: {slope:.4f}")

if -1.1 < slope < -0.9:
    print("The data follows Zipf's law.")
else:
    print("The data does not follow Zipf's law closely.")
