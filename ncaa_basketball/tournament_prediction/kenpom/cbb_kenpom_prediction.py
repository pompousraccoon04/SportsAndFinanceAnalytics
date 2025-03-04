import kagglehub
import pandas as pd
import matplotlib.pyplot as plt
import os

# Download the Kaggle dataset (latest version)
dataset_path = kagglehub.dataset_download("jonathanpilafas/2024-march-madness-statistical-analysis")
print("Path to dataset files:", dataset_path)

# Define the expected file name (with spaces)
expected_file = "INT _ KenPom _ Summary.csv"
file_path = os.path.join(dataset_path, expected_file)

# Check if the file exists; if not, list available files
if not os.path.exists(file_path):
    print(f"File {expected_file} not found in dataset. Available files:")
    available_files = os.listdir(dataset_path)
    print(available_files)
    # Try a case-insensitive match or common variations
    for file in available_files:
        if file.lower() == expected_file.lower():
            file_path = os.path.join(dataset_path, file)
            break
    else:
        raise FileNotFoundError(f"Could not find {expected_file} or a matching file in the dataset.")

# Read the dataset into a pandas DataFrame
df = pd.read_csv(file_path)

# Filter for the 2025 season
df = df[df["Season"] == 2025]

# Preview the data
print("First 5 records (2025 season):", df.head())

# Ensure column names match expected KenPom metrics (adjust if needed)
# Confirmed columns: TeamName, Season, AdjOE, RankAdjOE, AdjDE, RankAdjDE, AdjTempo
df = df.rename(columns={
    "TeamName": "School",
    "AdjTempo": "AdjT"
})

# Convert numeric columns to float
for col in ["AdjOE", "RankAdjOE", "AdjDE", "RankAdjDE", "AdjT"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Simplified criteria: Teams must be in top 21 for AdjOE and top 31 for AdjDE (based on ranks)
# Lower rank means better performance (e.g., RankAdjOE = 1 is best offense)
eligible_teams = df[
    (df["RankAdjOE"] <= 21) &  # Top 21 in Adjusted Offense
    (df["RankAdjDE"] <= 31)    # Top 31 in Adjusted Defense
]

# Sort eligible teams by RankAdjOE for better visualization
eligible_teams = eligible_teams.sort_values("RankAdjOE")

# Print eligible teams (excluding Conference and SOS)
print("Teams Eligible to Win 2025 NCAA Tournament (Top 21 AdjOE, Top 31 AdjDE):")
if eligible_teams.empty:
    print("No teams meet the eligibility criteria.")
else:
    print(eligible_teams[["School", "AdjOE", "RankAdjOE", "AdjDE", "RankAdjDE"]])

# Visualize eligible teams with a bar chart comparing AdjOE and AdjDE
if not eligible_teams.empty:
    plt.figure(figsize=(12, 6))

    # Plot AdjOE and AdjDE as bars for each eligible team
    bar_width = 0.35
    index = range(len(eligible_teams))

    plt.bar(index, eligible_teams["AdjOE"], bar_width, label="Adjusted Offense (AdjOE)", color="blue")
    plt.bar([i + bar_width for i in index], eligible_teams["AdjDE"], bar_width, label="Adjusted Defense (AdjDE)", color="red")

    plt.xlabel("Teams")
    plt.ylabel("KenPom Metrics")
    plt.title("Eligible Teams for 2025 NCAA Tournament (Top 21 AdjOE, Top 31 AdjDE)")
    plt.xticks([i + bar_width / 2 for i in index], eligible_teams["School"], rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()

    plt.savefig("cbb_kenpom_eligible_teams.png")
    plt.show()
else:
    print("No eligible teams to visualize.")

# Save eligible teams to CSV for reference (excluding Conference and SOS)
if not eligible_teams.empty:
    eligible_teams[["School", "AdjOE", "RankAdjOE", "AdjDE", "RankAdjDE"]].to_csv("cbb_2025_kenpom_eligible_teams.csv", index=False)
    print("Eligible teams data saved to cbb_2025_kenpom_eligible_teams.csv")
else:
    print("No eligible teams to save.")