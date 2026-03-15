# EU "Have Your Say" Platform: Stakeholder Participation Analysis

## Overview
This repository contains the data, scraping scripts, and analytical code used for the computational social science term paper: *"Do different stakeholder groups exhibit systematically different participation patterns across semantic policy topic clusters on the EU 'Have Your Say' platform?"*

The project utilizes Natural Language Processing (BERT embeddings and K-Means clustering) to categorize EU policy initiatives and employs Poisson regression models with robust standard errors to analyze participation heterogeneity among citizens, NGOs, and business associations.

## Repository Structure
* `data/`: Contains the raw and cleaned datasets.
  * `eu_policies_high_engagement.csv`: Initial consultation links (Credit: Marcus Novotny).
  * `updated_feedback_data_final.csv`: Full dataset with feedback counts and stakeholder percentages scraped by us.
* `scripts/`: Python scripts used for data collection and analysis.
  * `scrap_all_links.py`: Web scraping script to get feedback links.
  * `scrap_all_actors.py`: Web scraping script to collect feedback statistics.
  * `CSS_final_analysis_HaveYourSay_IlaydaDikmen.ipynb`: Jupyter notebook containing the BERT embedding and K-Means clustering of policy titles. Statistical analysis, including the Poisson count models, Wald tests, and data visualization.
#* `figures/`: Output graphs and tables used in the paper (e.g., topic distribution, stakeholder shares).

## Prerequisites
To run the code, you will need Python 3.8+ and the following libraries installed:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels transformers
