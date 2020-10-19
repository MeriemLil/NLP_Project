import pandas as pd
# the SentiStrength tool calculates the positive and negative scores of a sentence
# we feed to it the combined database train-test-val as txt file 'concatenated_data.txt' and it returns the results as txt file 'concatenated_data+results.txt'

sentiStrength = pd.read_csv('sentistrength\concatenated_data+results.txt', sep= '\t')

# We add a column for summing the negative and positive scores
sentiStrength['Sum'] = ''
for i in range(len(sentiStrength)):
    sentiStrength['Sum'][i] = sentiStrength['Positive'][i] + sentiStrength['Negative'][i]

# we save the results
sentiStrength.to_csv('sentistrength\sentistrength_results.csv')

# The sentiment score can be used as a rough indicator to distinguish between the positive sentiments (love, joy, surprise) and the negative sentiments (anger, sadness, fear)
# In general, for positive sentiments we get an overall score that is positive, and for the negative ones the overall score is negative
# sometimes an ambiguity rises when score is 0, indicating neither positive nor negative but neutral
# Thus, discriminating the various emotion states is not possible, because this classification only tells us about barely the positive and negative sentiments and it does not
# separate between states that belong to positive or those who belong to negative.
# Also because sometimes a positive or a negative sentiment is reported as neutral



