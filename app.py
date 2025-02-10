import streamlit as st
import numpy as np
import pandas as pd

# Load the image as the title
image_url = "https://raw.githubusercontent.com/kolbm/UniformSlippy/refs/heads/main/Screenshot%202025-02-10%20094911.png"
st.image(image_url, use_column_width=True)

def calculate_slip(static_friction, velocity, radius):
    required_friction = (velocity ** 2) / (radius * 10)  # g = 10 m/s²
    if required_friction > static_friction:
        return "The car will slip."
    else:
        return "The car will not slip."

def calculate_missing(static_friction, velocity, radius, missing_variable):
    if missing_variable == "Coefficient of Static Friction":
        return round((velocity ** 2) / (radius * 10), 3)
    elif missing_variable == "Velocity":
        return round(np.sqrt(static_friction * 10 * radius), 3)
    elif missing_variable == "Radius":
        return round((velocity ** 2) / (static_friction * 10), 3)
    else:
        return "Invalid selection."

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

# Generate data for charts
velocities = np.linspace(5, 50, 100)
radii = np.array([20, 50, 100])

# Create data for velocity vs. required friction
data_velocity = pd.DataFrame({f"Radius {r} m": (velocities ** 2) / (r * 10) for r in radii}, index=velocities)
st.line_chart(data_velocity.rename_axis("Velocity (m/s)").rename("Required Friction"))

# Create data for radius vs. required friction at different velocities
radii = np.linspace(10, 200, 100)
velocities_set = [10, 20, 30]
data_radius = pd.DataFrame({f"Velocity {v} m/s": (v ** 2) / (radii * 10) for v in velocities_set}, index=radii)
st.line_chart(data_radius.rename_axis("Radius (m)").rename("Required Friction"))
