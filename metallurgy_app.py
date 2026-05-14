import streamlit as st
import plotly.graph_objects as go
import numpy as np

# ==========================================
# PROJECT: BLAST FURNACE CHARGE CALCULATOR
# STUDENT VERSION - INDIAN MARKET CONTEXT
# ==========================================

st.set_page_config(page_title="Iron Making Simulator", layout="wide")

# Title of the Project
st.title("🏗️ Blast Furnace Material & Cost Analyzer")
st.markdown("---")

# --- SIDEBAR INPUTS ---
st.sidebar.header("📥 INPUT PARAMETERS")

# 1. Choosing the Metal Ore
mineral_selection = st.sidebar.selectbox(
    "Select Iron Ore Type", 
    ["Hematite (Fe2O3)", "Magnetite (Fe3O4)"]
)

# 2. Ore Quality (Iron Content)
# Fresher logic: Manual Sliders for every detail
iron_percent = st.sidebar.slider("Iron Content in Ore (Fe %)", 45.0, 70.0, 62.0)
impurities_percent = 100.0 - iron_percent

# 3. Silica (Gangue) logic
silica_in_gangue = st.sidebar.slider("Silica (SiO2) in Gangue %", 50, 90, 75)
actual_sio2_percent = (impurities_percent * silica_in_gangue) / 100

# 4. Process Target
target_basicity = st.sidebar.slider("Target Slag Basicity (CaO/SiO2)", 0.8, 2.0, 1.2)
production_aim = st.sidebar.number_input("Target Pig Iron Production (Tons)", value=100)

# 5. Flux Choice
flux_selection = st.sidebar.selectbox("Choose Flux Material", ["Limestone", "Dolomite"])

# 6. INDIAN PRICING (Rupees)
st.sidebar.subheader("💰 Market Rates (INR)")
price_ore = st.sidebar.number_input("Iron Ore Price (₹ per Ton)", value=8000)
price_flux = st.sidebar.number_input("Flux Price (₹ per Ton)", value=1500)

# --- MANUAL CALCULATIONS (The "Long" Way) ---

# Step 1: Calculate Total Ore Required
# We assume 5% loss in the process (95% recovery)
ore_needed = (production_aim / (iron_percent / 100)) / 0.95

# Step 2: Calculate total Silica entering the furnace
total_sio2_tons = (actual_sio2_percent / 100) * ore_needed

# Step 3: Calculate Flux needed to neutralize Silica
# Formula: CaO = Basicity * SiO2
cao_required = target_basicity * total_sio2_tons

# Efficiency of Flux (Limestone is better than Dolomite for CaO)
if flux_selection == "Limestone":
    flux_efficiency = 0.92
else:
    flux_efficiency = 0.82

total_flux_needed = cao_required / flux_efficiency

# Step 4: Slag Generation (Waste)
# Slag is roughly Silica + Flux used
total_slag = total_sio2_tons + cao_required

# Step 5: Total Economics
cost_of_ore = ore_needed * price_ore
cost_of_flux = total_flux_needed * price_flux
grand_total_cost = cost_of_ore + cost_of_flux
cost_per_ton_iron = grand_total_cost / production_aim

# --- DISPLAYING RESULTS ---

# Top Row Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Ore Required", f"{round(ore_needed, 2)} Tons")
with col2:
    st.metric("Total Flux Required", f"{round(total_flux_needed, 2)} Tons")
with col3:
    st.metric("Total Slag Produced", f"{round(total_slag, 2)} Tons")

st.markdown("---")

# Costing Metric (The Big One)
st.subheader("📊 Financial Summary")
st.info(f"The estimated cost to produce 1 Ton of Pig Iron is: **₹ {int(cost_per_ton_iron)}**")

# --- SANKEY DIAGRAM VISUAL ---
st.subheader("🔄 Material Flow Visualization")

# Defining labels and flow values
label_list = ["Iron Ore", "Flux", "Blast Furnace", "Pig Iron", "Slag Waste"]
source_indices = [0, 1, 2, 2] # From where
target_indices = [2, 2, 3, 4] # To where
values_list = [ore_needed, total_flux_needed, production_aim, total_slag]

# Plotting
fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = label_list,
      color = "orange"
    ),
    link = dict(
      source = source_indices,
      target = target_indices,
      value = values_list
    ))])

st.plotly_chart(fig, use_container_width=True)

# Footer Detail
st.write(f"Note: This calculation uses a 95% Fe recovery rate and assumes a {flux_efficiency*100}% purity for {flux_selection}.")
