import streamlit as st

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Bitoku Tengu Helper", layout="centered")
st.title("👺 Bitoku: Tengu AI & Scoring Helper")

# --- SESSION STATE (The Program's Memory) ---
if 'resources' not in st.session_state:
    st.session_state.resources = {"Wood": 0, "Stone": 0, "Jade": 0, "Sake": 0}
if 'attitude' not in st.session_state:
    st.session_state.attitude = "Inactive"
if 'mp' not in st.session_state:
    st.session_state.mp = 0

# Tabs for easy navigation on mobile
tab1, tab2 = st.tabs(["🎮 Turn Wizard", "📊 Ascension Scoring"])

# --- SIDEBAR: SETUP & DIFFICULTY ---
with st.sidebar:
    st.header("🛠️ Game Setup")
    difficulty = st.checkbox("Easier: No Spring MP for Crystals")
    fav_type = st.radio("Tengu Favorite (from Iwakura Rocks):", ["Yōkai", "Buildings", "Mitamas"])
    
    st.divider()
    st.header("🎒 Tengu Resources")
    for res in st.session_state.resources:
        col1, col2 = st.columns([2, 1])
        col1.write(f"{res}: {st.session_state.resources[res]}")
        if col2.button(f"+", key=f"add_{res}"):
            st.session_state.resources[res] += 1
    
    st.divider()
    st.write(f"**Attitude Tile:** {st.session_state.attitude}")
    if st.button("Manual Flip Attitude"):
        st.session_state.attitude = "Active" if st.session_state.attitude == "Inactive" else "Inactive"

# --- TAB 1: THE TURN WIZARD ---
with tab1:
    st.header("Tengu Activation Cycle (TAC)")
    card_pos = st.radio("Which card was selected by the Will of the Tengu?", 
                        ["Left", "Middle", "Right"], horizontal=True)

    st.subheader("Follow these checks in order:")
    
    # Step A
    if st.checkbox("A: Is Tengu at a CONTESTED CROSSING for the card's top half?"):
        st.success("ACTION: Cross the river. Take the card. (Tie-break: Randomly)")
    else:
        # Step B/C
        if st.checkbox("B/C: Is the location on the BOTTOM of the card available?"):
            col_b, col_c = st.columns(2)
            if col_b.button("Has ONLY LOCKED dice"):
                if st.session_state.attitude == "Inactive" and card_pos == "Left":
                    st.success("ACTION (Step B): Flip Attitude to ACTIVE. Unlock 1 die and place it.")
                    st.session_state.attitude = "Active"
                else:
                    st.warning("Conditions for Step B not met (must be leftmost card & inactive).")
            if col_c.button("Has UNLOCKED dice"):
                st.success("ACTION (Step C): Place unlocked die. Advance Kodama.")
        else:
            # Step F
            if st.checkbox("F: Can Tengu place in Home of the Great Spirit?"):
                st.success("ACTION: Place unlocked die. Score 3VP + 2VP per player 5/6 die.")
            else:
                st.info("Continue down TAC steps (G-K) or Step L: Tengu PASSES.")

# --- TAB 2: ASCENSION SCORING ---
with tab2:
    st.header("End of Game Scoring")
    
    yokai_count = st.number_input("Total Yōkai, Buildings, & Mitamas matching Iwakura Rocks:", 0)
    st.write("*(3 VP each)*")
    
    adv_yokai = st.number_input("Total 'Advanced' Yōkai collected:", 0)
    st.write("*(6 VP each)*")
    
    crystals = st.number_input("Total Crystals collected:", 0)
    st.write("*(2 VP each)*")
    
    kodama_leads = st.number_input("Regions where Tengu Kodama is AHEAD of yours:", 0)
    st.write("*(Standard track VP + 3 bonus VP per region)*")

    # Automatic Resource Calculation
    total_res = sum(st.session_state.resources.values())
    
    # Final Tally
    score = (yokai_count * 3) + (adv_yokai * 6) + (crystals * 2) + total_res + (kodama_leads * 3)
    
    st.divider()
    st.subheader(f"Total Tengu Points: {score}")
    st.caption("Note: Remember to also add VP for Buildings removed from board and Bitoku Path progress.")
