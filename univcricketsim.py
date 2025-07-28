import streamlit as st
import pandas as pd

st.title("🏏 Cricket League Relegation Simulator")

st.subheader("📥 Upload Files")

points_file = st.file_uploader("Upload Points Table CSV", type=["csv"])
fixtures_file = st.file_uploader("Upload Fixtures CSV", type=["csv"])

if points_file and fixtures_file:
    # Load CSVs
    df = pd.read_csv(points_file)
    df.set_index("Team", inplace=True)

    fixtures_df = pd.read_csv(fixtures_file)
    fixtures = list(zip(fixtures_df["Team1"], fixtures_df["Team2"]))

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

else:
    st.info("Please upload both the Points Table and Fixtures CSV files.")