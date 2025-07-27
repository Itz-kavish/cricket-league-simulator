import streamlit as st

import pandas as pd
# Editable starting table
team_data = {
    "Team": ["United", "Cosmos", "Windies", "WestVan", "Abbotsford", "StarsVI", "Lions", "HawksIV", "StarsV", "NorthVan"
],
    "Points": [46,46,38,34,32,20,20,18,12,10],
    "Played": [15,15,14,13,13,14,14,14,14,12]
}

df = pd.DataFrame(team_data)
df.set_index("Team", inplace=True)

# === Fixtures ===
fixtures = [
("HawksIV", "NorthVan"),
("WestVan", "Abbotsford"),
("Abbotsford", "HawksIV"),
("Lions", "StarsVI"),
("NorthVan", "StarsV"),
("Windies", "WestVan"),
("Cosmos", "United"),
("WestVan", "Cosmos"),
("United", "Lions"),
("StarsV", "HawksIV"),
("StarsVI", "NorthVan"),
("Windies", "Abbotsford"),
("HawksIV", "StarsVI"),
("Abbotsford", "StarsV"),
("Cosmos", "Windies"),
("Lions", "WestVan"),
("NorthVan", "United"),
("Lions", "NorthVan"),
("WestVan", "StarsVI"),
("Abbotsford", "NorthVan"),
("Windies", "StarsV"),]


st.title("🏏 Cricket League Relegation Simulator")

st.subheader("✅ Predict Match Winners")

results = {}

for i, (team1, team2) in enumerate(fixtures):
    result = st.radio(
        f"Match {i+1}: {team1} vs {team2}",
        options=[
            f"{team1} wins",
            f"{team2} wins",
            "No result",
            "Not played"
        ],
        key=f"match_{i}"
    )
    results[(team1, team2)] = result

# === Update Table Based on Results ===

updated_df = df.copy()

for (team1, team2), result in results.items():
    if result == f"{team1} wins":
        updated_df.loc[team1, "Points"] += 4
        updated_df.loc[team1, "Played"] += 1
        updated_df.loc[team2, "Played"] += 1
    elif result == f"{team2} wins":
        updated_df.loc[team2, "Points"] += 4
        updated_df.loc[team2, "Played"] += 1
        updated_df.loc[team1, "Played"] += 1
    elif result == "No result":
        updated_df.loc[team1, "Points"] += 2
        updated_df.loc[team2, "Points"] += 1
        updated_df.loc[team1, "Played"] += 1
        updated_df.loc[team2, "Played"] += 1
    # "Not played" does nothing

# === Show Updated Table ===

st.subheader("📊 Updated Points Table")

sorted_table = updated_df.sort_values(by=["Points", "Played"], ascending=[False, True])
st.dataframe(sorted_table.style.format({"Points": "{:.0f}", "Played": "{:.0f}"}))

# Highlight relegation zone
relegation_teams = sorted_table.tail(2).index.tolist()
if relegation_teams:
    st.warning(f"🚨 Current Relegation Zone: {', '.join(relegation_teams)}")
