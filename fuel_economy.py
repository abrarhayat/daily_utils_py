import streamlit as st

st.title("Fuel Cost Comparison App")

# Input fields
distance_one_way = st.number_input(
    "Enter one-way distance (km):", min_value=0.0, value=933.0, step=1.0
)
fuel_price = st.number_input(
    "Enter fuel price (per litre):", min_value=0.0, value=1.98, step=0.01
)
consumption1 = st.number_input(
    "Vehicle 1 fuel consumption (L/100km):", min_value=0.0, value=5.5, step=0.1
)
consumption2 = st.number_input(
    "Vehicle 2 fuel consumption (L/100km):", min_value=0.0, value=8.5, step=0.1
)

# Calculations
distance_round = distance_one_way * 2
fuel_used1 = (consumption1 / 100.0) * distance_round
fuel_used2 = (consumption2 / 100.0) * distance_round
cost1 = fuel_used1 * fuel_price
cost2 = fuel_used2 * fuel_price
diff = cost2 - cost1

# Display results
st.subheader("Results")
st.write(f"Round-trip distance: **{distance_round:.2f} km**")
st.write(f"Vehicle 1 will use approx: **{fuel_used1:.2f} L**, costing **${cost1:.2f}**")
st.write(f"Vehicle 2 will use approx: **{fuel_used2:.2f} L**, costing **${cost2:.2f}**")
st.write(f"Difference in cost (Vehicle 2 minus Vehicle 1): **${diff:.2f}**")

if diff > 0:
    st.success(f"Vehicle 2 costs **${diff:.2f}** more than Vehicle 1 for this trip.")
elif diff < 0:
    st.success(f"Vehicle 2 costs **${-diff:.2f}** less than Vehicle 1 for this trip.")
else:
    st.info("Both vehicles cost the same for this trip.")

