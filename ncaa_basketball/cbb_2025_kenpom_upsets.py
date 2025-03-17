import kagglehub
import pandas as pd
import matplotlib.pyplot as plt
import os

# Download the Kaggle dataset (latest version)
dataset_path = kagglehub.dataset_download("jonathanpilafas/2024-march-madness-statistical-analysis")
print("Path to dataset files:", dataset_path)

# Define file path for DEV _ March Madness.csv
march_madness_file = "DEV _ March Madness.csv"
march_madness_path = os.path.join(dataset_path, march_madness_file)

# Check if file exists; if not, list available files
if not os.path.exists(march_madness_path):
    print(f"File {march_madness_file} not found in dataset. Available files:")
    available_files = os.listdir(dataset_path)
    print(available_files)
    for file in available_files:
        if file.lower() == march_madness_file.lower():
            march_madness_path = os.path.join(dataset_path, file)
            break
    else:
        raise FileNotFoundError(f"Could not find {march_madness_file} or a matching file in the dataset.")

# Load dataset
march_madness_df = pd.read_csv(march_madness_path)

# Filter for 2025 season and NCAAT
march_madness_df = march_madness_df[march_madness_df["Season"] == 2025]
march_madness_df = march_madness_df[march_madness_df["Post-Season Tournament"] == "March Madness"]

# Preview the data
print("First 5 records (March Madness 2025):", march_madness_df.head())

# Rename columns as needed
march_madness_df = march_madness_df.rename(columns={
    "Mapped ESPN Team Name": "School"
})

# Convert numeric columns to float
for col in ["RankAdjOE", "RankAdjDE", "RankAdjEM", "RankAdjTempo", "Seed"]:
    march_madness_df[col] = pd.to_numeric(march_madness_df[col], errors="coerce")

# Use march_madness_df directly (no merge needed)
merged_df = march_madness_df

# Validate merged data
print("Unique seeds in merged data:", merged_df["Seed"].unique())
print("Unique regions in merged data:", merged_df["Region"].unique())
print("Teams with missing seeds or regions:", merged_df[merged_df["Seed"].isna() | merged_df["Region"].isna()]["School"].tolist())

# Validate seed completeness per region
valid_regions = []
for region in merged_df["Region"].dropna().unique():
    region_df = merged_df[merged_df["Region"] == region].dropna(subset=["Seed"])
    unique_seeds = region_df["Seed"].dropna().unique()
    if len(unique_seeds) == 16 and set(unique_seeds) == set(range(1, 17)):
        valid_regions.append(region)
        print(f"{region} region has all seeds (1-16): {sorted(unique_seeds)}")
    else:
        print(f"WARNING: {region} region is missing seeds or has duplicates. Found seeds: {sorted(unique_seeds)}")

