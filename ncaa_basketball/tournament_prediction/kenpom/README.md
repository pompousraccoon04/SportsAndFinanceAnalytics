# NCAA 2025 Tournament Prediction with KenPom Data (Kaggle)
Predicted NCAA men’s basketball teams eligible to win the 2025 March Madness tournament using 2025 KenPom advanced metrics (Adjusted Offense and Defense) from Kaggle dataset.

## Tools
- Python, kagglehub, pandas, matplotlib

## Eligibility Criteria
- Top 21 in Adjusted Offense (AdjOE rank ≤ 21)
- Top 31 in Adjusted Defense (AdjDE rank ≤ 31)
- Season: 2025

## Findings
- Eligible teams: Auburn, Duke, Florida, Houston, Texas Tech, Wisconsin, Clemson, Arizona, Iowa St.
- Top 3 by AdjOE Rank:
  - Auburn (AdjOE: 130.745, Rank: 1; AdjDE: 93.1002, Rank: 10)
  - Duke (AdjOE: 128.900, Rank: 2; AdjDE: 89.8200, Rank: 4)
  - Florida (AdjOE: 126.918, Rank: 4; AdjDE: 92.9738, Rank: 7)
- See chart for full list and metrics

## Files
- `cbb_kenpom_prediction.py`: Prediction script
- `cbb_kenpom_eligible_teams.png`: Bar chart of eligible teams
- `cbb_2025_kenpom_eligible_teams.csv`: Eligible teams data (2025)