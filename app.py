import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Football Performance Dashboard", layout="wide")

# Function to fetch data from the SQLite database
def get_data(query):
    conn = sqlite3.connect('football_data.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# SIDEBAR FILTERS
st.sidebar.header("Global Filters")

# Period selection (Pre/Post Pandemic)
period_filter = st.sidebar.selectbox("Select Period", ["All", "Pre-Pandemic", "Post-Pandemic"])

# Tier selection (League levels)
tier_filter = st.sidebar.multiselect("Select Tiers", ["Elite", "Competitive", "Cup/Lower"], default=["Elite", "Competitive"])

min_mins = st.sidebar.slider("Minimum Minutes Played Threshold", min_value=0, max_value=3000, value=500, step=100)

# Building the dynamic SQL query based on sidebar inputs
where_clauses = []
if period_filter != "All":
    where_clauses.append(f"period = '{period_filter}'")
if tier_filter:
    tiers_str = "', '".join(tier_filter)
    where_clauses.append(f"tier IN ('{tiers_str}')")

# Applying the minimum minutes filter directly in SQL for performance
where_clauses.append(f"minutes_played >= {min_mins}")

where_stmt = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
main_query = f"SELECT * FROM player_performances {where_stmt}"

# Load filtered data
df = get_data(main_query)

# Define KPI dictionary for dynamic selection in plots
kpi_options = {
    "Total Contribution (G+A)": "total_contribution",
    "Efficiency (Score per Min)": "efficiency",
    "Discipline Score (Card Impact)": "discipline_score",
    "Continuity (Total Minutes)": "minutes_played"
}

st.title("⚽ Football Player Performance Analysis")
st.markdown(f"Currently filtering players with at least **{min_mins} minutes** played.")

# KPI CARDS
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Players", len(df['player_name'].unique()))
with col2:
    st.metric("Total Goals", int(df['goals'].sum()))
with col3:
    st.metric("Avg Efficiency", f"{df['efficiency'].mean():.4f}")
with col4:
    st.metric("Avg Discipline", f"{df['discipline_score'].mean():.2f}")

st.divider()

# INTERACTIVE CHARTS
tab1, tab2, tab3 = st.tabs(["📊 Performance Distributions", "🏆 Top Rankings", "🔍 Player Deep-Dive"])

with tab1:
    st.subheader("Distribution Analysis by Tier")
    selected_dist_kpi = st.selectbox("Select KPI for Distribution:", list(kpi_options.keys()), key="dist_box")
    kpi_col = kpi_options[selected_dist_kpi]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df, x='tier', y=kpi_col, hue='period', palette="Set2", ax=ax)
    plt.title(f"Distribution of {selected_dist_kpi}")
    st.pyplot(fig)

with tab2:
    st.subheader("Leaderboard (Top 10)")
    selected_rank_kpi = st.selectbox("Select KPI for Ranking:", list(kpi_options.keys()), key="rank_box")
    rank_col = kpi_options[selected_rank_kpi]
    
    # Sorting and taking top 10 based on selected KPI
    top_10 = df.sort_values(rank_col, ascending=False).head(10)
    
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_10, x=rank_col, y='player_name', hue='tier', dodge=False, ax=ax2)
    plt.title(f"Top 10 Players by {selected_rank_kpi}")
    st.pyplot(fig2)

with tab3:
    st.subheader("Individual Player Search")
    player_list = sorted(df['player_name'].unique())
    selected_player = st.selectbox("Select a player:", player_list)
    
    player_data = df[df['player_name'] == selected_player]
    
    st.write(f"Detailed Stats for **{selected_player}**:")
    st.dataframe(player_data[['player_name', 'tier', 'period', 'goals', 'assists', 'total_contribution', 'efficiency', 'discipline_score', 'minutes_played']])
    
    # Show comparison if player has data in both periods
    if len(player_data) > 1:
        st.write("### Evolution Over Time")
        melted_player = player_data.melt(id_vars=['period'], value_vars=['total_contribution', 'efficiency'], 
                                        var_name='Metric', value_name='Value')
        fig3, ax3 = plt.subplots()
        sns.barplot(data=melted_player, x='Metric', y='Value', hue='period', ax=ax3)
        st.pyplot(fig3)

# DATABASE PREVIEW
with st.expander("View Filtered SQL Data Table"):
    st.dataframe(df)

st.caption("Final Project: Python & SQL Course - Jan 2026")