# Function to identify potential upsets for a single region
def identify_upsets(df, region):
    upsets = []
    # Filter for the specific region
    region_df = df[df["Region"] == region].dropna(subset=["Seed", "RankAdjOE", "RankAdjDE", "RankAdjEM"])

    # Debug: Print teams in this region
    print(f"\nTeams in {region} region:")
    print(region_df[["School", "Seed", "RankAdjOE", "RankAdjDE", "RankAdjEM"]])

    # For seeds not involved in play-ins, take the first team per seed
    region_df_single = region_df.sort_values("RankAdjOE").drop_duplicates(subset=["Seed"], keep="first")

    # 2 vs 15
    two = region_df_single[region_df_single["Seed"] == 2].iloc[0] if not region_df_single[region_df_single["Seed"] == 2].empty else None
    fifteen = region_df_single[region_df_single["Seed"] == 15].iloc[0] if not region_df_single[region_df_single["Seed"] == 15].empty else None
    if two is not None and fifteen is not None and (two.RankAdjOE > 50 or two.RankAdjDE > 50):
        criteria = f"2-seed RankAdjOE ({two.RankAdjOE}) or RankAdjDE ({two.RankAdjDE}) > 50"
        upsets.append((f"{two.School} (2) vs {fifteen.School} (15)", "2 vs 15", two.School, fifteen.School, criteria,
                       two.RankAdjOE, two.RankAdjDE, two.RankAdjEM, fifteen.RankAdjOE, fifteen.RankAdjDE, fifteen.RankAdjEM))

    # 3 vs 14
    three = region_df_single[region_df_single["Seed"] == 3].iloc[0] if not region_df_single[region_df_single["Seed"] == 3].empty else None
    fourteen = region_df_single[region_df_single["Seed"] == 14].iloc[0] if not region_df_single[region_df_single["Seed"] == 14].empty else None
    if three is not None and fourteen is not None and abs(fourteen.RankAdjOE - fourteen.RankAdjDE) <= 40:
        criteria = f"14-seed RankAdjOE ({fourteen.RankAdjOE}) - RankAdjDE ({fourteen.RankAdjDE}) ≤ 40"
        upsets.append((f"{three.School} (3) vs {fourteen.School} (14)", "3 vs 14", three.School, fourteen.School, criteria,
                       three.RankAdjOE, three.RankAdjDE, three.RankAdjEM, fourteen.RankAdjOE, fourteen.RankAdjDE, fourteen.RankAdjEM))

    # 4 vs 13
    four = region_df_single[region_df_single["Seed"] == 4].iloc[0] if not region_df_single[region_df_single["Seed"] == 4].empty else None
    thirteen = region_df_single[region_df_single["Seed"] == 13].iloc[0] if not region_df_single[region_df_single["Seed"] == 13].empty else None
    if four is not None and thirteen is not None and (four.RankAdjOE > 40 or four.RankAdjDE > 40) and (thirteen.RankAdjOE <= 50 or thirteen.RankAdjDE <= 50):
        criteria = f"4-seed RankAdjOE ({four.RankAdjOE}) or RankAdjDE ({four.RankAdjDE}) > 40 AND 13-seed RankAdjOE ({thirteen.RankAdjOE}) or RankAdjDE ({thirteen.RankAdjDE}) ≤ 50"
        upsets.append((f"{four.School} (4) vs {thirteen.School} (13)", "4 vs 13", four.School, thirteen.School, criteria,
                       four.RankAdjOE, four.RankAdjDE, four.RankAdjEM, thirteen.RankAdjOE, thirteen.RankAdjDE, thirteen.RankAdjEM))

    # 5 vs 12
    five = region_df_single[region_df_single["Seed"] == 5].iloc[0] if not region_df_single[region_df_single["Seed"] == 5].empty else None
    twelve = region_df_single[region_df_single["Seed"] == 12].iloc[0] if not region_df_single[region_df_single["Seed"] == 12].empty else None
    if five is not None and twelve is not None and ((five.RankAdjOE >= 60 or five.RankAdjDE >= 60) or (twelve.RankAdjEM <= 60 and five.RankAdjEM <= 20)):
        criteria = f"5-seed RankAdjOE ({five.RankAdjOE}) or RankAdjDE ({five.RankAdjDE}) ≥ 60 OR (12-seed RankAdjEM ({twelve.RankAdjEM}) ≤ 60 AND 5-seed RankAdjEM ({five.RankAdjEM}) ≤ 20)"
        upsets.append((f"{five.School} (5) vs {twelve.School} (12)", "5 vs 12", five.School, twelve.School, criteria,
                       five.RankAdjOE, five.RankAdjDE, five.RankAdjEM, twelve.RankAdjOE, twelve.RankAdjDE, twelve.RankAdjEM))

    # 6 vs 11 (handle multiple 11-seeds due to play-ins)
    six = region_df_single[region_df_single["Seed"] == 6].iloc[0] if not region_df_single[region_df_single["Seed"] == 6].empty else None
    elevens = region_df[region_df["Seed"] == 11].sort_values("RankAdjEM")
    if six is not None and not elevens.empty:
        for eleven in elevens.itertuples():
            if eleven.RankAdjEM < six.RankAdjEM or abs(eleven.RankAdjEM - six.RankAdjEM) <= 5:
                criteria = f"11-seed RankAdjEM ({eleven.RankAdjEM}) < 6-seed RankAdjEM ({six.RankAdjEM}) OR within 5 spots"
                upsets.append((f"{six.School} (6) vs {eleven.School} (11)", "6 vs 11", six.School, eleven.School, criteria,
                               six.RankAdjOE, six.RankAdjDE, six.RankAdjEM, eleven.RankAdjOE, eleven.RankAdjDE, eleven.RankAdjEM))

    # 7 vs 10
    seven = region_df_single[region_df_single["Seed"] == 7].iloc[0] if not region_df_single[region_df_single["Seed"] == 7].empty else None
    ten = region_df_single[region_df_single["Seed"] == 10].iloc[0] if not region_df_single[region_df_single["Seed"] == 10].empty else None
    if seven is not None and ten is not None and ten.RankAdjEM < seven.RankAdjEM:
        criteria = f"10-seed RankAdjEM ({ten.RankAdjEM}) < 7-seed RankAdjEM ({seven.RankAdjEM})"
        upsets.append((f"{seven.School} (7) vs {ten.School} (10)", "7 vs 10", seven.School, ten.School, criteria,
                       seven.RankAdjOE, seven.RankAdjDE, seven.RankAdjEM, ten.RankAdjOE, ten.RankAdjDE, ten.RankAdjEM))

    return pd.DataFrame(upsets, columns=["Matchup", "Upset_Type", "Higher_Seed", "Lower_Seed", "Criteria",
                                         "Higher_Seed_RankAdjOE", "Higher_Seed_RankAdjDE", "Higher_Seed_RankAdjEM",
                                         "Lower_Seed_RankAdjOE", "Lower_Seed_RankAdjDE", "Lower_Seed_RankAdjEM"])

