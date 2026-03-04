import streamlit as st

st.set_page_config(page_title="Agri Drone Spreading Calculator", layout="centered")
st.title("🚁 Spreader settings")
st.caption("Turn-loss based spreading model")

st.divider()

# -----------------------
# Constants
# -----------------------
TURN_LOSS = 0
ACRE_M2 = 4046.86

# Fixed configuration (current calibration)
VALVE_SETTING = 30        # %
PWM_SETTING = 1500        # PWM
DISCHARGE_RATE = 10.0     # kg/min
SWATH_WIDTH = 7.5         # meters

# -----------------------
# Inputs
# -----------------------

material = st.selectbox(
    "Spreading Material",
    ["Urea", "DAP", "Potash", "Paddy", "Sesame", "Mustard"]
)

dispense_per_acre = st.number_input(
    "Dispense weight per acre (kg/acre)",
    min_value=1.0,
    max_value=200.0,
    value=25.0,
    step=1.0

)

area = st.number_input(
    "Area (acre)",
    min_value=0.1,
    max_value=50.0,
    value=1.0,
    step=0.1
)

turns = st.number_input(
    "Number of turns (N)",
    min_value=0,
    max_value=300,
    value=11,
    step=1
)

st.divider()

# -----------------------
# Calculations
# -----------------------

# Total material required (NEW constant display value)
total_dispense = dispense_per_acre * area

# Real area
A_real = area

# Ideal area required considering turn loss
A_ideal = A_real / ((1 - TURN_LOSS) ** turns)

# Spray time (seconds)
t_spray = ((total_dispense / DISCHARGE_RATE) * 60) - (turns * 4)

# Required speed (m/s)
v_required = (A_ideal * ACRE_M2) / (SWATH_WIDTH * t_spray)

# Round to 1 decimal
v_required = round(v_required, 1)

# -----------------------
# Output
# -----------------------
st.subheader("📊 Results")

c1, c2 = st.columns(2)

with c1:
    st.metric("Required Speed (m/s)", f"{v_required}")
    st.metric("Total Weight (kg)", f"{round(total_dispense,1)}")

with c2:
    st.metric("Valve Open Setting (%)", f"{VALVE_SETTING}%")
    st.metric("PWM Setting", f"{PWM_SETTING}")

st.caption(
    "Model:\n"
    "Total Weight = kg/acre × Area\n"
    "A_ideal = Area / (1 - 0.02)^N\n"
    "Speed = (A_ideal × 4046.86) / (Swath × SprayTime)\n\n"
    "Turn loss fixed at 2% per turn."
)




