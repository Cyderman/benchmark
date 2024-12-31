import streamlit as st
import pandas as pd

# Step 1: Load the summary data
lookup_table = pd.read_csv("lookup_table.csv")

# Step 2: Streamlit App
st.title("Horse Racing Performance Evaluation")

# Grade selection
grade = st.radio("Select Grade:", options=['A-', 'A', 'A+', 'S-', 'S', 'S+', 'SS-'])

# Direction selection
direction = st.radio("Select Direction:", options=['Left', 'Right'])
direction_value = f"{direction}Turning"

# Surface selection
surface = st.radio("Select Surface:", options=['Dirt', 'Turf'])
surface_value = surface  # Assigning surface to surface_value for clarity

# Condition selection
condition = st.radio("Select Condition:", options=['Sloppy', 'Soft', 'Yielding', 'Good', 'Fast'])
cond_range_map = {'Sloppy': 0.0, 'Soft': 0.25, 'Yielding': 0.5, 'Good': 0.75, 'Fast': 1.0}
cond_range = cond_range_map[condition]

# Distance selection
distance = st.radio("Select Race Distance:", options=list(range(4, 13)))

# Input finish time
fin_time = st.number_input("Enter Finish Time (seconds):", min_value=0.0, step=0.01)

# Function to evaluate benchmarks
def evaluate_benchmarks(fin_time, grade, direction_value, surface_value, cond_range, race_distance):
    # Filter lookup table for matching parameters
    relevant_benchmarks = lookup_table[
        (lookup_table['grade'] == grade) &
        (lookup_table['direction_value'] == direction_value) &
        (lookup_table['surface_value'] == surface_value) &
        (lookup_table['cond_range'] == cond_range) &
        (lookup_table['race_distance'] == race_distance)
    ]

    # Check against benchmarks
    relevant_benchmarks['fast_enough_to_win'] = fin_time <= relevant_benchmarks['avg_winner_time']
    relevant_benchmarks['fast_enough_to_place'] = fin_time <= relevant_benchmarks['avg_top3_time']

    return relevant_benchmarks[['race_type', 'fast_enough_to_win', 'fast_enough_to_place']]

# Evaluate benchmarks if inputs are valid
if fin_time > 0:
    results = evaluate_benchmarks(fin_time, grade, direction_value, surface_value, cond_range, distance)

    # Display results
    st.subheader("Evaluation Results")
    for _, row in results.iterrows():
        st.write(f"Race Type: {row['race_type']}")
        st.markdown(
            f"- Win Benchmark: {'✅' if row['fast_enough_to_win'] else '❌'}")
        st.markdown(
            f"- Podium Benchmark: {'✅' if row['fast_enough_to_place'] else '❌'}")
else:
    st.warning("Please enter a valid finish time.")