# Identify potential upsets for each valid region
all_upsets = []
for region in valid_regions:
    print(f"\nProcessing region: {region}")
    region_upsets = identify_upsets(merged_df, region)
    all_upsets.append(region_upsets)

# Concatenate all upsets
upset_df = pd.concat(all_upsets, ignore_index=True)

# Print potential upsets
print("\nPotential Upsets in Round of 64 (2025 NCAA Tournament):")
if upset_df.empty:
    print("No potential upsets identified.")
else:
    print(upset_df)

# Visualize potential upsets with multiple metrics
if not upset_df.empty:
    plt.figure(figsize=(15, 8))
    bar_width = 0.2
    index = range(len(upset_df))

    # Plot multiple metrics for higher and lower seeds
    plt.bar([i - bar_width for i in index], upset_df["Higher_Seed_RankAdjOE"], bar_width, label="Higher Seed RankAdjOE", color="blue", alpha=0.7)
    plt.bar(index, upset_df["Higher_Seed_RankAdjDE"], bar_width, label="Higher Seed RankAdjDE", color="green", alpha=0.7)
    plt.bar([i + bar_width for i in index], upset_df["Higher_Seed_RankAdjEM"], bar_width, label="Higher Seed RankAdjEM", color="cyan", alpha=0.7)

    plt.bar([i - bar_width for i in index], upset_df["Lower_Seed_RankAdjOE"], bar_width, label="Lower Seed RankAdjOE", color="red", alpha=0.7, hatch='/')
    plt.bar(index, upset_df["Lower_Seed_RankAdjDE"], bar_width, label="Lower Seed RankAdjDE", color="orange", alpha=0.7, hatch='/')
    plt.bar([i + bar_width for i in index], upset_df["Lower_Seed_RankAdjEM"], bar_width, label="Lower Seed RankAdjEM", color="magenta", alpha=0.7, hatch='/')

    # Add criteria as annotations above each bar group
    for i, row in upset_df.iterrows():
        plt.text(i, max(row["Higher_Seed_RankAdjOE"], row["Higher_Seed_RankAdjDE"], row["Higher_Seed_RankAdjEM"],
                        row["Lower_Seed_RankAdjOE"], row["Lower_Seed_RankAdjDE"], row["Lower_Seed_RankAdjEM"]) + 5,
                 row["Criteria"], ha="center", va="bottom", rotation=90, fontsize=8, wrap=True)

    plt.xlabel("Matchups")
    plt.ylabel("Rankings (Lower is Better)")
    plt.title("Potential Upsets in 2025 NCAA Tournament Round of 64")
    plt.xticks(index, upset_df["Matchup"], rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig("cbb_kenpom_potential_upsets.png")
    plt.show()
else:
    print("No potential upsets to visualize.")

# Save potential upsets to CSV with criteria and metrics
if not upset_df.empty:
    upset_df.to_csv("cbb_2025_kenpom_potential_upsets.csv", index=False)
    print("Potential upsets data saved to cbb_2025_kenpom_potential_upsets.csv")
else:
    print("No potential upsets to save.")