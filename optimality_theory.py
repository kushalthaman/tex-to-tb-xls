import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

df = pd.read_excel('FinnishSyllabary1.xlsx', engine='openpyxl')

df = df.sort_values(by='Token Frequency', ascending=False)
df['Rank'] = range(1, len(df) + 1)

log_ranks = np.log(df['Rank'])
log_token_frequencies = np.log(df['Token Frequency'])

#Linear Regression
X_lin = sm.add_constant(log_ranks)   
model_lin = sm.OLS(log_token_frequencies, X_lin).fit()
print(model_lin.summary())
plt.figure(figsize=(10, 6))
plt.scatter(log_ranks, log_token_frequencies, color='blue', label="Data")
plt.plot(log_ranks, model_lin.predict(X_lin), color='red', label="Linear Regression")
plt.title('Linear Regression on Token Frequency')
plt.xlabel('Log Rank')
plt.ylabel('Log Token Frequency')
plt.legend()
plt.grid(True)
plt.show()

#Binomial Regression
model_binom = sm.GLM(df['Token Frequency'], sm.add_constant(df['Rank']), family=sm.families.Binomial()).fit()
print(model_binom.summary())

#Poisson Regression
model_poisson = sm.GLM(df['Token Frequency'], sm.add_constant(df['Rank']), family=sm.families.Poisson()).fit()
print(model_poisson.summary())
 
