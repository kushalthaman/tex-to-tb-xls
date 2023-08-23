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

log_ranks = np.log(df['Rank'])
log_token_frequencies = np.log(df['Token Frequency'])

log_freq = np.log(df['Token Frequency'])
log_rank = np.log(df['Rank'])
slope, intercept, r_value, p_value, std_err = linregress(log_rank, log_freq)
best_fit = slope * log_rank + intercept
plt.figure(figsize=(10,6))
plt.loglog(df['Rank'], df['Token Frequency'], 'o', label='Data')
plt.loglog(df['Rank'], np.exp(best_fit), 'r', label=f'Best Fit: y = {np.exp(intercept):.3f} * x^{slope:.3f}')
plt.loglog(df['Rank'], np.exp(intercept) * df['Rank']**-1, 'g', label="Zipf's law: y = k * x^-1")
plt.xlabel('Rank')
plt.ylabel('Token Frequency')
plt.title('Log-Log Plot of Token Frequency vs Rank')
plt.legend()
plt.grid(True, which="both", ls="--", linewidth=0.5)
plt.show()

#Binomial Regression
model_binom = sm.GLM(df['Token Frequency'], sm.add_constant(df['Rank']), family=sm.families.Binomial()).fit()
print(model_binom.summary())

#Poisson Regression
model_poisson = sm.GLM(df['Token Frequency'], sm.add_constant(df['Rank']), family=sm.families.Poisson()).fit()
print(model_poisson.summary())

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
poisson_model = smf.glm(formula, data = df, family=sm.families.Poisson()).fit()
nb_model = smf.glm(formula, data=df, family=sm.families.NegativeBinomial(alpha=0.6762968626)).fit()
lr_stat = -2*(poisson_model.llf - nb_model.llf)
p_value = chi2.sf(lr_stat, df=1)
print(f"Likelihood Ratio Statistic: {lr_stat}")
print(f"P-Value: {p_value}")

