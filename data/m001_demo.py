import streamlit as st
import pandas as pd
import requests
from io import StringIO
import math

st.set_page_config(
    page_title="Fantasy Draft Assistant 2026",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- DATA LOADING ----------
@st.cache_data(ttl=3600)
def load_adp_data():
    """Load latest PPR ADP from FantasyFootballCalculator"""
    url = "https://fantasyfootballcalculator.com/adp/csv/ppr.csv?teams=12"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        content = r.text
        lines = content.strip().splitlines()
        header_idx = None
        for i, line in enumerate(lines):
            if line.startswith("ADP,Overall"):
                header_idx = i
                break
        if header_idx is None:
            raise ValueError("Could not find ADP header")
        csv_data = "\n".join(lines[header_idx:])
        df = pd.read_csv(StringIO(csv_data))
        df.columns = [c.strip() for c in df.columns]
        # First col is round.pick style ADP, Overall is the true overall ADP number
        df = df.rename(columns={
            "Name": "Player",
            "Position": "Pos",
            "Overall": "OverallADP",
            "ADP": "RoundADP",
        })
        df["ADP"] = pd.to_numeric(df["OverallADP"], errors="coerce")
        df = df.dropna(subset=["Player", "ADP"])
        df = df.sort_values("ADP").reset_index(drop=True)
        df["Rank"] = range(1, len(df) + 1)
        df["Pos"] = df["Pos"].astype(str).str.upper().str.strip()
        df["Pos"] = df["Pos"].replace({"PK": "K", "DEF": "DST", "D/ST": "DST", "DEFENSE": "DST"})
        cols = ["Rank", "Player", "Pos", "Team", "ADP", "Bye", "Times Drafted"]
        for c in cols:
            if c not in df.columns:
                df[c] = None
        return df[cols].copy()
    except Exception as e:
        return get_fallback_data()

def get_fallback_data():
    """Hardcoded top players as of early August 2026 (PPR)"""
    data = [
        (1, "Jahmyr Gibbs", "RB", "DET", 1.6, 6),
        (2, "Bijan Robinson", "RB", "ATL", 2.0, 11),
        (3, "Puka Nacua", "WR", "LAR", 2.7, 11),
        (4, "Ja'Marr Chase", "WR", "CIN", 3.9, 6),
        (5, "Christian McCaffrey", "RB", "SF", 5.2, 8),
        (6, "Jaxon Smith-Njigba", "WR", "SEA", 6.0, 11),
        (7, "Amon-Ra St. Brown", "WR", "DET", 7.1, 6),
        (8, "Jonathan Taylor", "RB", "IND", 7.6, 13),
        (9, "De'Von Achane", "RB", "MIA", 9.4, 6),
        (10, "Drake London", "WR", "ATL", 10.8, 11),
        (11, "CeeDee Lamb", "WR", "DAL", 11.3, 14),
        (12, "Rashee Rice", "WR", "KC", 11.6, 5),
        (13, "Chase Brown", "RB", "CIN", 12.3, 6),
        (14, "Justin Jefferson", "WR", "MIN", 13.0, 6),
        (15, "Ashton Jeanty", "RB", "LV", 14.0, 13),
        (16, "James Cook III", "RB", "BUF", 15.3, 7),
        (17, "Derrick Henry", "RB", "BAL", 16.4, 13),
        (18, "A.J. Brown", "WR", "NE", 17.4, 11),
        (19, "Saquon Barkley", "RB", "PHI", 18.7, 10),
        (20, "Omarion Hampton", "RB", "LAC", 20.0, 7),
        (21, "Chris Olave", "WR", "NO", 20.2, 8),
        (22, "George Pickens", "WR", "DAL", 21.3, 14),
        (23, "Nico Collins", "WR", "HOU", 23.0, 8),
        (24, "Josh Jacobs", "RB", "GB", 24.6, 11),
        (25, "Jeremiyah Love", "RB", "ARI", 25.2, 14),
        (26, "Josh Allen", "QB", "BUF", 26.4, 7),
        (27, "Zay Flowers", "WR", "BAL", 26.5, 13),
        (28, "Kenneth Walker III", "RB", "KC", 26.7, 5),
        (29, "Breece Hall", "RB", "NYJ", 28.1, 13),
        (30, "Garrett Wilson", "WR", "NYJ", 28.2, 13),
        (31, "DeVonta Smith", "WR", "PHI", 28.9, 10),
        (32, "Cam Skattebo", "RB", "NYG", 30.7, 8),
        (33, "Kyren Williams", "RB", "LAR", 32.2, 11),
        (34, "Trey McBride", "TE", "ARI", 35.2, 14),
        (35, "Brock Bowers", "TE", "LV", 40.7, 13),
        (36, "Drake Maye", "QB", "NE", 49.9, 11),
        (37, "Lamar Jackson", "QB", "BAL", 54.0, 13),
        (38, "Joe Burrow", "QB", "CIN", 57.5, 6),
        (39, "Jayden Daniels", "QB", "WAS", 71.6, 7),
        (40, "Jalen Hurts", "QB", "PHI", 75.1, 10),
    ]
    df = pd.DataFrame(data, columns=["Rank", "Player", "Pos", "Team", "ADP", "Bye"])
    df["Times Drafted"] = 500
    return df

# ---------- SESSION STATE ----------
if "drafted" not in st.session_state:
    st.session_state.drafted = set()  # player names taken by anyone
if "my_team" not in st.session_state:
    st.session_state.my_team = []  # list of dicts
if "pick_number" not in st.session_state:
    st.session_state.pick_number = 1
if "data" not in st.session_state:
    st.session_state.data = load_adp_data()

df = st.session_state.data

# ---------- SIDEBAR SETTINGS ----------
st.sidebar.title("🏈 Draft Settings")
league_size = st.sidebar.selectbox("League Size", [8, 10, 12, 14], index=2)
scoring = st.sidebar.radio("Scoring", ["PPR", "Half-PPR", "Standard"], index=0)
draft_pos = st.sidebar.number_input("Your Draft Position", min_value=1, max_value=league_size, value=1)
rounds = st.sidebar.slider("Rounds", 10, 18, 15)

st.sidebar.markdown("---")
st.sidebar.subheader("Quick Actions")
if st.sidebar.button("🔄 Reset Draft", type="primary"):
    st.session_state.drafted = set()
    st.session_state.my_team = []
    st.session_state.pick_number = 1
    st.rerun()

if st.sidebar.button("↻ Refresh Rankings"):
    st.cache_data.clear()
    st.session_state.data = load_adp_data()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Data: FantasyFootballCalculator PPR ADP (live)")
st.sidebar.caption("Updated ~daily · Early Aug 2026")

# ---------- HELPERS ----------
def get_available():
    return df[~df["Player"].isin(st.session_state.drafted)].copy()

def current_round_pick():
    """Estimate current overall pick number"""
    return st.session_state.pick_number

def is_my_turn(overall_pick: int) -> bool:
    """Snake draft logic"""
    round_num = (overall_pick - 1) // league_size + 1
    pos_in_round = (overall_pick - 1) % league_size + 1
    if round_num % 2 == 1:  # odd rounds: 1 → N
        return pos_in_round == draft_pos
    else:  # even rounds: N → 1
        return pos_in_round == (league_size - draft_pos + 1)

def roster_needs(my_team):
    """Simple count of what we still need (typical starters)"""
    counts = {"QB": 0, "RB": 0, "WR": 0, "TE": 0, "FLEX": 0, "K": 0, "DST": 0}
    for p in my_team:
        pos = p["Pos"]
        if pos in counts:
            counts[pos] += 1
        elif pos == "RB" or pos == "WR" or pos == "TE":
            counts["FLEX"] += 1
    # Typical needs for 12-team: 1QB, 2RB, 2WR, 1TE, 1FLEX, 1K, 1DST
    needs = {
        "QB": max(0, 1 - counts["QB"]),
        "RB": max(0, 2 - counts["RB"]),
        "WR": max(0, 2 - counts["WR"]),
        "TE": max(0, 1 - counts["TE"]),
        "FLEX": max(0, 1 - counts["FLEX"]),  # extra RB/WR/TE
        "K": max(0, 1 - counts["K"]),
        "DST": max(0, 1 - counts["DST"]),
    }
    return needs

# ---------- MAIN UI ----------
st.title("🏈 2026 Fantasy Football Draft Assistant")
st.caption(f"Live PPR ADP · {league_size}-team · Your pick: #{draft_pos} · Snake draft")

# Status bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Overall Pick", f"#{st.session_state.pick_number}")
with col2:
    my_turn = is_my_turn(st.session_state.pick_number)
    st.metric("Your Turn?", "✅ YES" if my_turn else "⏳ Waiting")
with col3:
    st.metric("Players Drafted", len(st.session_state.drafted))
with col4:
    st.metric("On Your Roster", len(st.session_state.my_team))

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Recommendations", "📋 Available Players", "👤 My Team", "📊 Full Board"])

available = get_available()

with tab1:
    st.subheader("Who should you pick?")
    
    if my_turn:
        st.success("🟢 **It's your turn!** Here are the top recommendations.")
    else:
        st.info("It's not your pick yet. Review the board and plan ahead.")

    # Top overall available
    st.markdown("### 🔥 Best Available Overall")
    top = available.head(12)
    for i, row in top.iterrows():
        value = ""
        if row["ADP"] < st.session_state.pick_number - 5:
            value = " 💎 **VALUE**"
        elif row["ADP"] > st.session_state.pick_number + 8:
            value = " ⬆️ Reach"
        st.write(f"**{row['Rank']}. {row['Player']}** ({row['Pos']} - {row['Team']}) · ADP {row['ADP']:.1f}{value}")

    st.markdown("---")
    st.markdown("### 📍 Best by Position")
    
    pos_cols = st.columns(4)
    for idx, pos in enumerate(["RB", "WR", "TE", "QB"]):
        with pos_cols[idx]:
            st.markdown(f"**{pos}**")
            pos_df = available[available["Pos"] == pos].head(5)
            for _, row in pos_df.iterrows():
                st.caption(f"{row['Player']} ({row['ADP']:.1f})")

    # Needs based suggestion
    needs = roster_needs(st.session_state.my_team)
    if any(v > 0 for v in needs.values()):
        st.markdown("---")
        st.markdown("### 🧩 Roster Needs")
        need_str = ", ".join([f"{k}: {v}" for k, v in needs.items() if v > 0])
        st.write(need_str)

with tab2:
    st.subheader("Available Players")
    
    # Filters
    fcol1, fcol2, fcol3 = st.columns([2, 1, 1])
    with fcol1:
        search = st.text_input("Search player", placeholder="e.g. Gibbs, Chase, Allen...")
    with fcol2:
        pos_filter = st.multiselect("Position", ["QB", "RB", "WR", "TE", "K", "DST"], default=[])
    with fcol3:
        show_n = st.selectbox("Show top", [25, 50, 100, 200], index=1)

    filtered = available.copy()
    if search:
        filtered = filtered[filtered["Player"].str.contains(search, case=False, na=False)]
    if pos_filter:
        filtered = filtered[filtered["Pos"].isin(pos_filter)]
    
    filtered = filtered.head(show_n)

    # Display with draft buttons
    st.write(f"Showing {len(filtered)} available players")
    
    for _, row in filtered.iterrows():
        c1, c2, c3 = st.columns([4, 1, 1])
        with c1:
            st.write(f"**{row['Rank']}. {row['Player']}** · {row['Pos']} · {row['Team']} · ADP {row['ADP']:.1f} · Bye {int(row['Bye']) if pd.notna(row['Bye']) else '?'}")
        with c2:
            if st.button("Draft 🟢", key=f"draft_{row['Player']}", help="Add to MY team"):
                st.session_state.drafted.add(row["Player"])
                st.session_state.my_team.append({
                    "Player": row["Player"],
                    "Pos": row["Pos"],
                    "Team": row["Team"],
                    "ADP": row["ADP"],
                    "Pick": st.session_state.pick_number
                })
                st.session_state.pick_number += 1
                st.rerun()
        with c3:
            if st.button("Taken 🔴", key=f"taken_{row['Player']}", help="Someone else drafted"):
                st.session_state.drafted.add(row["Player"])
                st.session_state.pick_number += 1
                st.rerun()

with tab3:
    st.subheader("Your Roster")
    if not st.session_state.my_team:
        st.info("No players drafted yet. Go to Available Players and click **Draft 🟢**.")
    else:
        team_df = pd.DataFrame(st.session_state.my_team)
        # Group by position
        for pos in ["QB", "RB", "WR", "TE", "K", "DST"]:
            pos_players = team_df[team_df["Pos"] == pos]
            if not pos_players.empty:
                st.markdown(f"**{pos}**")
                for _, p in pos_players.iterrows():
                    st.write(f"• {p['Player']} ({p['Team']}) — drafted at overall #{p['Pick']} (ADP {p['ADP']:.1f})")
        
        st.markdown("---")
        if st.button("Remove last player from my team"):
            if st.session_state.my_team:
                last = st.session_state.my_team.pop()
                st.session_state.drafted.discard(last["Player"])
                st.session_state.pick_number = max(1, st.session_state.pick_number - 1)
                st.rerun()

with tab4:
    st.subheader("Full ADP Board (All Players)")
    st.dataframe(
        df[["Rank", "Player", "Pos", "Team", "ADP", "Bye"]].style.format({"ADP": "{:.1f}"}),
        width="stretch",
        height=600
    )

# Footer
st.markdown("---")
st.caption("Built for you · Data refreshes from FantasyFootballCalculator · Not affiliated with any league platform · Good luck in your draft! 🏆")
