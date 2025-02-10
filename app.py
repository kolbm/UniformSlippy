import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# Function to calculate if the car will slip
def calculate_slip(static_friction, velocity, radius):
    # Calculate the required coefficient of friction
    required_friction = (velocity ** 2) / (radius * 10)  # g = 10 m/s²

    # Determine if the car slips
    if required_friction > static_friction:
        return "The car will slip."
    else:
        return "The car will not slip."

# Function to calculate the missing variable
def calculate_missing(static_friction, velocity, radius, missing_variable):
    if missing_variable == "Coefficient of Static Friction":
        return round((velocity ** 2) / (radius * 10), 3)
    elif missing_variable == "Velocity":
        return round(math.sqrt(static_friction * 10 * radius), 3)
    elif missing_variable == "Radius":
        return round((velocity ** 2) / (static_friction * 10), 3)
    else:
        return "Invalid selection."

# Streamlit UI
st.title("Car Slip Calculator with Graphs (g = 10 m/s²)")

st.sidebar.header("Input Parameters")
static_friction = st.sidebar.number_input("Coefficient of Static Friction (μ)", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
velocity = st.sidebar.number_input("Velocity (m/s)", min_value=0.0, value=15.0)
radius = st.sidebar.number_input("Radius of Curve (m)", min_value=0.1, value=50.0)

calculation_type = st.radio("Select Calculation Type:", 
                           ("Check if the car will slip", "Calculate a missing variable"))

if calculation_type == "Check if the car will slip":
    result = calculate_slip(static_friction, velocity, radius)
    st.write(f"**Result:** {result}")

elif calculation_type == "Calculate a missing variable":
    missing_variable = st.selectbox("Select the missing variable:", 
                                    ["Coefficient of Static Friction", "Velocity", "Radius"])
    missing_value = calculate_missing(static_friction, velocity, radius, missing_variable)
    st.write(f"**The calculated value for {missing_variable} is:** {missing_value}")

st.write("All values should be entered in metric units (meters per second, meters).")

# Graph: Required friction vs. Velocity for different radii
st.subheader("Required Friction vs. Velocity for Different Radii")

velocities = np.linspace(5, 50, 100)
radii = [20, 50, 100]  # Different radii to compare

plt.figure(figsize=(6,4))
for r in radii:
    required_friction = (velocities ** 2) / (r * 10)
    plt.plot(velocities, required_friction, label=f"Radius = {r} m")

plt.axhline(y=static_friction, color='r', linestyle='--', label=f"Given μ = {static_friction}")
plt.xlabel("Velocity (m/s)")
plt.ylabel("Required Coefficient of Friction (μ)")
plt.title("Required Friction vs. Velocity")
plt.legend()
plt.grid()
st.pyplot(plt)

# Graph: Required friction vs. Radius for different velocities
st.subheader("Required Friction vs. Radius for Different Velocities")

radii = np.linspace(10, 200, 100)
velocities = [10, 20, 30]  # Different velocities to compare

plt.figure(figsize=(6,4))
for v in velocities:
    required_friction = (v ** 2) / (radii * 10)
    plt.plot(radii, required_friction, label=f"Velocity = {v} m/s")

plt.axhline(y=static_friction, color='r', linestyle='--', label=f"Given μ = {static_friction}")
plt.xlabel("Radius (m)")
plt.ylabel("Required Coefficient of Friction (μ)")
plt.title("Required Friction vs. Radius")
plt.legend()
plt.grid()
st.pyplot(plt)
