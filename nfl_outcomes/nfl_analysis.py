import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and clean dataset
df = pd.read_csv("spreadspoke_scores.csv")
df = df[df["schedule_season"] >= 2018]
df.dropna(subset=["score_home", "score_away"], inplace=True)
df["winner"] = df.apply(lambda row: row["team_home"] if row["score_home"] > row["score_away"] else row["team_away"], axis=1)

# Home-field advantage
home_wins = df[df["score_home"] > df["score_away"]].shape[0]
total_games = df.shape[0]
home_win_pct = (home_wins / total_games) * 100
print(f"Games Analyzed (2018+): {total_games}")
print(f"Home Win Percentage (2018+): {home_win_pct:.2f}%")

# Top teams
team_wins = df["winner"].value_counts().head(10)
print("\nTop 10 Teams by Wins (2018+):")
print(team_wins)

# Visualize home vs. away
outcomes = {"Home Wins": home_wins, "Away Wins": total_games - home_wins}
plt.bar(outcomes.keys(), outcomes.values(), color=["blue", "orange"])
plt.title("Home vs. Away Wins (NFL 2018+)")
plt.ylabel("Number of Games")
plt.savefig("home_away_wins.png")
plt.show()

# Visualize top teams
plt.figure(figsize=(10, 6))
sns.barplot(x=team_wins.values, y=team_wins.index, palette="viridis")
plt.title("Top 10 NFL Teams by Wins (2018+)")
plt.xlabel("Wins")
plt.savefig("top_teams.png")
plt.show()