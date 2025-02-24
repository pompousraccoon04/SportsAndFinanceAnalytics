import requests
from bs4 import BeautifulSoup
import pandas as pd
import io
import matplotlib.pyplot as plt

# URL for 2024-25 advanced school stats (offensive only)
url = "https://www.sports-reference.com/cbb/seasons/men/2025-advanced-school-stats.html"

# Fetch the webpage
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find the stats table (using the correct ID from your observation)
table = soup.find("table", {"id": "adv_school_stats"})

# Initialize list to store all rows
all_rows = []

if table:
    # Get all rows (including headers and data)
    rows = table.find_all("tr")
    
    for row in rows:
        # Get row cells
        cells = row.find_all("td")  # Data cells
        headers = row.find_all("th")  # Header cells (for team names or repeating headers)
        
        # Check if this is a header row (repeating every 20 teams or so)
        if headers and len(headers) > 1 and ("School" in headers[0].get_text() or "Rk" in headers[0].get_text()):
            continue  # Skip header rows (e.g., "Rk", "School", etc., repeating)
        
        # If it's a data row, process it
        if cells and len(cells) > 0:  # Ensure it's not an empty row
            row_data = {}
            for cell in cells:
                stat = cell.get("data-stat", "")
                value = cell.get_text(strip=True)
                if stat:  # Only include cells with data-stat
                    row_data[stat] = value
            all_rows.append(row_data)

    # Define offensive stats we want (based on data-stat attributes, updated FTR to FT/FGA)
    offensive_stats = {
        "school_name": "School",  # Team name
        "efg_pct": "O eFG%",      # Offensive Effective Field Goal %
        "tov_pct": "O TO%",       # Offensive Turnover %
        "orb_pct": "O OR%",       # Offensive Rebound %
        "ft_rate": "O FT/FGA"        # Offensive Free Throws per Field Goal Attempt
    }
    
    # Filter rows and create DataFrame with only offensive stats
    df_list = []
    for row in all_rows:
        row_dict = {}
        for stat, col_name in offensive_stats.items():
            row_dict[col_name] = row.get(stat, "")  # Use empty string if stat not found
        if any(row_dict.values()):  # Only include non-empty rows
            df_list.append(row_dict)
    
    if df_list:
        df = pd.DataFrame(df_list)
        # Clean numeric columns (convert to float, handle % or other formats)
        for col in df.columns:
            if col != "School":
                df[col] = pd.to_numeric(df[col].str.replace("%", "").str.replace("+", ""), errors="coerce")
        
        # Save to CSV
        df.to_csv("cbb_2025_advanced_offensive_stats.csv", index=False)
        print("Offensive data saved to cbb_2025_advanced_offensive_stats.csv")
        
        # Preview the DataFrame
        print("Offensive Columns Found:", df.columns.tolist())
        print("\nFirst 5 rows of offensive stats:")
        print(df.head())

        # Analysis: Top 10 teams by offensive efficiency (O eFG%)
        top_efficiency = df[["School", "O eFG%"]].sort_values("O eFG%", ascending=False).head(10)

        # Analysis: Teams with lowest turnover % (O TO%) for efficiency
        top_low_turnover = df[["School", "O TO%"]].sort_values("O TO%", ascending=True).head(10)
        
        # Print insights
        print("\nTop 10 Teams by Offensive Efficiency (O eFG%):")
        print(top_efficiency)
        print("\nTop 10 Teams by Lowest Turnover % (O TO%):")
        print(top_low_turnover)

        # Offensive efficiency bar chart
        plt.subplot(1, 2, 1)
        plt.bar(top_efficiency["School"], top_efficiency["O eFG%"], color="blue")
        plt.title("Top 10 NCAA Teams by Offensive Efficiency (O eFG%, 2024-25)")
        plt.xlabel("Team")
        plt.ylabel("Offensive eFG%")
        plt.xticks(rotation=45, ha="right")

        # Lowest turnover % bar chart
        plt.subplot(1, 2, 2)
        plt.bar(top_low_turnover["School"], top_low_turnover["O TO%"], color="green")
        plt.title("Top 10 NCAA Teams by Lowest Turnover % (O TO%, 2024-25)")
        plt.xlabel("Team")
        plt.ylabel("Turnover %")
        plt.xticks(rotation=45, ha="right")

        plt.tight_layout()
        plt.savefig("cbb_offensive_efficiency_charts.png")
        plt.show()

    else:
        print("No data rows found—check table structure or data-stat attributes.")
else:
    print("Table not found—check the URL or page structure.")