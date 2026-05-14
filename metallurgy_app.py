import streamlit as st
import plotly.graph_objects as go

# --- CONFIG ---
st.set_page_config(page_title="Blast Furnace Pro", layout="wide")
st.title("🏗️ Metallurgical Charge Optimizer")

# --- SIDEBAR: INPUTS ---
st.sidebar.header("1. Material Chemistry")
mineral = st.sidebar.selectbox("Iron Ore Mineral", ["Hematite (Fe2O3)", "Magnetite (Fe3O4)"])

# Slider 1: Iron Grade
fe_content = st.sidebar.slider("Iron Grade (% Fe)", 45.0, 68.0, 62.0)

# Slider 2: Silica Ratio (Related to the remaining gangue)
gangue_total = 100.0 - fe_content
sio2_in_gangue_percent = st.sidebar.slider("Silica Severity (% SiO2 in Gangue)", 40.0, 90.0, 70.0)
sio2_content = (gangue_total * sio2_in_gangue_percent) / 100

st.sidebar.header("2. Process Parameters")
flux_type = st.sidebar.selectbox("Flux Agent", ["Limestone (CaO)", "Dolomite (CaO+MgO)"])
basicity = st.sidebar.slider("Target Basicity (B = CaO/SiO2)", 0.8, 2.0, 1.2)
target_iron = st.sidebar.number_input("Target Production (Tons)", value=100)

st.sidebar.header("3. Economic Data")
ore_price = st.sidebar.number_input("Ore Price ($/Ton)", value=110)
flux_price = st.sidebar.number_input("Flux Price ($/Ton)", value=40)

# --- THE CALCULATIONS (The Logic) ---
# 1. How much Ore do we need? 
# Assuming 95% recovery of Fe into the Pig Iron
ore_required = (target_iron / (fe_content / 100)) / 0.95

# 2. How much total SiO2 is entering?
total_sio2 = (sio2_content / 100) * ore_required

# 3. Flux calculation
# If Limestone, we assume 90% effective CaO. If Dolomite, 80% effective basic oxides.
flux_efficiency = 0.90 if flux_type == "Limestone (CaO)" else 0.80
cao_needed = basicity * total_sio2
flux_required = cao_needed / flux_efficiency

# 4. Outputs
slag_generated = total_sio2 + cao_needed
total_cost = (ore_required * ore_price) + (flux_required * flux_price)

# --- MAIN DASHBOARD ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Ore Needed", f"{int(ore_required)} T")
c2.metric("Flux Needed", f"{int(flux_required)} T")
c3.metric("Slag Waste", f"{int(slag_generated)} T")
c4.metric("Cost / Ton Fe", f"${round(total_cost/target_iron, 2)}")

# --- VISUAL: SANKEY DIAGRAM ---
# Defining the flows
fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 20, thickness = 20,
      label = ["IRON ORE", "FLUX", "BLAST FURNACE", "PIG IRON", "SLAG"],
      color = ["#ef553b", "#636efa", "#ab63fa", "#00cc96", "#fb00d1"]
    ),
    link = dict(
      source = [0, 1, 2, 2], 
      target = [2, 2, 3, 4],
      value = [ore_required, flux_required, target_iron, slag_generated]
  ))])

st.plotly_chart(fig, use_container_width=True)

st.write(f"**Technical Note:** At {fe_content}% Fe, your ore contains {round(gangue_total,1)}% impurities. To maintain a basicity of {basicity}, you are consuming {round((flux_required/ore_required)*1000)} kg of flux for every ton of ore processed.")