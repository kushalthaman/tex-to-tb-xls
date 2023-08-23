import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import chi2
from scipy.stats import spearmanr
from scipy.stats import linregress

df = pd.read_excel('FinnishSyllabary1.xlsx', engine='openpyxl')

df = df.sort_values(by='Token Frequency', ascending=False)
df['Rank'] = range(1, len(df) + 1)
df = df[df['Token Frequency'] > 0]
log_ranks = np.log(df['Rank'])
log_token_frequencies = np.log(df['Token Frequency'])

##Linear Regression
X_lin = sm.add_constant(log_ranks)   
model_lin = sm.OLS(log_token_frequencies, X_lin).fit()
slope = model_lin.params[1]
intercept = log_token_frequencies.iloc[0] - slope * log_ranks.iloc[0]
equation_str = f"y = {intercept:.3f} + {slope:.3f}x"

plt.figure(figsize=(10, 6))
plt.scatter(log_ranks, log_token_frequencies, color='blue', label="Data")
plt.plot(log_ranks, model_lin.predict(X_lin), color='red', label=f"Linear Regression: {equation_str}")
plt.plot(log_ranks, intercept - log_ranks, color='green', linestyle='--', label="Zipf's Law: y = K/x")
plt.title('Linear Regression on Token Frequency for Finnish')
plt.xlabel('Log Rank')
plt.ylabel('Log Token Frequency')
plt.legend()
plt.grid(True)
plt.show()

print(model_lin.summary())

#Poisson Regression
model_poisson = sm.GLM(df['Token Frequency'], sm.add_constant(df['Rank']), family=sm.families.Poisson()).fit()
print(model_poisson.summary())

#Negbinom Regression
model_nb = sm.GLM(df['Token Frequency'], sm.add_constant(df['Rank']), family=sm.families.NegativeBinomial()).fit()
print(model_nb.summary())

#Correlation 
df_sorted = df.sort_values(by="Token Frequency", ascending=False)
ranks = np.arange(1, len(df_sorted) + 1)
plt.figure(figsize=(10, 6))
plt.scatter(ranks, df_sorted['Token Frequency'], color='green')

k = df['Token Frequency'].iloc[0]  # Take the frequency of the most frequent word as k
df['Zipf Frequency'] = k / df['Rank']
plt.plot(df['Rank'], df['Zipf Frequency'], 'r--', label="Zipf's Law")


# spearman correlation between zipf and actual values
frequency = df_sorted['Token Frequency'].values
rank = df_sorted.index + 1
df_sorted['Zipf Frequency'] = frequency[0] / rank
non_zero_mask = frequency > 0
rank_non_zero = rank[non_zero_mask]
frequency_non_zero = frequency[non_zero_mask]
zipf_frequency_non_zero = df_sorted['Zipf Frequency'][non_zero_mask].values
correlation, _ = spearmanr(frequency_non_zero, zipf_frequency_non_zero)

print(f"Spearman correlation: {correlation:.4f}")

plt.title("Zipfs Law correlation")
plt.xlabel('Rank')
plt.ylabel('Token Frequency')
plt.xscale('log')
plt.yscale('log')
plt.grid(True, which="both", ls="--", c='0.65')
plt.show()

#compare poisson v/s negbinom

formula = "Q('Token Frequency') ~ Onset + Coda + Q('Complex Onset') + Q('Complex Coda') + Template"
lr_stat = -2*(model_poisson.llf - model_nb.llf)
p_value = chi2.sf(lr_stat, df=1)
print(f"Likelihood Ratio Statistic: {lr_stat}")
print(f"P-Value: {p_value}")

