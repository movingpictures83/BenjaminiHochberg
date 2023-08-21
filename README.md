# BenjaminiHochberg
# Language: Python
# Input: TXT
# Output: PREFIX 
# Tested with: PluMA 1.1, Python 3.6
# Dependency: scipy==1.4.1, pandas==1.1.15, statsmodels==0.12.1, numpy==1.19.1

PluMA plugin that takes a CSV file of correlations and p-values, and performs Benjamini-Hochberg correction on the p-values

The plugin takes as input a TXT file of keyword-value pairs:
diffCorr: Correlations CSV file
pval: P-value CSV file

Output correlations will be p-value thresholded.  Prefix is used for both quoted (TMP) and unquoted outputs.
