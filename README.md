# Transformer Losses Analyzer & Efficiency Calculator

A **GUI-based tool** to analyze transformer losses (iron, copper, stray) and calculate efficiency. Users can input transformer specifications, material properties, and load conditions to visualize losses and efficiency trends.

## Features
- **Inputs**: Transformer specs (voltage, power, frequency), material properties (core type, winding resistance), and load conditions.
- **Losses Calculation**:
  - **Iron (core) losses**: Hysteresis & eddy currents.
  - **Copper losses**: Winding resistance & current.
  - **Stray & dielectric losses**: Stray flux & insulation heating.
- **Efficiency Analysis**:
  - Formula:  
    \[
    \eta = \left(\frac{\text{Output Power}}{\text{Input Power}}\right) \times 100\%
    \]
  - Graph: Efficiency vs. Load.
  - Material comparison: Impact on efficiency.

## Technologies
- **Python**: Tkinter, PyQt, or Streamlit for GUI.
- **MATLAB (optional)**: For simulation.

## How to Use
1. Clone the repository:
   ```bash
   git clone https://github.com/S1aY3x/GUI.git