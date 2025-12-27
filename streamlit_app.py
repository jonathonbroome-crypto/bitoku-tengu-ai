import streamlit as st

# --- INITIALIZATION ---
if 'turn_count' not in st.session_state:
    st.session_state.turn_count = 1
if 'resources' not in st.session_state:
    st.session_state.resources = {"Wood": 0, "Stone": 0, "Jade": 0, "Sake": 0}
if 'attitude' not in st.session_state:
    st.session_state.attitude = "Inactive"

def next_turn():
    # This function resets the transient UI elements for a new turn
    st.session_state.turn_count += 1
    # We use a 'key' on widgets to force them to reset when this is called
    st.info(f"Turn {st.session_state.turn_count - 1} complete. Starting Turn {st.session_state.turn_count}!")

st.title(f"👺 Bitoku Helper: Turn {st.session_state.turn_count}")

# --- SIDEBAR (Persistent Data) ---
with st.sidebar:
    st.header("📊 Bot State")
    st.write(f"**Attitude:** {st.session_state.attitude}")
    # Display resources with increment buttons
    for res, val in st.session_state.resources.items():
        col1, col2 = st.columns([2,1])
        col1.write(f"{res}: {val}")
        if col2.button("+", key=f"btn_{res}"):
            st.session_state.resources[res] += 1
            st.rerun()

# --- THE TURN LOOP ---
st.subheader("1. Roll & Select Card")
roll = st.number_input("Enter lowest die roll (1-6):", 1, 6, key=f"roll_{st.session_state.turn_count}")

st.subheader("2. Run the TAC Hierarchy")
# We use keys based on turn_count to ensure checkboxes reset every turn
step_a = st.checkbox("Step A: Contested Crossing available?", key=f"a_{st.session_state.turn_count}")

if step_a:
    st.success("ACTION: Cross and take card.")
else:
    step_b = st.checkbox("Step B/C: Location available?", key=f"bc_{st.session_state.turn_count}")
    if step_b:
        st.success("ACTION: Place die / Unlock die.")

# --- THE NEXT TURN BUTTON ---
st.divider()
if st.button("🏁 Finish Tengu Turn & Reset Checklist", type="primary"):
    next_turn()
    st.rerun() # Forces the app to refresh with the new turn_count

if st.button("🔄 Reset Entire Game"):
    st.session_state.clear()
    st.rerun()
