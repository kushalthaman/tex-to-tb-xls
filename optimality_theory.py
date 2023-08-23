import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Load the data from the Excel file
df = pd.read_excel('data.xlsx', engine='openpyxl')

# Sort by Token Frequency in descending order and create ranks
df = df.sort_values(by='Token Frequency', ascending=False)
df['Rank'] = range(1, len(df) + 1)

# Log transform for linear regression
log_ranks = np.log(df['Rank'])
log_frequencies = np.log(df['Token Frequency'])

# 1. Linear Regression
X_lin = sm.add_constant(log_ranks) # adding a constant (intercept)
model_lin = sm.OLS(log_frequencies, X_lin).fit()
print(model_lin.summary())

# Plotting linear regression
plt.figure(figsize=(10, 6))
plt.scatter(log_ranks, log_frequencies, color='blue', label="Data")
plt.plot(log_ranks, model_lin.predict(X_lin), color='red', label="Linear Regression")
plt.title('Linear Regression')
plt.xlabel('Log Rank')
plt.ylabel('Log Token Frequency')
plt.legend()
plt.grid(True)
plt.show()

# 2. Binomial Regression
# Note: This might not be appropriate as binomial regression assumes a binary outcome.
# We're using it here purely for demonstration purposes.
model_binom = sm.GLM(df['Token Frequency'], sm.add_constant(df['Rank']), family=sm.families.Binomial()).fit()
print(model_binom.summary())

# 3. Poisson Regression
model_poisson = sm.GLM(df['Token Frequency'], sm.add_constant(df['Rank']), family=sm.families.Poisson()).fit()
print(model_poisson.summary())
