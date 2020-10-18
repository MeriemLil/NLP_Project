import pandas as pd
# the SentiStrength tool calculates the positive and negative scores of a sentence
# we feed to it the combined database train-test-val as txt file and it returns the results as txt file
# for readability we read the results as excel file
sentiStrength = pd.read_excel('sentistrength\sentistrength_results_excel.xlsx')

# then we convert to csv for manipulation
sentiStrength.to_csv("sentistrength\sentistrength_results_csv.csv", header=True)
sentiStrength_results = pd.read_csv('sentistrength\sentistrength_results_csv.csv')

# We add a column for summing the negative and positive scores
sentiStrength_results['Sum'] = ''
for i in range(len(sentiStrength_results)):
    sentiStrength_results['Sum'][i] = sentiStrength_results['Positive'][i] + sentiStrength_results['Negative'][i]

# we save in the same file
sentiStrength_results.to_csv('sentistrength\sentistrength_results_csv.csv')

# The sentiment score can be used an indicator to distinguish between the positive sentiments (love, joy, surprise) and the negative sentiments (anger, sadness, fear)
# For positive sentiments we get an overall score that is positive, and for the negative ones the overall score is negative
# Thus, discriminating the various emotion states is not possible, as this classification only tells us about the positive and negative sentiments and it does not separate
# between states that belong to positive or those who belong to negative.




