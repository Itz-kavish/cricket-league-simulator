import streamlit as st
import pandas as pd
import datetime  # 🔧 Import datetime module

st.title("🏏 BCMCL Points Table Simulator")

# === File Upload ===
st.subheader("📥 Upload Files")

points_file = st.file_uploader("Upload Points Table CSV", type=["csv"])
fixtures_file = st.file_uploader("Upload Fixtures Excel File", type=["xlsx"])

if points_file and fixtures_file:
    # === Load and Clean Points Table ===
    points_df = pd.read_csv(points_file)
    points_df.columns = points_df.columns.str.strip()
    points_df = points_df.rename(columns={"TEAM": "Team", "PTS": "Points", "MAT": "Played"})
    points_df = points_df[["Team", "Points", "Played"]]
    points_df.set_index("Team", inplace=True)

    # === Load Fixtures Excel ===
    try:
        fixtures_df = pd.read_excel(fixtures_file, skiprows=1)
        fixtures_df.columns = fixtures_df.columns.str.strip()
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        st.stop()

    # 🔧 Filter fixtures based on current date
    if "Date" not in fixtures_df.columns:
        st.error("❌ 'Date' column is missing in the fixtures file.")
        st.stop()

    fixtures_df["Date"] = pd.to_datetime(fixtures_df["Date"]).dt.date
    today = datetime.date.today()
    upcoming_fixtures_df = fixtures_df[fixtures_df["Date"] > today]

    if upcoming_fixtures_df.empty:
        st.success("✅ No upcoming fixtures after today.")
        st.stop()

    # 🔧 Extract fixtures after today
    if "Team One" in upcoming_fixtures_df.columns and "Team Two" in upcoming_fixtures_df.columns:
        fixtures = list(zip(upcoming_fixtures_df["Team One"], upcoming_fixtures_df["Team Two"]))
    else:
        st.error("❌ Could not find 'Team One' and 'Team Two' columns in the Excel file.")
        st.stop()

    # === Match Predictions ===
    st.subheader("✅ Predict Match Winners")

    results = {}

    # Zip team1, team2, and dates together
    for i, (team1, team2, match_date) in enumerate(zip(
            upcoming_fixtures_df["Team One"],
            upcoming_fixtures_df["Team Two"],
            upcoming_fixtures_df["Date"])):
        
        readable_date = match_date.strftime("%b %d, %Y")  # Example: Jul 31
        result = st.radio(
            f"Match {i+1}: {team1} vs {team2} ({readable_date})",
            options=[
                f"{team1} wins",
                f"{team2} wins",
                "No result",
                "Not played"
            ],
            index=3,
            key=f"match_{i}"
        )
        results[(team1, team2)] = result


    # === Update Table Based on Results ===
    updated_df = points_df.copy()

    for (team1, team2), result in results.items():
        if team1 not in updated_df.index or team2 not in updated_df.index:
            continue  # Skip if team names are inconsistent
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

    # === Final Table in Sidebar ===
    sorted_table = updated_df.sort_values(by=["Points", "Played"], ascending=[False, True])
    with st.sidebar:
        st.subheader("📊 Updated Points Table")
        st.dataframe(sorted_table.style.format({"Points": "{:.0f}", "Played": "{:.0f}"}), use_container_width=True)

        # Highlight relegation zone
        relegation_teams = sorted_table.tail(2).index.tolist()
        if relegation_teams:
            st.warning(f"🚨 Relegation Zone: {', '.join(relegation_teams)}")

# Show info message if files not uploaded
else:
    st.info("Please upload both files to begin.")

