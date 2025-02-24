import pandas as pd
import matplotlib.pyplot as plt

# Load existing offensive stats
df = pd.read_csv("cbb_2025_advanced_offensive_stats.csv")

# Clean and ensure numeric (already confirmed correct, but double-check)
for col in ["O eFG%", "O TO%", "O OR%", "O FT/FGA"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Manually add seed projections (simplified based on Feb 2025 bracketology)
seed_data = {
    "School": ["Auburn", "Duke", "Alabama", "Florida", "Tennessee", "Houston", "Texas A&M", "Iowa State", 
               "Michigan", "Wisconsin", "St. John’s", "Michigan State", "Purdue", "Texas Tech", "Arizona", "Missouri"],
    "Seed": [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4]
}
seeds_df = pd.DataFrame(seed_data)

# Merge offensive stats with seed data
merged_df = pd.merge(df, seeds_df, on="School", how="left")

# Create a prediction score based on offensive stats and seed
# Higher O eFG%, O OR%, O FT/FGA = better; Lower O TO% = better
merged_df["Prediction_Score"] = (
    merged_df["O eFG%"] * 0.4 +  # Weight offensive efficiency heavily
    merged_df["O OR%"] * 0.3 +   # Rebounding boosts tournament success
    merged_df["O FT/FGA"] * 0.2 + # Free throws matter in close games
    (100 - merged_df["O TO%"]) * 0.1  # Lower turnover % is better, scaled to 100
) / merged_df["Seed"]  # Lower seeds (better rank) boost score

# Sort by prediction score to rank tournament potential
ranked_df = merged_df[["School", "Seed", "Prediction_Score", "O eFG%", "O TO%", "O OR%", "O FT/FGA"]]\
    .sort_values("Prediction_Score", ascending=False).head(16)  # Top 16 for tournament

# Print insights
print("Top 16 NCAA Teams Predicted for 2025 Tournament Success (Based on Stats and Seeds):")
print(ranked_df)

# Visualize top 10 teams by prediction score
top_10 = ranked_df.head(10)
plt.figure(figsize=(12, 6))
plt.bar(top_10["School"], top_10["Prediction_Score"], color="purple")
plt.title("Top 10 NCAA Teams Predicted for 2025 Tournament Success")
plt.xlabel("Team")
plt.ylabel("Prediction Score (Higher = Better)")
plt.xticks(rotation=45, ha="right")
plt.savefig("cbb_tournament_prediction.png")
plt.show()