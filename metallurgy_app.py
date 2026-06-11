import streamlit as st

st.title("🏗️ Metallurgical Optimizer")

# --- 1. SIMPLE INPUTS ---
st.header("Inputs")
target_iron = st.number_input("Target Iron Production (Tons)", value=100)
fe_content = st.slider("Iron Grade in Ore (% Fe)", 45.0, 68.0, 62.0)
basicity = st.slider("Target Basicity (Ratio)", 0.8, 2.0, 1.2)

# Prices in Rupees
ore_price = st.number_input("Ore Price (₹/Ton)", value=8500)
flux_price = st.number_input("Flux Price (₹/Ton)", value=1500)

# --- 2. BARE LOGIC ---
# Calculate Ore needed (Assuming 95% recovery)
ore_required = (target_iron / (fe_content / 100)) / 0.95

# Calculate the Dirt (Silica) left in the ore (Assuming it's 10% of the ore)
total_sio2 = ore_required * 0.10

# Calculate Flux needed using the Basicity Ratio
flux_required = basicity * total_sio2

# Calculate Total Cost
total_cost = (ore_required * ore_price) + (flux_required * flux_price)

# --- 3. CLEAN OUTPUTS ---
st.header("Results")
st.metric("Iron Ore Needed", f"{int(ore_required)} Tons")
st.metric("Limestone (Flux) Needed", f"{int(flux_required)} Tons")
st.metric("Total Material Cost", f"₹{int(total_cost)}")
